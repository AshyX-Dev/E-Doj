#Creator : @LydiaTeam
#Updater : @netixPhish
#Lib
import telebot, ast, os, random, requests, json
from telebot import types
from grpcp import *
from time import sleep
import threading

#Info
admin = [-1001912799127, 5854456385]
token =  "6691418175:AAGr-"
bot = telebot.TeleBot(token)

#Headers
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

#Defs
def check_validity(message):
    text = message.text
    chatid = message.chat.id    
    if message.text:
        try:

            nexttext = text.split('_')
            rangetext = nexttext[2].split('&')
            
            for savers in range(1, 99):
                savern = open(f'./data/numbers{savers}.txt', 'w')
                savern.write("hi\n")
                savern.close()

            count = 0 # time counter 
            times = 1 # how many times get 2000
            for newnumber in range(int(rangetext[0]), int(rangetext[1])):
                fullnumber = f"{nexttext[1]}{newnumber}"
                
                saver = open(f'./data/numbers{times}.txt', 'a')
                saver.write(f"{fullnumber}\n")
                saver.close()
                
                if int(count) == int(1000):
                    times += 1
                    count = 0

                count += 1

            numbers_markup = types.InlineKeyboardMarkup()
            numbers_markup.add(types.InlineKeyboardButton(text="Confirm✅", callback_data="['confirm','" + str(times) + "']"))
            bot.send_message(chatid, "Do u wannna check validity of this data ?", reply_markup=numbers_markup)
        except:
           bot.send_message(chatid, "Unknown pattern ❌")

def perform_headers(token, path):
    perform_header = {

    'authority': 'next-ws.bale.ai',
    'method': 'POST',
    'scheme': 'https',
    'path': f'{path}',
    'accept': 'application/grpc-web-text',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '36',
    'content-type': 'application/grpc-web-text',
    'cookie': f'access_token={token};',
    'origin': 'https://web.bale.ai',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'ec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-grpc-web': '1',
    'x-user-agent': 'grpc-web-javascript/0.1',

    }

    return perform_header

def decode_proto(string):
    parser = ProtobufParser(string)
    grpc = parser.parse_grpc()
    for msg in grpc['msgs']:
        return msg

def encode_proto(json_d):
    grpc_encode_base = {'trailer': '', 'msgs': []}
    grpc_encode_base['msgs'].append(json_d)
    encoder = ProtobufEncoder(grpc_encode_base)
    res = encoder.encode_grpc()
    return res

def setphonenumber(message):
    number = message.text
    lnumber = list(message.text)

    if len(lnumber) == 12:
        psaver = open('./data/number.txt', 'w', encoding='utf-8')
        psaver.write(number)
        psaver.close()
        bot.send_message(message.chat.id, "✅ Your PHONENUMBER changed successfully.")

    else:
        bot.send_message(message.chat.id, "❌ Please send me a valid PHONENUMBER .")

def makeKeyboard(number=None):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="👤 PhoneNumber :",
                                            callback_data="phone"),
        types.InlineKeyboardButton(text=f"{number}",
                                callback_data="jyjytyjyj")),
    
    markup.add(types.InlineKeyboardButton(text="🔎 Login",
                                        callback_data="login")) 
                  
    return markup

def login(message, res):
    try:
        auth = message.text
        rphone = open('./data/number.txt', 'r').read()
        chatid = message.chat.id
        response_decode = decode_proto(res)
        result = response_decode['1:2']

        verify_encode = encode_proto({'1:2': f'{result}', '2:2': f'{auth}', '3:2': {'1:0': 1}})
        try:
            sendcode = requests.post('https://next-ws.bale.ai/bale.auth.v1.Auth/ValidateCode', data=verify_encode, headers=request_headers)
        except:
            pass

        if sendcode.status_code == 200:
            res_decode = decode_proto(sendcode.text)
            resresult = res_decode['2:2']['2:0']
            resresult2 = res_decode['4:2']['1:2']

            sid = open('./data/sid.txt', 'w')
            sid.write(f"{resresult}")
            sid.close()

            accesstoken = open('./data/token.txt', 'w')
            accesstoken.write(f"{resresult2}")
            accesstoken.close()
            #print(resresult)
            bot.send_message(chatid, f"✅ You have successfully logged in.\n📞 Phone : {rphone}\nuse /check command to find valid numbers.")
        else:
            bot.send_message(chatid, f"❌ There is a problem")
    except:
        pass

