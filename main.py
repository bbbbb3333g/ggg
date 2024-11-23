from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors.rpcerrorlist import UsernamePurchaseAvailableError, ChannelsAdminPublicTooMuchError,ChannelInvalidError,ChatAdminRequiredError,UsernameInvalidError,UsernameOccupiedError,UsernamePurchaseAvailableError,UsernameNotOccupiedError
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.sync import TelegramClient
from telethon import functions, types
from aiogram import Bot
from time import sleep
import time, random, aiogram, asyncio, os, aiohttp
import config
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
from threading import Timer
import traceback

tasks = [] 
mainpath = os.getcwd()
stop=False 
words = config.words
YOUR_BOT_TOKEN = config.YOUR_BOT_TOKEN
YOUR_CHAT_ID = config.YOUR_CHAT_ID
channels = config.channels
alls = config.alls
bot = Bot(token=YOUR_BOT_TOKEN)
waitlist, freewords, claimlist,taski = [],[],[],[]
semaphoreU,semaphoreQ = asyncio.Semaphore(1),asyncio.Semaphore(1) 
channels=[]
y=0
mainpath=os.getcwd()
print('Время запуска:', time.strftime("%H:%M"))
print('Список запрещенных слов: ',len(alls),'\nВсего слов:',len(words))

async def telegram(word,session,client):

    if len(word) <= 4:
        return

    if word in alls:  
        return

    if not word[0].isalpha():
        words.remove(word)
        return
  
    
    try:

            async with session.get(f'https://t.me/{word}',headers=config.theaders) as response:
                text = await response.text()

                await checktelegram(word,text,session,client)

    except Exception as e:
        print('telegram',e)
        return
    pass
 
async def checktelegram(word,text,session,client):
    try:
        if 'tgme_page_extra' in text:
            #print('\nзанято @'+word)
            global y
            y+=1
            print(f"\r{y}", end="")
            return
        else:
            waitlist.append(word)
                
            if waitlist[1]:
                await fragment_query(waitlist[1], text, session, client)
                #del waitlist[1]
            if waitlist[0]:
                await fragment_username(waitlist[0], text, session, client)
                #del waitlist[0]     
    except IndexError as e:
        return
async def fragment_query(word,text,session,client):
    try:   
        async with semaphoreQ:
            async with session.get(f'https://fragment.com/?query='+word, headers=config.fheaders,cookies=config.fcookies) as response:
                text = await response.text()
                res = await username(waitlist[1],text,response.history,client)
                del waitlist[1]
                print(res)
                if res == 1:
                    print('wait 10')
                    return
                if res == 2:
                    print('520')
                    return

    except IndexError as r:
        #print('index error2 ',waitlist)
        return
    except Exception as e:
        print('fragment222',e,word)
        return

async def fragment_username(word,text,session,client):
    try:   
        async with semaphoreU:
            async with session.get(f'https://fragment.com/username/'+word, headers=config.fheaders,cookies=config.fcookies) as response:
                text = await response.text()
                res = await Fusername(waitlist[0],text,response.history,client)
                del waitlist[0]
                print(res)
                if res == 1:
                    print('1')
                    return
                if res == 2:
                    print('520') 
                    return
                
    except IndexError as r:
        #print('index error1 ',waitlist)
        return
    except Exception as e:
        print('fragment333',e,word)

async def Fusername(word,text,r,client):
    try:
        soup = BeautifulSoup(text, "html.parser")
        sales = soup.find('div', class_='table-cell-value tm-value tm-status-unavail')
        taken = soup.find('span', class_='tm-section-header-status tm-status-taken')
        avail = soup.find('span', class_='tm-section-header-status tm-status-avail')
        sold = soup.find('span', class_='tm-section-header-status tm-status-unavail')
        topauc = soup.find('span', class_='wide-only')

        if 'Bid History' in str(sales):
            alls.append(word)
            with open(mainpath+r'\solded.txt','a') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'\nauction {word}'
        
        if 'Ownership History' in str(sales):
            alls.append(word)
            print('Good')
            with open(mainpath+r'\solded.txt','a',encoding='utf-8') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'sold {word}'

        if 'Unavailable' in str(sales):
            claimlist.append(word)
            alls.append(word)
            with open(mainpath+r'\html.html','a') as f:
                f.write(text)
                print('записано')
            await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'free `{word}` @{word}',parse_mode="MARKDOWN")
            #await query(word,client)
            with open(mainpath+r'\free.txt','a') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'\nfree {word}'

        if sold:
            alls.append(word)
            print('Good')
            with open(mainpath+r'\solded.txt','a',encoding='utf-8') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'\nsold {word}'
        
        if taken:
            return f'\nclaimed {word}'

        if avail:
            return f'\nselling {word}'

        if topauc:
            #print(r)
            return 1
        
        if 'Error code 520' in text:
            print(r)
            print('520 помогите1' )
            return 2 
        
        print('PISHET1')
        with open(r'C:\Users\уы\Desktop\html.html','a',encoding='utf-8') as f:
            f.write(text)
            #quit()
    except Exception as e:
        print('username1',e)
        
