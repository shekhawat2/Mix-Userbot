################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio
import importlib
import re
import subprocess

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.handlers import *
from pyrogram.types import *
from team.nandev.class_log import LOGGER
from team.nandev.class_modules import CMD_HELP
from team.nandev.database import ndB, udB

from assistant import BOT_PLUGINS
from config import *
from modular import USER_MOD

TOKEN_BOT = ndB.get_key("BOT_TOKEN") or bot_token


class Userbot(Client):
    _prefix = {}
    _translate = {}

    def __init__(self, **kwargs):
        super().__init__(
            name="user",
            api_id=api_id,
            api_hash=api_hash,
            session_string=session,
            device_model="Mix-Userbot",
            proxy=dict(hostname=proxy_host, port=22),
            **kwargs,
        )
        # ipv6=True,

    """
            proxy={
                "scheme": "socks5",
                "hostname": proxy_host,
                "port": 1080,
                "username": proxy_username,
                "password": proxy_password,
            },
    """

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    def user_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, c, m):
            if m.text:
                text = m.text.strip().encode("utf-8").decode("utf-8")
                username = c.me.username or ""
                prefixes = await self.get_prefix(c.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix) :]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        m.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)

    def get_m(self, m):
        msg = (
            m.reply_to_message
            if m.reply_to_message
            else "" if len(m.command) < 2 else " ".join(m.command[1:])
        )
        return msg

    def get_text(self, m):
        if m.reply_to_message:
            if len(m.command) < 2:
                text = m.reply_to_message.text or m.reply_to_message.caption
            else:
                text = (
                    (m.reply_to_message.text or m.reply_to_message.caption)
                    + "\n\n"
                    + m.text.split(None, 1)[1]
                )
        else:
            if len(m.command) < 2:
                text = ""
            else:
                text = m.text.split(None, 1)[1]
        return text

    async def eor(self, message, text):
        sudo_id = udB.get_list_from_var(self.me.id, "SUDO_USER", "ID_NYA")
        if not message:
            return await message.edit(text)
        if not message.from_user:
            return await message.edit(text)
        if message.from_user.id in sudo_id:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(text)
            return await message.reply_text(text)
        return await message.edit(text)

    async def bash(self, cmd):
        try:
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err
        except NotImplementedError:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            stdout, stderr = process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err

    async def run_cmd(self, cmd):
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    async def aexec(self, code, c, m):
        exec(
            "async def __aexec(c, m): " + "".join(f"\n {l_}" for l_ in code.split("\n"))
        )
        return await locals()["__aexec"](c, m)

    async def shell_exec(self, code, treat=True):
        process = await asyncio.create_subprocess_shell(
            code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )

        stdout = (await process.communicate())[0]
        if treat:
            stdout = stdout.decode().strip()
        return stdout, process

    def get_arg(self, m):
        if m.reply_to_message and len(m.command) < 2:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
            return msg
        elif len(m.command) > 1:
            return " ".join(m.command[1:])
        else:
            return ""

    async def extract_userid(self, m, t):
        def is_int(t):
            try:
                int(t)
            except ValueError:
                return False
            return True

        text = t.strip()

        if is_int(text):
            return int(text)

        entities = m.entities
        m._client
        entity = entities[1 if m.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            return (await self.get_users(text)).id
        if entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
        return None

    async def extract_user_and_reason(self, m, s=False):
        args = m.text.strip().split()
        text = m.text
        rg = None
        reason = None
        if m.reply_to_message:
            reply = m.reply_to_message
            if not reply.from_user:
                if reply.sender_chat and reply.sender_chat != m.chat.id and s:
                    id_ = reply.sender_chat.id
                else:
                    return None, None
            else:
                id_ = reply.from_user.id

            if len(args) < 2:
                reason = None
            else:
                reason = text.split(None, 1)[1]
            return id_, reason

        if len(args) == 2:
            rg = text.split(None, 1)[1]
            return await self.extract_userid(m, rg), None

        if len(args) > 2:
            rg, reason = text.split(None, 2)[1:]
            return await self.extract_userid(m, rg), reason

        return rg, reason

    async def extract_user(self, m):
        return (await self.extract_user_and_reason(m))[0]

    async def start(self):
        await super().start()
        handler = udB.get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._translate[self.me.id] = {"negara": "id"}
        LOGGER.info(f"Importing User Modules...")
        for modul in USER_MOD:
            imported_module = importlib.import_module(f"modular." + modul)
            if hasattr(imported_module, "__modles__") and imported_module.__modles__:
                imported_module.__modles__ = imported_module.__modles__
                if hasattr(imported_module, "__help__") and imported_module.__help__:
                    CMD_HELP[imported_module.__modles__.replace(" ", "_").lower()] = (
                        imported_module
                    )
        LOGGER.info(f"Successfully Import User Modules...")
        LOGGER.info(f"Starting Userbot {self.me.id}|{self.me.mention}")


class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(
            name="bot", api_id=api_id, api_hash=api_hash, bot_token=TOKEN_BOT, **kwargs
        )

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        LOGGER.info(f"Importing Bot Modules...")
        for plus in BOT_PLUGINS:
            imported_module = importlib.import_module(f"assistant." + plus)
            importlib.reload(imported_module)
        LOGGER.info(f"Successfully Import Bot Modules...")
        LOGGER.info(f"Starting Assistant {self.me.id}|{self.me.mention}")