def checkvalidity(chat_id, read_phone_numbers, raccesstoken):
    for validnumbter in read_phone_numbers:
        newnum = validnumbter.replace('09', '989')
        #Search Contact 
        grcpencode = encode_proto({'1:2': f'{newnum}'})
        try:
            importco = requests.post('https://next-ws.bale.ai/bale.users.v1.Users/SearchContacts', data=grcpencode, headers=perform_headers(raccesstoken, '/bale.users.v1.Users/SearchContacts'))
            importco_response = decode_proto(importco.text) #response import contact
            if "2:2" in importco_response:
                validdata = open(f'./data/validnumbers.txt', 'a')
                validdata.write(f'{validnumbter}\n')
                validdata.close()
        except:
            print('cnnection error.')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.chat.id
    if os.path.isfile('./data/number.txt'):
        rphone = open('./data/number.txt', 'r').read()
        bot.send_message(chat_id=message.chat.id,
                text=f"Hello, dear {message.from_user.first_name} .",
                reply_markup=makeKeyboard(rphone),
                parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id,
            text=f"Hello, dear {message.from_user.first_name} .",
            reply_markup=makeKeyboard(),
            parse_mode='HTML')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.content_type == "text":
        if message.chat.id in admin:
            chat_id = message.chat.id

            if message.text.startswith("/check_"):
                check_validity(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:

        chat_id = call.message.chat.id
        if chat_id in admin:
            if (call.data.startswith("['confirm','")):
                threads = []
                timesFromCallBack = int(ast.literal_eval(call.data)[1]) + int(1)
                bot.send_message(chat_id, "The validation process has been started(30 min).")

                raccesstoken = open('./data/token.txt', 'r').read()

                starter = open(f'./data/validnumbers.txt', 'w')
                starter.write('1.3\n')
                starter.close()

                for times in range(1, timesFromCallBack):
                    starter = open(f'./data/validnumbers{times}.txt', 'w')
                    starter.write('1.2\n')
                    starter.close()

                for do in range(1, timesFromCallBack):
                    read_phone_numbers = open(f'./data/numbers{do}.txt', 'r').read().splitlines()
                    t = threading.Thread(target=checkvalidity, args=[chat_id, read_phone_numbers, raccesstoken])
                    threads.append(t)   

                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                
                readvalidnumbersc = open(f'./data/validnumbers.txt', 'r').read().splitlines()
                readvalidnumbers = open(f'./data/validnumbers.txt', 'rb')
                bot.send_document(chat_id, readvalidnumbers, caption=f'Count : {len(readvalidnumbersc)}')


            elif (call.data.startswith("phone")):
                input_text = bot.send_message(chat_id, '📞 Send me your PhoneNumber for Login (989121478259) :')
                bot.register_next_step_handler(input_text, setphonenumber)

            elif (call.data.startswith("login")):
                if os.path.isfile('./data/number.txt'):
                    bot.send_message(chat_id, "🕔 Wait ...")
                    rphone = open('./data/number.txt', 'r').read()
                    
                    grcpencode = encode_proto({'1:0': int(rphone), '2:0': 4, '3:2': 'C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D', '4:2': 'Chrome, Windows', '5:2': 'Chrome, Windows'})
                    loginn = requests.post('https://next-ws.bale.ai/bale.auth.v1.Auth/StartPhoneAuth', data=grcpencode, headers=request_headers)
                    if loginn.status_code == 200:
                        input_text = bot.send_message(chat_id, '✏️ Send me your AUTH Code (i will send it to your PHONENUMBER) :')
                        bot.register_next_step_handler(input_text, login, loginn.text)
                    else:
                        bot.send_message(chat_id, "❌ There is a problem :/")

    except Exception as e:
        print(e)


bot.infinity_polling()

#@LydiaTeam
