token = "7818062489:AAEh3vbk2z212B2Yls-aP6znsu-zcRa6Vc8"

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from manager import Manager
from datetime import datetime
from pytz import timezone

bot = AsyncTeleBot(token)
manager = Manager()

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
                await manager.setPhone(logFront)
                await bot.reply_to(msg, f"[ ✅ ] - شماره تلفن ست شد\n[ ⌛ ] - {dt.strftime("%Y/%m/%d ● %H:%M:%S")}\n[ 💎 ] - {logFront}", reply_markup=InlineKeyboardMarkup().add(
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
                await bot.reply_to(msg, f"[ ⏭ ] - از قبل برای شما شماره تلفنی ثبت شده, مایل به تغییر آن هستید؟\n[ 📪 ] - {inc.phone}", reply_markup=mark)

@bot.callback_query_handler(func=lambda call: True)
async def onQuery(call: CallbackQuery):
    if call.data == "close":
        if call.message.reply_to_message.from_user.id == call.from_user.id:
            try:await bot.delete_message(call.message.chat.id, call.message.id)
            except:...

    elif call.data.startswith("accecpt"):
        dt = datetime.now(timezone("Asia/Tehran"))
        logFront = call.data.split("_")[1]
        await manager.setPhone(logFront)
        await bot.edit_message_text(f"[ ✅ ] - شماره تلفن جایگذاری شد\n[ ⌛ ] - {dt.strftime("%Y/%m/%d ● %H:%M:%S")}\n[ 💎 ] - {logFront}", reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("login ♻", callback_data=f"log_{logFront}")
        ), chat_id=call.message.chat.id, message_id=call.message.id)

    elif call.data.startswith("log_"):...