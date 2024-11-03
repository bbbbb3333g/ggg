import aiohttp
import asyncio
import os
import requests
from aiogram import Bot, Dispatcher
import json
import config 

mainpath = os.getcwd()

with open(mainpath + '/words.txt', 'r') as f1:
    words = [line.strip().lower() for line in f1.readlines()]
with open(mainpath + '/banned.txt', 'r') as f4:
    banned_steamwords = [line.strip() for line in f4.readlines()]
with open(mainpath + '/claim.txt', 'r') as f6:
    claimwords = [line.strip() for line in f6.readlines()]
alls = claimwords + banned_steamwords

delete = input('delete repeat words?\n yes / no')
if delete == 'yes':
    list(set(words))
    print('repeaters was delete')

y=0
YOUR_CHAT_ID = config.CHATID
YOUR_BOT_TOKEN = config.TOKEN
STEAMAPI = ''
bot = Bot(token=YOUR_BOT_TOKEN) 
s = asyncio.Semaphore(50)
freewords = []
CHARS = 'qweasdzxcrtyfghvbnuiojklmp1234567890_-QWEASDZXCRTYFGHVBNUIOJKLMP'

def clean():
    for word in words:
        for char in word:
            if char not in CHARS:
                print('no', word)
                words.remove(word)
clean()

        
async def claim(claimword):
    try:
        sesid = config.cookies['sessionid']
        sls = config.cookies['steamLoginSecure']
        
        files = [
            ('type', (None, 'profileSave')),
            ('personaName', (None, 'caulg')),
            ('real_name', (None, 'caulo')),
            ('customURL', (None, claimword)),
            ('summary', (None, 't.me/caulo')),
            ('sessionID', (None, sesid)),
            ('json', (None, '1')),  
        ]
        
        response = requests.post(
            'https://steamcommunity.com/profiles/'+sls[:17]+'/edit/',
            cookies=config.cookies,
            files=files,
        )
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=response.text)
        return
    except Exception as e:
        print(e)


async def steam(session, word):
    try:

        if word in alls: 
            return
        if len(word) < 2:
            return
        global y
        async with session.get(f'https://steamcommunity.com/id/{word}') as response:
            html_steam = await response.text()
            response_status = response.status
            if response_status > 400:
                await asyncio.sleep(30)
            else:
                if 'The specified profile could not be found.' in html_steam:
                    if word not in freewords:
                        print(f'STEAM maybe free                    {word}')

                        r = requests.get(f'https://steamcommunity.com/id/{word}')
                        if 'The specified profile could not be found.' in r.text:
                            freewords.append(word)
                            print(f'STEAM free                    {word}')
                            await claim(word)
                            with open(mainpath+r'\claimSteam.txt', 'a') as f5:
                                f5.write(f'{word}\n')
                            await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'steam\t @{word}')
                else:
                    y+=1
                    print(f'{y}\r',end='')

    except Exception as e:
        await asyncio.sleep(30)
        print(e)

async def steamreq(session,word):
    try:
        for word in words:
            async with session.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAMAPI}&vanityurl={word}') as response:
                print(response)
        
    except Exception as e:
        print(e)
        

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for word in words:
                tasks.append(steam(session, word))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
