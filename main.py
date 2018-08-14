import asyncio
import discord
import getpass
from PIL import Image
import requests
from io import BytesIO
from mapleinfo import *
import sqlite3

# database 
username = getpass.getuser()
conn = sqlite3.connect("/Users/"+username+"/Documents/maple.db")
cur = conn.cursor()
sql = """create table if not exists users (
    user text not null,
    url text not null
);"""
cur.execute(sql)
conn.commit()

# ro =cur.execute("select * from users where 1")
# for i in ro:
#     print(i)


client = discord.Client()
token = "NDU5MDU1NDIyNzcxMjk4MzA0.Dgwv6A.TP8JJSqiMCVTbcziYb6VwJFEnGM"

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
    print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    print(client.user.id)
    print("===========")
    # 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
    # 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
    await client.change_presence(game=discord.Game(name="MapleStory | help", type=1))

# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(message):
    if message.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
        return None #동작하지 않고 무시합니다.

    id = message.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.

    if message.content.startswith('!랭킹'): #만약 해당 메시지가 '!커맨드' 로 시작하는 경우에는
        # await client.send_message(channel, url) #봇은 해당 채널에 '커맨드' 라고 말합니다.
        user = message.content[4:]
        if user == None:
            await client.send_message(channel, "!도움 을 입력하세요")
        else:
            sql = "select url from users where user='{}'".format(
                user
            )
            cur.execute(sql)
            rows = cur.fetchall()
            
            if rows == []:
                await client.send_message(channel, "!도움 을 입력하세요")
            else:
                maple = MapleInfo(rows[0][0])
                await client.send_message(channel, embed=maple.get_name())
                await client.send_message(channel, embed=maple.get_info())
                await client.send_message(channel, embed=maple.get_ranking())
        
    # elif message.content.startswith("!도움"):
    #     await client.send_message(channel, "아래 url로 접속하여 닉네임을 검색한 후 그 url을 복사하여 <!등록 닉네임 url> 로 등록하세요\nhttp://rank.maplestory.nexon.com/MapleStory/Page/Gnx.aspx?Url=Ranking/SearchResult&strCharacter_search=%b9%cc%b8%a3%b6%ed%b9%cc%b8%a3%b6%ed")
    
    elif message.content.startswith("!등록"):
        args = message.content.split()
        if len(args) != 3:
            await client.send_message(channel, "!도움 을 입력하세요")
        else:
            sql = "insert into users (user, url) values ('{}', '{}')".format(
                args[1],
                args[2]
            )
            cur.execute(sql)
            conn.commit()
            await client.send_message(channel, "등록완료!\n!랭킹 닉네임 으로 랭킹 검색하세요")

    elif message.content.startswith("!삭제"):
        user = message.content[4:]
        if user == None:
            await client.send_message(channel, "!도움 을 입력하세요")
        else:
            sql = "delete from users where user='{}'".format(
                user
            )
            cur.execute(sql)
            conn.commit()
            await client.send_message(channel, "삭제 완료!")
    
    elif message.content.startswith("!갤러리"):
        
        sql = "select * from users where 1"
        cur.execute(sql)
        rows = cur.fetchall()

        for i in rows:
            maple = MapleInfo(i[1])
            await client.send_message(channel, embed=maple.get_name())
    
    elif message.content.startswith("!도움"):
        text = """
        명령어:
            !랭킹 <닉네임>
            !등록 <닉네임> <url>
            !삭제 <닉네임>
            !갤러리
            !도움
        등록:
            주기적으로 링크가 바뀌니 안될때마다 삭제하고 재등록 바람
            아래 url 접속 -> 닉네임 검색 -> url 복사 -> !등록 <닉네임> <url>
            http://rank.maplestory.nexon.com/MapleStory/Page/Gnx.aspx?URL=Ranking/SearchResult&strCharacter_Search=7EQjvwlmkmqWNFt%2f0NlZhIcS%2bjHSwqWCJLFltl7Hgmrqd2pPWADVKe3CmkxPG9y0aawVAwMXo8wHr5g3MJLVP2kB4kv5E2%2buDHxN3t1AJv0%3d
            버전:
            0.0.1
            """
        await client.send_message(channel, text)


    else: #위의 if에 해당되지 않는 경우
        #메시지를 보낸사람을 호출하며 말한 메시지 내용을 그대로 출력해줍니다.
        # await client.send_message(channel, "<@"+id+">님이 \""+message.content+"\"라고 말하였습니다.")
        pass
client.run(token)