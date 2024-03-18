# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinXdSupport & t.me/AyiinSupport

import asyncio

from pyrogram import *

from Mix import *


@ky.ubot("cacad", sudo=True)
async def _(c: nlx, m):
    if m.reply_to_message and m.reply_to_message.from_user.id in DEVS:
        await m.edit("**YOUR ACCOUNT IS GONE, BITCH?**")
        return
    uputt = await m.edit("**Cacad 😏**", reply_to_message_id=ReplyCheck(m))
    await asyncio.sleep(1.8)
    await uputt.edit("**Unclean Accounts are Handicapped 😂**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Hahahahaha Cacad 🤣**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Defective Account Joke 😂🤣**")


@ky.ubot("hayo", sudo=True)
async def _(c: nlx, m):
    if m.reply_to_message and m.reply_to_message.from_user.id in DEVS:
        await m.edit("**YOUR ACCOUNT IS LOST, BITCH??**")
        return
    uputt = await m.edit("**Hayolo 😂**", reply_to_message_id=ReplyCheck(m))
    await asyncio.sleep(1.8)
    await uputt.edit("**Hayoloo 😭**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Hayolooo 😆**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Hayoloooo 😭🕺**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Hayolooooo 👻**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Haayolooooo 🤭**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Did the bot die?**")
    await asyncio.sleep(1.8)
    await uputt.edit("**Is the bot dead? kasiaaaan** 😭🤌")
