import json
from MusicClient import MusicPlayer
import datetime
import discord
import random
import requests
import urllib
import asyncio
import time
from discord import opus
from bs4 import BeautifulSoup



client = discord.Client()
champions = []
media_players = {}
play_list = {}
media_clients = {}
music_clients = {}
kullanici_komutlari = []

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))

def find_my_channel(channel_id):
    for channel in client.get_all_channels():
        if channel.id == channel_id:
            return channel
    return None

def KomutEkle(kullaniciId: str, kullaniciKomutlari: list, kullaniciMesajlari: list, mention: bool):
    eklenecek_komut = {
        "id": kullaniciId,
        "komutlar": kullaniciKomutlari,
        "mesajlar": kullaniciMesajlari,
        "mention": mention,
        "last" : 0
    }
    kullanici_komutlari.append(eklenecek_komut)


def app():
    client.run(data["token"])


def getRasgeleCevap():
    answer_list = [
        #Olumlu
        "Anladığım Kadarı ile Evet",
        "Kesin Zaten",
        "Kesinlikle Öyle",
        "Büyük İhtimal",
        "Olabilir",
        "İşaretler Evet'i Gösteriyor",
        "Şüphesiz",
        "Evet",
        "Evet Kesinlikle",
        "Evet Güvenebilirsin",

        #Kararsız
        "Cevap Bulanık, Tekrar Sor",
        "Daha Sonra Tekrar Sor",
        "Şuan Söylememem Daha İyi",
        "Şuanda Kestiremiyorum",
        "Odaklan Ve Tekrar Sor",

        #Olumsuz
        "Buna Bel Bağlama",
        "Hayır",
        "Kaynaklarım Hayır Diyor",
        "Olmayabilir",
        "Çok Süpheli"
    ]
    return random.choice(answer_list)


def parse_9gag_gif(url):
    r = requests.get(url)
    page_html = r.text
    soup = BeautifulSoup(page_html, "html.parser")
    articles = soup.find_all("article")
    gags = []
    next_page = soup.select_one("a.badge-load-more-post")
    print(next_page)
    for article in articles:
        entry = article["data-entry-url"]
        title = article.find("h1").string
        gags.append({"url": entry, "title": title})
    return gags


@client.async_event
async def on_ready():
    print('Bot Started as : ')
    print(client.user.name)
    print(client.user.id)
    game = discord.Game(name="Yardım için !komutlar")
    await client.change_presence(game=game)
    print('------')
    load_opus_lib()
 


@client.async_event
async def on_member_join(member: discord.Member):
    '''
    if member.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Sunucuya Katıldı", colour=discord.Colour.blue, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{member.name}#{member.discriminator}",url=member.avatar_url)
        kayit_embed.set_thumbnail(url=member.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Kullanıcı", value=f"{member.name}#{member.discriminator}")
        kayit_embed.add_field(name="Hesap Oluşturma Tarihi", value=f"{member.created_at}")
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{member.id}")
    
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)
    '''
    if member.server.id == data["PaKunSunucu"]:
        await client.send_message(member, """
        Pa Kun Sunucusuna Hoş Geldin :blush: 

        Turnuva Amaçlı Geldiysen Eğer Sunucudaki Chat'e Takım Adınızı ve Kaptanınızı Yazmayı Unutma Lütfen

        İyi Vakit Geçirmen Dileği ile... :hugging: 
        """)

@client.async_event
async def on_member_remove(member: discord.Member):
    '''
    if member.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Sunucudan Ayrıldı", colour=0xBDBDBD, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{member.name}#{member.discriminator}",url=member.avatar_url)
        kayit_embed.set_thumbnail(url=member.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Kullanıcı", value=f"{member.name}#{member.discriminator}")
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{member.id}")
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)
    '''
    

