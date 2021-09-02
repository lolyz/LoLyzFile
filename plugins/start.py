#(©)Codexbotz

import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, START_MSG, OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON
from helper_func import subscribed, encode, decode, get_messages

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    text = "<b>𝗔𝗻𝗱𝗮 𝗵𝗮𝗿𝘂𝘀 𝗷𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹/𝗚𝗿𝗼𝘂𝗽 𝘂𝗻𝘁𝘂𝗸 𝗺𝗲𝗻𝗴𝗴𝘂𝗻𝗮𝗸𝗮𝗻 𝗕𝗢𝗧\n\n 𝙏𝙤𝙡𝙤𝙣𝙜 𝙗𝙚𝙧𝙜𝙖𝙗𝙪𝙣𝙜𝙡𝙖𝙝 𝙙𝙞 𝐊𝐞𝐝𝐮𝐚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡/𝙂𝙧𝙤𝙪𝙥. 𝙆𝙖𝙡𝙖𝙪 𝙗𝙚𝙡𝙪𝙢 𝙟𝙤𝙞𝙣, 𝘽𝙊𝙏 𝙩𝙞𝙙𝙖𝙠 𝙢𝙚𝙣𝙜𝙞𝙧𝙞𝙢 𝙛𝙞𝙡𝙚/𝙩𝙞𝙙𝙖𝙠 𝘽𝙚𝙠𝙚𝙧𝙟𝙖. 𝙠𝙖𝙡𝙖𝙪 𝙨𝙪𝙙𝙖𝙝 𝙟𝙤𝙞𝙣 𝙨𝙞𝙡𝙖𝙝𝙠𝙖𝙣 𝙠𝙡𝙞𝙠</b>"
    message_text = message.text
    try:
        command, argument = message_text.split()
        text = text + f" <b>\n\n<a href='https://t.me/{client.username}?start={argument}'>GET LINK</a></b>"
            except ValueError:
        pass
    reply_markup = InlineKeyboardMarkup(
             [
                  [
                       InlineKeyboardButton("𝐋𝐀𝐆𝐈 𝐕𝐈𝐑𝐀𝐋", url="https://t.me/LgViral"),
                       InlineKeyboardButton("𝐓𝐄𝐑𝐕𝐈𝐑𝐀𝐋", url="https://t.me/TerViral")
                  ],
                  [
                       InlineKeyboardButton("🔄 𝐆𝐄𝐓 𝐅𝐈𝐋𝐄 🔄", url = f'https://t.me/{client.username}?start={argument}')
                  ]
             ]
         )
    await message.reply(
        text = text,
        reply_markup = reply_markup,
        quote = True,
        disable_web_page_preview = True
    )
