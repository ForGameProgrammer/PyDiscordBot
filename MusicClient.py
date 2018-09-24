import asyncio
import discord


class MusicPlayer():
    queue = []
    client: discord.Client = None
    media_client: discord.VoiceClient = None
    player:discord.voice_client.StreamPlayer = None  # ytdl player object
    voicechannel = None
    textchannel = None
    repeat = None

    def __init__(self, clnt, voicechannel, textchannel):
        self.client = clnt
        self.voicechannel = voicechannel
        self.textchannel = textchannel

    def play_after(self):
        if self.repeat is None:
            if len(self.queue) < 1:
                renk = self.disconnect_client()
                cor = asyncio.run_coroutine_threadsafe(renk, self.media_client.loop)
                try:
                    cor.result()
                except:
                    pass
                return
            oynatilacak = self.queue.pop(0)
        else:
            oynatilacak = self.repeat
        dans = self.oynat(oynatilacak)
        cor = asyncio.run_coroutine_threadsafe(dans, self.media_client.loop)
        try:
            cor.result()
        except:
            pass

    async def disconnect_client(self):
        self.player = None
        self.queue = []
        await self.client.send_message(self.textchannel, "🎤 Listedeki Tüm Müzikleri Oynattım Bitti. Hadi Ben Çıkıyorum ✋")
        await self.media_client.disconnect()
        self.media_client = None

    def set_channel(self, voicechannel, textchannel):
        self.voicechannel = voicechannel
        self.textchannel = textchannel

    async def oynat(self, url: str):
        if self.media_client is None or not self.media_client.is_connected():
           self.media_client = await self.client.join_voice_channel(self.voicechannel)
        if "&list=" in url:
            url = url.split("&list=")[0]
        self.player = await self.media_client.create_ytdl_player(url, ytdl_options={'default_search': 'ytsearch'}, after=self.play_after)
        self.player.start()
        await self.client.send_message(self.textchannel, f" 🎵 Şuanda Çalıyorum Bak **{self.player.title or self.player.url}** 🎵")

    async def ekle(self, message: discord.Message, url: str):
        await self.client.delete_message(message)
        try:
            bot_member = discord.utils.find(lambda m: m.id == self.client.user.id, message.server.members)
            self.client.server_voice_state(bot_member, mute=False, deafen=True)
        except Exception as ex:
            print(f"Mute/Deafen Hata : {ex}")
        self.repeat = None
        self.queue.append(url)
        self.voicechannel = message.author.voice.voice_channel
        self.textchannel = message.channel
        await self.client.send_message(self.textchannel, f" ➕ Çalınacaklar Listesine Ekledim **{url}** ➕")
        if self.player is None:
            await self.oynat(self.queue.pop(0))
            return
        if self.player.is_done() or not self.player.is_playing():
            await self.oynat(self.queue.pop(0))

    async def gec(self, message: discord.Message):
        await self.client.delete_message(message)
        if self.player is None:
            return
        await self.client.send_message(message.channel, f" ➡ Diğer Müziğe Geç! Bekleme Yapma (**{self.player.title or self.player.url}**) ➡")
        await self.player.stop()
        self.play_after()

    async def durdur(self, message: discord.Message):
        await self.client.delete_message(message)
        if self.media_client is None:
            return
        self.player = None
        self.queue = []
        await self.client.send_message(message.channel, f" ❕ Hoooop! Tamamdır Müzikleri Durdurdum. Odadan da Çıkıyorum :( ❕")
        await self.media_client.disconnect()
        self.media_client = None

    async def tekrarla(self):
        if self.player is None or not self.player.is_playing():
            await self.client.send_message(self.textchannel, "⛔ Hata : Şuanda Hiçbirşey Çalmıyor! ⛔")
            return
        if self.repeat is None:
            self.repeat = self.player.url
            await self.client.send_message(self.textchannel, f"💿 Tekrarlama Başlatıldı (**{self.player.title or self.player.url}**) 💿")
        else:
            self.repeat = None
            await self.client.send_message(self.textchannel, f"📢 Tekrarlama Durduruldu Artık Diğer Müziklerinize Devam Edebilirsiniz 📢")


    async def playlist_goster(self, message: discord.Message):
        await self.client.delete_message(message)
        await self.client.send_typing(message.channel)
        if len(self.queue) < 1:
            await self.client.send_message(message.channel, "Çalma Listesi Boş!")
            return
        playlist_embed = discord.Embed()
        playlist_embed.add_field(name="Çalma Listesi",
                                 value="\n".join(self.queue))
        await self.client.send_message(message.channel, "", embed=playlist_embed)