@client.async_event
async def on_member_ban(member: discord.Member):
    
    '''if member.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Banlandı!", colour=0xFE2E2E, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{member.name}#{member.discriminator}",url=member.avatar_url)
        kayit_embed.set_thumbnail(url=member.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Kullanıcı", value=f"{member.name}#{member.discriminator}")
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{member.id}")
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''
    


@client.async_event
async def on_message_edit(before: discord.Message, after: discord.Message):
    
    '''if after.author.server.id == data["YuruyenBaseSunucu"]:
        if not before or not after:
            return
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Mesaj Değiştirildi", colour=0xF7FE2E, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{after.author.name}#{after.author.discriminator}",url=after.author.avatar_url)
        kayit_embed.set_thumbnail(url=after.author.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Kullanıcı", value=f"{after.author.name}#{after.author.discriminator}")
        kayit_embed.add_field(name="Kanal", value=f"{after.channel.mention}")
        kayit_embed.add_field(name="Önceki Mesaj", value=before.content)
        kayit_embed.add_field(name="Değiştirilen Mesaj", value=after.content)
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{after.author.id}")
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''
    

@client.async_event
async def on_message_delete(message: discord.Message):
    
    '''if message.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Mesaj Silindi", colour=0x8A0808, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",url=message.author.avatar_url)
        kayit_embed.set_thumbnail(url=message.author.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Mesajı Silinen Kullanıcı", value=f"{message.author.name}#{message.author.discriminator}")
        kayit_embed.add_field(name="Kanal", value=f"{message.channel.mention}")
        kayit_embed.add_field(name="Silinen Mesaj", value=message.content)
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{message.author.id}")
        print(kayit_embed)

        await client.send_message(kayit_channel, "", embed=kayit_embed)'''


@client.async_event
async def on_channel_delete(channel_updated: discord.Channel):
    
    '''if channel_updated.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Kanal Silindi", colour=0xFF0000, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{channel_updated.name}",url=channel_updated.server.icon)
        kayit_embed.set_thumbnail(url=channel_updated.server.icon)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        print(kayit_embed)
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''
    


@client.async_event
async def on_channel_create(channel_updated: discord.Channel):
    
    '''if channel_updated.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Kanal Oluşturuldu", colour=0x64FE2E, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{channel_updated.mention}",url=channel_updated.server.icon)
        kayit_embed.set_thumbnail(url=channel_updated.server.icon)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        print(kayit_embed)
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''
    


