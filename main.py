import aiohttp
import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
import json

mainpath = '/root/ggg'
desktop_path = '/home/your_username/Desktop'

with open(mainpath + '/words.txt', 'r') as f1:
    words = [line.strip().lower() for line in f1.readlines()]
with open(mainpath + '/banned.txt', 'r') as f4:
    banned_steamwords = [line.strip() for line in f4.readlines()]
with open(mainpath + '/Claim.txt', 'r') as f6:
    claimwords = [line.strip() for line in f6.readlines()]
alls = claimwords + banned_steamwords

delete = input('delete repeat words?\n yes / no')
if delete == 'yes':
    list(set(words))
    print('repeaters was delete')

YOUR_CHAT_ID = ''
YOUR_BOT_TOKEN = 2
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

        
async def claim(claimWord):
    with open(mainpath+'accounts.json', 'r') as f:
        acc = json.load(f)
    
    for i in range(0,50):
        sesid = acc[f"{i}"]["sessionid"]
        sls = acc[f"{i}"]["steamLoginSecure"]
        print(sesid)

        cookies = {
            'sessionid': sesid,
            'steamLoginSecure': sls,
        }

        files = [
            ('type', (None, 'profileSave')),
            ('personaName', (None, 'caulg')),
            ('real_name', (None, 'caulo')),
            ('customURL', (None, claimWord)),
            ('summary', (None, 't.me/caulo')),
            ('sessionID', (None, sesid)),
            ('json', (None, '1')),  
        ]
        response = requests.post(
            'https://steamcommunity.com/profiles/'+sls[:17]+'/edit/',
            cookies=cookies,
            files=files,
        )
        return


async def steam(session, word):
    try:
        async with s:

            if word in alls: 
                return
            if len(word) < 2:
                return
            
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
                                with open(mainpath+r'\ClaimSteam.txt', 'a') as f5:
                                    f5.write(f'{word}\n')
                                await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'steam\t @{word}')
                    else:
                        print(f'STEAM {word} ', response_status)

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


