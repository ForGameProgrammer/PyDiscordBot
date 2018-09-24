from bs4 import BeautifulSoup
import requests

def parse_9gag_gif(url):
    r = requests.get(url)
    page_html = r.text
    soup = BeautifulSoup(page_html, "html.parser")
    articles = soup.find_all("article")
    next_page = soup.select_one("a.badge-load-more-post")
    print(next_page)
    for article in articles:
        entry = article["data-entry-url"]
        title = article.find("h1").string
        

parse_9gag_gif("https://9gag.com/gif?id=a1Kg4AY%2CaL8oqKW%2CaoOoBZw&amp;c=10")