@client.async_event
async def on_channel_update(channel: discord.Channel, after: discord.Channel):
    
    '''if channel.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_embed = discord.Embed(title="Kanal Değiştirildi", colour=0x5882FA, timestamp=datetime.datetime.utcnow())
        kayit_embed.set_author(name=f"{channel.mention}",url=channel.server.icon)
        kayit_embed.set_thumbnail(url=channel.server.icon)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        print(kayit_embed)
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''


@client.async_event
async def on_voice_state_update(before: discord.Member, after: discord.Member):
    
    '''if after.server.id == data["YuruyenBaseSunucu"]:
        kayit_channel = find_my_channel(data["YuruyenBaseKayitlar"])
        kayit_title = ""
        kanal = ""
        if before.voice.voice_channel != after.voice.voice_channel:
            if before.voice.voice_channel:
                kayit_title = "Kullanıcı Konuşmadan Ayrıldı"
                kanal = f"{before.voice.voice_channel.mention}"
            if after.voice.voice_channel:
                kayit_title = "Kullanıcı Konuşmaya Katıldı"
                kanal = f"{after.voice.voice_channel.mention}"
            if before.voice.voice_channel and after.voice.voice_channel:
                kayit_title = "Kullanıcı Konuşma Odası Değiştirdi"
                kanal = f"{before.voice.voice_channel.mention} -> {after.voice.voice_channel.mention}"
        else:
            if before.voice.self_mute != after.voice.self_mute:
                if before.voice.self_mute:
                    kayit_title = "Kullanıcı Kendi Mikrofonunu Açtı"
                else:
                    kayit_title = "Kullanıcı Kendi Mikrofonunu Kapadı"
                
            if before.voice.mute != after.voice.mute:
                if before.voice.mute:
                    kayit_title = "Kullanıcının Mikrofonu Açıldı"
                else:
                    kayit_title = "Kullanıcının Mikrofonu Kapatıldı"
            
            if before.voice.self_deaf != after.voice.self_deaf:
                if before.voice.self_deaf:
                    kayit_title = "Kullanıcı Kendi Kulaklığını Açtı"
                else:
                    kayit_title = "Kullanıcı Kendi Kulaklığını Kapadı"
                    
            if before.voice.deaf != after.voice.deaf:
                if before.voice.deaf:
                    kayit_title = "Kullanıcının Kulaklığı Açıldı"
                else:
                    kayit_title = "Kullanıcının Kulaklığı Kapatıldı"

        kayit_embed = discord.Embed(title=kayit_title, colour=0xCC2EFA, timestamp=datetime.datetime.utcnow())

        if len(kanal) > 0:
            kayit_embed.add_field(name="Kanal", value=kanal)

        kayit_embed.set_author(name=f"{after.name}#{after.discriminator}",url=after.avatar_url)
        kayit_embed.set_thumbnail(url=after.avatar_url)
        kayit_embed.set_footer(text=f"@ForGamerBot",icon_url=discord.Embed.Empty)
        kayit_embed.add_field(name="Kullanıcı", value=f"{after.name}#{after.discriminator}")
        kayit_embed.add_field(name="Kullanıcı ID'si", value=f"{after.id}")
        print(kayit_embed)
        
        await client.send_message(kayit_channel, "", embed=kayit_embed)'''
        


@client.async_event
async def on_message(message: discord.Message):
    print(message.author.id, ":", message.author.name, ", Server :",
          message.server, "->", message.channel, ", Mesaj :", message.content)
    if message.channel.is_private and message.author.id != data["forgamer"] and message.author.id != client.user.id:
        forgamer = await client.get_user_info(data["forgamer"])
        await client.send_message(forgamer, f"Bot Received Message : {message.author.name}#{message.author.discriminator} -> {message.content}")
    if message.content.startswith(command_constant):
        cmds = message.content[len(command_constant):].split(" ")
        cmd = cmds[0].lower()
        args = []
        if len(cmds) > 1:
            args = cmds[1:]
        await on_command(cmd, args, message)
    if message.channel.id == "455513338445692938":
        if "@everyone" in message.content:
            await client.delete_message(message)



async def on_command(command: str, args: list, message: discord.Message):
    print("Command : ", command, args, message)
    """
    if message.server.id == data["YuruyenBaseSunucu"]:
        role = message.author.top_role
        permissions = role.permissions
        print(message.channel.id)
        if message.channel.id != "316657125067587584" and not permissions.administrator and message.author.id != data["forgamer"]:
            return
    """

    help_commands = ["help", "yardım", "yardim", "komut", "komutlar"]
    if command in help_commands:
        embed_help = discord.Embed()
        embed_help.add_field(name="!help !yardım !komutlar",
                             value="Komutlar Listesi ve Kullanımı")
        embed_help.add_field(name="!davet !invite !botlink",
                             value="Beni Discorduna Eklemen İçin Gereken Link")
        embed_help.add_field(name="!sor !soru !8ball",
                             value="Kullanımı : '!sor <soru>' şeklinde. Cevabı 'Evet' veya 'Hayır' Olan Soruları Yanıtlar")
        embed_help.add_field(name="!avatar !resim !pp",
                             value="Profil Resmini Büyük Şekilde Chat'e Gönder")
        embed_help.add_field(name="!rastgele !random",
                             value="Sayı vermezseniz 1 ile 100 arasında Sayı verirseniz Verdiğiniz iki sayı arasında Rastgele Sayı Üretir")
        embed_help.add_field(
            name="!gif !giphy", value="Kullanımı : '!gif <Aranacak Gif>' şeklinde. Gif'ler içinde Arar ve İngilizce (Giphy)")
        embed_help.add_field(name="!rastgelegif !randomgif",
                             value="Kullanımı : '!randomgif' şeklinde. Gif'ler içinden Rastgele Gif Getirir (Giphy)")
        embed_help.add_field(
            name="!9gag !gag", value="Kullanımı : '!9gag <Arama>' şeklinde. 9GaG'den Arama (Bozuk Olabilir Bu Aralar)")
        embed_help.add_field(name="!dolar !euro !sterlin",
                             value="Sayı Vermezseniz 1 Döviz Türü Sayı Verirseniz O Sayı Kadar Döviz Türünü TL ye Çevirir. Sürekli Günceldir")
        embed_help.add_field(name="!sil !delete !purge",
                             value="Kullanımı : '!sil <Sayı>' şeklinde. Girilen Sayı kadar Mesajı o Kanaldan Siler. Admin yada Mesaj Silme Yetkisine Sahip Olunması Gerekir")
        embed_help.add_field(name="!sihirdar !summoner !lol",
                             value="Kullanımı : '!sihirdar <Sihirdar İsmi>' şeklinde. Girilen Sihirdar'ın Bilgilerini Getirir (TR Serverı)")
        embed_help.add_field(name="!çal !müzik !play",
                             value="Kullanımı : '!çal <Aranacak Müzik yada Youtube URL>' şeklinde. Odaya Katlıp Aranacak Müziği Yada Youtube Linkini Çalar. Zaten Çalıyorsa Listeye Ekler")
        embed_help.add_field(name="!dur !kapat !stop",
                             value="Çalanı Durdur Odadan Ayrıl :(")
        embed_help.add_field(name="!geç !atla !skip",
                             value="Çalan Müziği Atla")
        embed_help.add_field(name="!liste !list !playlist",
                             value="Çalma Listesi - Playlist")
        embed_help.add_field(name="!tekrarla !tekrar !repeat",
                             value="Çalan Şarkıyı Sürekli Tekrarla / Durdur")
        await client.send_message(message.channel, "", embed=embed_help)

    davet_commands = ["davet", "invite", "davetlinki",
                      "invitelink", "botlink", "botinvite", "botdavet"]
    if command in davet_commands:
        await client.send_message(message.author, "Bu Botu Davet Etme Linki : {link}".format(link=data["davet-url"]))

    avatar_commands = ["avatar", "resim", "pp"]
    if command in avatar_commands:
        await client.send_typing(message.channel)
        resim = discord.Embed()
        resim.set_image(url=message.author.avatar_url)
        await client.send_message(message.channel, embed=resim)

    soru_commands = ["sor", "soru", "8ball", "cevap", "cevapla"]
    if command in soru_commands:
        await client.send_typing(message.channel)
        rasgele_cevap = getRasgeleCevap()
        await client.send_message(message.channel, f"🔮 {rasgele_cevap} {message.author.mention}")

    rasgele_commands = ["rasgele", "rastgele", "rnd", "random"]
    if command in rasgele_commands:
        await client.send_typing(message.channel)
        sayi1 = 1
        sayi2 = 100
        if len(args) > 1:
            sayi1 = int(args[0])
            sayi2 = int(args[1])
        sayi = random.randint(sayi1, sayi2)
        await client.send_message(message.channel, "🎲 Senin İçin Rasgele Sayım {author} : {sayi}".format(sayi=sayi, author=message.author.mention))

    gif_commands = ["gif", "giphy"]
    if command in gif_commands:
        if len(args) < 1:
            return
        await client.send_typing(message.channel)
        gif_search = urllib.parse.quote(" ".join(args))
        gif_url = "https://api.giphy.com/v1/gifs/search?api_key={api}&q={q}&limit=20&offset=0&rating=G&lang=tr".format(
            api=data["giphy-api"], q=gif_search)
        gif_req = requests.get(gif_url)
        gif_json = gif_req.json()
        gif = random.choice(gif_json["data"])
        await client.send_message(message.channel, "{gif}".format(gif=gif["images"]["original"]["url"]))

    random_gif_commands = ["randomgif", "rasgelegif",
                           "rastgelegif", "gifrasgele", "gifrastgele"]
    if command in random_gif_commands:
        await client.send_typing(message.channel)
        gif_search = urllib.parse.quote(" ".join(args))
        gif_url = "https://api.giphy.com/v1/gifs/random?api_key={api}&tag=&rating=G".format(
            api=data["giphy-api"])
        gif_req = requests.get(gif_url)
        gif_json = gif_req.json()
        gif = gif_json["data"]["image_original_url"]
        await client.send_message(message.channel, "{gif}".format(gif=gif))

    gag_commands = ["9gag", "gag"]
    if command in gag_commands:
        await client.send_typing(message.channel)
        gag_url = "https://9gag.com/hot"
        if len(args) > 0:
            gag_url = "https://9gag.com/search?query={q}".format(
                q=urllib.parse.quote(" ".join(args)))
        gags = parse_9gag_gif(gag_url)
        if len(gags) < 1:
            await client.send_message(message.channel, "Aranılan Sonuç 9Gag'de Bulunamadı")
            return
        gag = gags[0]
        title = gag["title"]
        gag_link = gag["url"]
        await client.send_message(message.channel, "{title} : {gag_link}".format(title=title, gag_link=gag_link))

    mesaj_commands = ["mesaj", "message", "ozel"]
    if command in mesaj_commands and len(args) > 1:
        mentions = message.mentions
        if len(mentions) != 1:
            await client.send_message(message.channel, "1 Kişiyi Etiketlemen Gerekiyor")
            return
        await client.delete_message(message)
        user = mentions[0]
        message_to_send = " ".join(args[1:])
        await client.send_message(user, "{to} : {msg}".format(to=message.author.name, msg=message_to_send))
        await client.send_message(message.author, "Mesajınız Gönderildi. Message Sent. {to} : {msg}".format(to=user.name, msg=message_to_send))

    dolar_commands = ["dolar", "USD", "$"]
    if command in dolar_commands:
        await client.send_typing(message.channel)
        sayi = 1
        if len(args) > 0:
            sayi = float(args[0])
        doviz_req = requests.get(url=data["doviz-url"])
        doviz_json = doviz_req.json()
        oran = 0
        for doviz in doviz_json:
            if doviz["code"] == "USD":
                oran = float(doviz["selling"])
                break
        sonuc = oran * sayi
        ters = sayi / oran
        await client.send_message(message.channel, "{sayi} Dolar = {sonuc:.3f} TL\n{sayi} TL = {ters:.3f} Dolar".format(sayi=sayi, sonuc=sonuc, ters=ters))

    euro_commands = ["euro", "eur", "€", "avro"]
    if command in euro_commands:
        await client.send_typing(message.channel)
        sayi = 1
        if len(args) > 0:
            sayi = float(args[0])
        doviz_req = requests.get(url=data["doviz-url"])
        doviz_json = doviz_req.json()
        oran = 0
        for doviz in doviz_json:
            if doviz["code"] == "EUR":
                oran = float(doviz["selling"])
                break
        sonuc = oran * sayi
        ters = sayi / oran
        await client.send_message(message.channel, "{sayi} Euro = {sonuc:.3f} TL\n{sayi} TL = {ters:.3f} Euro".format(sayi=sayi, sonuc=sonuc, ters=ters))

    sterlin_commands = ["gbp", "sterlin"]
    if command in sterlin_commands:
        await client.send_typing(message.channel)
        sayi = 1
        if len(args) > 0:
            sayi = float(args[0])
        doviz_req = requests.get(url=data["doviz-url"])
        doviz_json = doviz_req.json()
        oran = 0
        for doviz in doviz_json:
            if doviz["code"] == "GBP":
                oran = float(doviz["selling"])
                break
        sonuc = oran * sayi
        ters = sayi / oran
        await client.send_message(message.channel, "{sayi} Sterlin = {sonuc:.3f} TL\n{sayi} TL = {ters:.3f} Sterlin".format(sayi=sayi, sonuc=sonuc, ters=ters))

    yen_commands = ["yen", "jpy"]
    if command in yen_commands:
        await client.send_typing(message.channel)
        sayi = 1
        if len(args) > 0:
            sayi = float(args[0])
        doviz_req = requests.get(url=data["doviz-url"])
        doviz_json = doviz_req.json()
        oran = 0
        for doviz in doviz_json:
            if doviz["code"] == "JPY":
                oran = float(doviz["selling"])
                break
        sonuc = oran * sayi
        ters = sayi / oran
        await client.send_message(message.channel, "{sayi} Yen = {sonuc:.3f} TL\n{sayi} TL = {ters:.3f} Yen".format(sayi=sayi, sonuc=sonuc, ters=ters))

    kore_won_commands = ["won", "krw"]
    if command in kore_won_commands:
        await client.send_typing(message.channel)
        sayi = 1
        if len(args) > 0:
            sayi = float(args[0])
        doviz_req = requests.get(url=data["doviz-url"])
        doviz_json = doviz_req.json()
        oran = 0
        for doviz in doviz_json:
            if doviz["code"] == "KRW":
                oran = float(doviz["selling"])
                break
        sonuc = oran * sayi
        ters = sayi / oran
        await client.send_message(message.channel, "{sayi} Güney Kore Won = {sonuc:.3f} TL\n{sayi} TL = {ters:.3f} Güney Kore Won".format(sayi=sayi, sonuc=sonuc, ters=ters))

    for komutlar in kullanici_komutlari:
        if command in komutlar["komutlar"]:
            if (time.time() - komutlar["last"]) < data["delay"]:
                return
            await client.send_typing(message.channel)
            kullanici = await client.get_user_info(komutlar["id"])
            rnd_mesaj = random.choice(komutlar["mesajlar"])
            if komutlar["mention"]:
                rnd_mesaj += " " + kullanici.mention
            await client.send_message(message.channel, rnd_mesaj)
            komutlar["last"] = time.time()

    purge_commands = ["purge", "delete", "sil", "mesajsil"]
    if command in purge_commands:
        role = message.author.top_role
        permissions = role.permissions
        if not permissions.manage_messages and not permissions.administrator and message.author.id != data["forgamer"]:
            return
        if len(args) < 1:
            await client.send_message(message.channel, "Doğru Kullanım : !komut sayı")
            return
        sayi = int(args[0])
        if sayi < 0:
            return
        await client.send_typing(message.channel)
        await client.purge_from(message.channel, limit=sayi + 1)
        msg = await client.send_message(message.channel, "{adet} Adet Mesaj Silindi! 👍".format(adet=sayi))
        await client.wait_for_message(timeout=10)
        await client.delete_message(msg)

    mastery_commands = ["summoner", "sihirdar", "lol"]
    if len(args) >= 1 and command in mastery_commands:
        await client.send_typing(message.channel)
        summoner_name_raw = " ".join(args)
        summoner_name = urllib.parse.quote(summoner_name_raw)
        summoner_url = data["summoner-url"].format(
            summoner=summoner_name, api=data["riot-api-key"])
        summoner_req = requests.get(url=summoner_url, headers={
                                    'User-agent': 'ForGamerDiscordBot v0.1'})
        if summoner_req.status_code == 429:
            await client.send_message(message.channel, "Riot Api Limitine Ulaşıldı :/ . {sn} Saniye Sonra Tekrar Deneyin".format(sn=summoner_req.headers["Retry-After"]))
            return
        if summoner_req.status_code != 200:
            await client.send_message(message.channel, "Sihirdar Bulunamadı yada Bir Hata Oluştu. Hata Kodu : {}".format(summoner_req.status_code))
            return
        summoner_level = summoner_req.json()["summonerLevel"]
        summoner_id = summoner_req.json()["id"]
        mastery_url = data["mastery-url"].format(
            id=summoner_id, api=data["riot-api-key"])
        mastery_req = requests.get(url=mastery_url, headers={
                                   'User-agent': 'ForGamerDiscordBot v0.1'})
        if mastery_req.status_code == 429:
            await client.send_message(message.channel, "Riot Api Limitine Ulaşıldı :/ . {sn} Saniye Sonra Tekrar Deneyin".format(sn=mastery_req.headers["Retry-After"]))
            return
        masteries = mastery_req.json()
        top_champions = list()
        for mastery in masteries[:3]:
            champion = None
            for champ in champions:
                if champions[champ]["id"] == mastery["championId"]:
                    champion = champions[champ]
                    break
            if champion is None:
                continue
            top_champions.append("{champ} Puan : {points:,}".format(
                champ=champion["name"], points=int(mastery["championPoints"])))

        rank_url = data["rank-url"].format(id=summoner_id,
                                           api=data["riot-api-key"])
        rank_req = requests.get(url=rank_url, headers={
            'User-agent': 'ForGamerDiscordBot v0.1'})

        msg = discord.Embed()
        msg.set_thumbnail(
            url=data["summoner-icon-url"].format(summonername=summoner_name))
        msg.add_field(name="League Of Legends Sihirdar Bilgi", value="{summoner} İsimli Sihirdarın Sihirdar Seviyesi : {level}".format(
            summoner=summoner_name_raw, level=summoner_level))
        msg.add_field(name="{summoner} En Çok Puana Sahip Olduğu Şampiyonlar".format(
            summoner=summoner_name_raw), value="\n".join(top_champions))
        if rank_req.ok:
            ranks = rank_req.json()
            for rank in ranks:
                rank_type = rank["queueType"]
                if rank_type == "RANKED_FLEX_TT":
                    rank_type = "Ranked 3v3"
                elif rank_type == "RANKED_SOLO_5x5":
                    rank_type = "Ranked SoloQ"
                elif rank_type == "RANKED_FLEX_SR":
                    rank_type = "Ranked Flex"
                rank_tier = rank["tier"]  # Bronze/Silver/Gold/Plat/Diamond...
                rank_num = rank["rank"]  # I, II, III, IV, V
                rank_lp = rank["leaguePoints"]
                msg.add_field(name=rank_type, value="{tier} {rank} {lp}LP".format(
                    tier=rank_tier, rank=rank_num, lp=rank_lp))
        await client.send_message(message.channel, embed=msg)

    

    cal_commands = ["çal", "cal", "oynat", "play", "müzik", "muzik"]
    if command in cal_commands:
        if len(args) < 1:
            return
        youtube_url = " ".join(args)
        if not message.server.id in music_clients:
            music_clients[message.server.id] = MusicPlayer(
                client, message.author.voice.voice_channel, message.channel)
        await music_clients[message.server.id].ekle(message, youtube_url)
        # await ekle(message, youtube_url)

    stop_commands = ["kapat", "durdur", "stop", "dur"]
    if command in stop_commands:
        if not message.server.id in music_clients:
            return
        await music_clients[message.server.id].durdur(message)
        # await durdur(message)

    skip_commands = ["skip", "gec", "ilerle", "atla", "geç"]
    if command in skip_commands:
        if not message.server.id in music_clients:
            return
        await music_clients[message.server.id].gec(message)
        # await gec(message)

    playlist_commands = ["liste", "playlist",
                         "list", "çalanlar", "çalmalistesi"]
    if command in playlist_commands:
        if not message.server.id in music_clients:
            return
        await music_clients[message.server.id].playlist_goster(message)

    repeat_commands = ["tekrarla", "tekrar", "repeat", "döngü"]
    if command in repeat_commands:
        if not message.server.id in music_clients:
            return
        await music_clients[message.server.id].tekrarla()

    sor2_commands = ["sor2", "soru2", "cevap2"]
    if command in sor2_commands:
        await client.send_typing(message.channel)
        req = requests.get(url=data["yesno"], headers={
                                    'User-agent': 'ForGamerDiscordBot v0.1'})
        sonuc = req.json()
        cevap_gif = sonuc["image"]
        cevap_text = sonuc["answer"]
        cevap_yazi = {
            "yes" : "Evet",
            "no" : "Hayır",
            "maybe" : "Belki"
        }
        await client.send_message(message.channel, f"{cevap_yazi[cevap_text]} \n{cevap_gif}")

    #-------------------FORGAMER'A ÖZEL-------------------
    if message.author.id != data["forgamer"]:
        return   

    #ÖZELLLLLL
    ozel_commands = ["ozel", "özel", "taşı", "tasi"]
    if command in ozel_commands:
        userid = args[0]
        serverid = args[1]
        channelid = args[2]

        serverToChange =  client.get_server(serverid)
        memberToChange =  serverToChange.get_member(userid)
        channelToChange =  serverToChange.get_channel(channelid)
        await client.move_member(memberToChange,channelToChange)
    #ÖZELLLLLL

    server_list_commands = ["servers", "serverlar", "sunucular", "serverlist"]
    if command in server_list_commands:
        forgamer = await client.get_user_info(data["forgamer"])
        server_list = client.servers
        server_messages = list()
        for srv in server_list:
            server_messages.append(f"Name : {srv.name}\n ID : {srv.id}")
        server_messages.append(f"Sunucu Sayısı : {server_list.count()}")
        await client.send_message(forgamer, "\n\n".join(server_messages))

    server_invite_commands = ["serverinvite", "sunucudavet"]
    if command in server_invite_commands:
        if len(args) < 1:
            return
        forgamer = await client.get_user_info(data["forgamer"])
        srv_id = args[0]
        server_list = client.servers
        for srv in server_list:
            if srv.id == srv_id:
                server_invite = ""
                try:
                    server_invite = await client.create_invite(destination=list(srv.channels)[0], unique=False, max_age=0, max_uses=0, temporary=False)
                except Exception as ex:
                    server_invite = f"{srv.name} X Hata : {ex}"
                await client.send_message(forgamer, server_invite)
                break

def komutlar():
    KomutEkle(
        data["forgamer"],
        ["forgamer"],
        ["**Unluckiest Man Alive**", "**The Flash**"],
        False
    )
    KomutEkle(
        data["cemal"],
        ["cemal", "yasuo", "hasaki"],
        ["Klik or Dont Klik işte bütün mesele bu",
            "Azir Azir, Kader Bize Ne Yazir?", "Selam Sana Yasuo",
             "Azir mi Banlama GG?", "Hangi Rima? ŞURİMA"],
        True
    )
    KomutEkle(
        data["saksıta"],
        ["saksıta", "saks1ta", ".saks1ta", "berkehan", "tachanga", "paçanga"],
        ["**'Vatanseverlik Zafere Yol Açar'**"],
        True
    )
    KomutEkle(
        data["kefo"],
        ["kefo", "kefaret", "yürüyenkefaret"],
        ["AĞLA KEFO", "KES LAN KEFO"],
        True
    )
    KomutEkle(
        data["niyazi"],
        ["niyazi", "darari", "nyzi", "nyziklcu"],
        ["Selam Sana Discord'un En Darari İnsanı :D",
         "Adam Gibi Adam Beee",
         "Darari Darari Darari Darari",
         "Discord'un Adam Gibi Adamı.",
         "Arkadaşın, Dostun Dibi Behh Adam behh",
         "Enn Vayyy Ziiii EnVayZi EnVayZi",
         "Darari Dariyi Bırakmış Dayayi Dayayi",
         "Kanka Naber Ya"],
        True
    )
    KomutEkle(
        data["pakun"],
        ["pakun", "pa-kun", "pa", "polis"],
        ["Pa-Chan",
         "Ka-Pun", "Pa Pa Pa... Pa-Kun", "Pa-San", "Pa-Sama"],
        False
    )
    KomutEkle(
        data["squirtle"],
        ["skörtıl", "sükörtıl", "squirtle", "skortil"],
        ["Bir Skörtıl Gördüm Sanki... Evet evet hemde Support Squirtle :)"],
        True
    )
    KomutEkle(
        data["zekihoca"],
        ["hoca", "shurima", "yaşasın", "yasasin", "zekihoca"],
        ["Bestest Engurish Ticher Eva", "Azir 1.si Hocaların En iyisi", "Shurima Efendisi", "Shurima Padişahı", "Shurima İmparatorun Geri Döndü"],
        False
    )
    KomutEkle(
        data["cmkaizen"],
        ["kaizen", "cmkaizen", "kurt"],
        ["AUUUUUUUUUUUU", "GURT GIZDI", "Hırrr!"],
        True
    )
    KomutEkle(
        data["civcivfatih"],
        ["fatih", "civciv"],
        [":frowning2:", ":frowning:",":disappointed_relieved:"],
        True
    )
    KomutEkle(
        data["burcak"],
        ["burcak", "burçak", "mârul","marul"],
        ["Marul Sevsin Seni", "Herşeye Marul Olma",
        "Al Marul, Kültürlen...", "Marulun Faydaları?"],
        True
    )

if __name__ == "__main__":

    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    command_constant = data["command"]
    champions_url = data["champion-url"].format(api=data["riot-api-key"])
    champions_req = requests.get(url=champions_url, headers={
                                 'User-agent': 'ForGamerDiscordBot v0.1'})
    if champions_req.status_code == 429:
        print("Şampiyonlar İçin Çok Fazla Request... Kalan Sn:{sn}".format(
            sn=champions_req.headers["Retry-After"]))
    if champions_req.status_code != 200:
        print("Şampion Data : {}".format(champions_req))
    if champions_req.ok:
        champions = champions_req.json()["data"]
    komutlar()
    app()
    
