token = "7818062489:AAEh3vbk2z212B2Yls-aP6znsu-zcRa6Vc8"

import asyncio
import requests
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from manager import Manager
from balechecker.grpcp import ProtobufEncoder
from datetime import datetime
from pytz import timezone

bot = AsyncTeleBot(token)
manager = Manager()

request_headers = {
    'authority': 'next-ws.bale.ai',
    'method': 'POST',
    'accept': 'application/grpc-web-text',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '152',
    'content-type': 'application/grpc-web-text',
    'cookie': '_ga=GA1.1.1530819521.1676153465; _ga_M7ZV898665=GS1.1.1676195727.2.1.1676196141.60.0.0',
    'origin': 'https://web.bale.ai',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-grpc-web': '1',
    'x-user-agent': 'grpc-web-javascript/0.1',
}

def encode_proto(json_d):
    grpc_encode_base = {'trailer': '', 'msgs': []}
    grpc_encode_base['msgs'].append(json_d)
    encoder = ProtobufEncoder(grpc_encode_base)
    res = encoder.encode_grpc()
    return res

@bot.message_handler(content_types=['text'], chat_types=['private', 'supergroup'])
async def onMessages(msg: Message):
    await manager.validate(msg.from_user.id)

    if msg.text.startswith("لاگ"):
        inc = await manager.getIncludes(msg.from_user.id)
        if inc.phone == "":
            logFront = msg.text[3:].strip()
            if logFront == "":
                await bot.reply_to(msg, "[ ❌ ] - شماره تلفنی یافت نشد", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("close", callback_data="close")
                ))
            
            elif not logFront.startswith("+98"):
                await bot.reply_to(msg, "[ ❌ ] - شماره تلفن دارای کد ایران (+98) نمیباشد", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("close", callback_data="close")
                ))
            
            else:
                dt = datetime.now(timezone("Asia/Tehran"))
                await manager.setPhone(msg.from_user.id, logFront)
                await bot.reply_to(msg, f"[ ✅ ] - شماره تلفن ست شد\n[ ⌛ ] - در {dt.strftime("%Y/%m/%d ● %H:%M:%S")}\n[ 💎 ] - {logFront}", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("login ♻", callback_data=f"log_{logFront}")
                ))
        
        else:
            logFront = msg.text[3:].strip()
            if logFront == "":
                await bot.reply_to(msg, "[ ❌ ] - شماره تلفنی یافت نشد", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("close", callback_data="close")
                ))
            
            elif not logFront.startswith("+98"):
                await bot.reply_to(msg, "[ ❌ ] - شماره تلفن دارای کد ایران (+98) نمیباشد", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("close", callback_data="close")
                ))
            
            else:
                mark = InlineKeyboardMarkup()
                mark.add(
                    InlineKeyboardButton("تغییر 👀", callback_data=f"accept_{logFront}"),
                    InlineKeyboardButton("تمایل ندارم ❌", callback_data="close")
                )
                await bot.reply_to(msg, f"[ ⏭ ] - از قبل برای شما شماره تلفنی ثبت شده, مایل به تغییر آن هستید؟\n[ 📪 ] - تلفن {inc.phone}", reply_markup=mark)

@bot.callback_query_handler(func=lambda call: True)
async def onQuery(call: CallbackQuery):
    if call.data == "close":
        if call.message.reply_to_message.from_user.id == call.from_user.id:
            try:await bot.delete_message(call.message.chat.id, call.message.id)
            except:...

    elif call.data.startswith("accept"):
        if call.message.reply_to_message.from_user.id == call.from_user.id:
            dt = datetime.now(timezone("Asia/Tehran"))
            logFront = call.data.split("_")[1]
            await manager.setPhone(call.message.from_user.id, logFront)
            await bot.edit_message_text(f"[ ✅ ] - شماره تلفن جایگذاری شد\n[ ⌛ ] - در {dt.strftime("%Y/%m/%d ● %H:%M:%S")}\n[ 💎 ] - {logFront}", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("login ♻", callback_data=f"log_{logFront}")
            ), chat_id=call.message.chat.id, message_id=call.message.id)

    elif call.data.startswith("log_"):
        logFront = call.data.split("_")[1]
        grcpencode = encode_proto({'1:0': int(logFront), '2:0': 4, '3:2': 'C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D', '4:2': 'Chrome, Windows', '5:2': 'Chrome, Windows'})
        loginn = requests.post('https://next-ws.bale.ai/bale.auth.v1.Auth/StartPhoneAuth', data=grcpencode, headers=request_headers)

asyncio.run(bot.polling())