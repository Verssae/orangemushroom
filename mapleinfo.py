from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import quote, unquote
import discord

        
def get_html(url):
   _html = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      _html = resp.text
   return _html


URL = "http://maplestory.nexon.game.naver.com/MapleStory/Page/Gnx.aspx?Url=Ranking/SearchResult&strCharacter_search=%b9%cc%b8%a3%b6%ed%b9%cc%b8%a3%b6%ed"


class MapleInfo:
    
    def __init__(self, url):
        self.url = url
        self.get_data()
    
    def get_data(self):
        
        html = get_html(self.url)
        soup = BeautifulSoup(html, 'html.parser')
        ranking = soup.find("dl",{"class":"info"})
        avatars = soup.find("dl",{"class":"info"}).find_all("div")
        text = ranking.get_text()
        
        self.avatar = avatars[0].img["src"]
        
        names = text.split()
        self.user_name = names[2][:-1]
        self.job = names[5]
        self.level = names[8]
        self.xp = names[11]
        self.popularity = names[14]
        self.total_ranking = names[17]
        self.world_ranking = names[20]
        self.job_ranking = names[23]
        self.pop_ranking = names[26]
        
        self.world_name = ranking.img['alt']
        self.world_icon = ranking.img['src']
    
    def get_name(self):
        em = discord.Embed(title=self.user_name, color=0xe67e22)
        em.set_image(url=self.avatar)
        return em
    
    def get_info(self):
        text = "경험치: " + self.xp +"\n인기도: " + self.popularity
        em = discord.Embed(title=self.job+" Lv " + self.level, description=text, colour=0xa84300)
        em.set_author(name=self.world_name, icon_url=self.world_icon)
        return em
    def get_ranking(self):
        text = "종합랭킹: " + self.total_ranking + "위\n월드랭킹: " + self.world_ranking + "위\n직업랭킹: " + self.job_ranking + "위\n인기도랭킹: " + self.pop_ranking + "위"
        em = discord.Embed(title="종합랭킹 정보", description=text)
        return em