async def username(word,text,r,client):
    try:
        soup = BeautifulSoup(text, "html.parser")
        sales = soup.find('div', class_='table-cell-value tm-value tm-status-unavail')
        taken = soup.find('div', class_='table-cell-value tm-value tm-status-taken')
        avail = soup.find('div', class_='table-cell-value tm-value tm-status-avail')
        topauc = soup.find('span', class_='wide-only')

        if 'Bid History' in str(sales):
            return f'\nauction1 {word}'
        
        if 'Ownership History' in str(sales):
            alls.append(word)
            with open(mainpath+r'\solded.txt','a') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'\nSold {word}'

        if 'Unavailable' in str(sales):
            claimlist.append(word)
            alls.append(word)
            await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'free `{word}` @{word}',parse_mode="MARKDOWN")
            #await query(word,client)
            with open(mainpath+r'\free.txt','a') as f:
                f.write(f'{word}\n')
                print('записано')
            return f'\nFree {word}'
        
        if taken:
            return f'\nClaimed1 {word}'

        if avail:
            return f'\nSelling1 {word}'

        if topauc:
            #print(r)
            return 1
        
        if 'Error code 520' in text:
            print(r)
            print('520 помогите' )
            return 2 
        
        else:
            with open(r'C:\Users\уы\Desktop\html.html','a',encoding='utf-8') as f:
                f.write(text)
                print('PISHET')
                #quit()

    except Exception as e:
        print('usernameF',e)

async def claim(word,client):
    try:
        await client.connect()
        me = await client.get_me()
        print('Начинается Claim',word, 'На аккаунте:',me.first_name)
        result = await client(functions.channels.UpdateUsernameRequest(channel=channels[0], username=word))
        if result == True:
            print('Результат: ',result)
            del channels[0]
            del claimlist[0]
            await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'{result} @{word}')
            await client.disconnect()
            return
        else:
            print('resolt not True')
            print(result)
            alls.append(word)
            await bot.send_message(chat_id=YOUR_CHAT_ID, text=f'banned {word}')
            await client.disconnect()
            return

    except UsernameInvalidError:
        await banneddelete(word)
        return 'banned'
    except UsernameOccupiedError:
        await banneddelete(word)
        return 'taken'
    except UsernamePurchaseAvailableError:
        await banneddelete(word)
        return 'no free'
    except ChannelInvalidError:
        await banneddelete(word)
        return 'error name channel'
    except Exception as e:
        await banneddelete(word)
        print('claim erorr',e)

async def start():
    random.shuffle(words)
    list(set(words))
    api_hash=config.api_hash
    api_id=config.api_id
    print(api_hash,api_id)
    client = await TelegramClient('zzved.session',api_hash=config.api_hash,api_id=config.api_id, system_version='4.16.30-vxCUSTOM').start()
    await client.connect()
    me = await client.get_me()
    print('Аккаунт',me.first_name,me.id,'загружен')
    print('Настройка слов выполнена.')
    await client.disconnect()
'''    dialogs = await client.get_dialogs()
    for dia in dialogs:
        print(dia.title)
        has = hasattr(dia.entity, 'creator')
        if has == True:
            if 'qewin' in dia.title: 
                print(dia)

                result = await client(functions.channels.UpdateUsernameRequest(channel=dia.entity, username='dddddOVOSHdddddd2222'))
'''
    #print('Настройка слов выполнена.')
    #await client.disconnect()

async def filter(word,session):
    try:

        
        if word in alls:
            print('q',word)
            words.remove(word)
            return

        if not word[0].isalpha():
            print('w',word)
            words.remove(word)
            return

        if word[0].isnumeric():
            print('e',word)
            words.remove(word)
            return
        
        if len(word) <= 4:
            print(word)
            words.remove(word)
            return
        
        await telegram(word,session)

    except Exception as e:
        print(e)
    
async def query(word,client):
    await asyncio.sleep(10)
    await claim(claimlist[0],client)
    
async def getgroups():
    try:
        client = await TelegramClient('zzved.session',api_hash=config.api_hash,api_id=config.api_id, system_version='4.16.30-vxCUSTOM').start('0')
        chat = await client.get_input_entity('zzved')
        print(chat)
        await client.connect()
        global channels
        me = await client.get_me()
        print('получаем группы На аккаунте:',me.first_name)
        dialogs = await client.get_dialogs()
        for dia in dialogs:
            if 'qewin' in dia.title:
                print(dia.entity.username)
                channels.append(dia.entity)

        print('Загруженно', len(channels), 'групп')
        await client.disconnect()
        return client
    except Exception as e:
        print('get groups',e)

async def banneddelete(word):
    del claimlist[0] 
    alls.append(word)
    return

async def main():

    try:
        await start()

        client = await getgroups()
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = []
                for wordf in words:
                    tasks.append(telegram(wordf, session, client))

                try:
                    await asyncio.gather(*tasks)
                except asyncio.CancelledError:
                    pass

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())
