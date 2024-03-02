################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || MissKaty
"""
################################################################

import inspect
import json
import os.path
from functools import partial, wraps
from glob import glob
from typing import Dict, List

from team.nandev.database import udB


enabled_locales: List[str] = [
    "en-US",  # English (United States)
    "id-ID",  # Indonesian
]

default_language: str = "id-ID"


def cache_localizations(files: List[str]) -> Dict[str, Dict[str, Dict[str, str]]]:
    ldict = {lang: {} for lang in enabled_locales}
    for file in files:
        _, lname, pname = file.split(os.path.sep)
        pname = pname.split(".")[0]
        dic = json.load(open(file, encoding="utf-8"))
        dic.update(ldict[lname].get(pname, {}))
        ldict[lname][pname] = dic
    return ldict


jsons: List[str] = []

for locale in enabled_locales:
    jsons += glob(os.path.join("langs", locale, "*.json"))

langdict = cache_localizations(jsons)


def get_locale_string(
    dic: dict, language: str, default_context: str, key: str, context: str = None
) -> str:
    if context:
        default_context = context
        dic = langdict[language].get(context, langdict[default_language][context])
    res: str = (
        dic.get(key) or langdict[default_language][default_context].get(key) or key
    )
    return res


async def get_lang(c) -> str:

    lang = default_language or udB.get_bahasa(c.me.id)

    if len(lang.split("-")) == 1:
        # Try to find a language that starts with the provided language_code
        for locale_ in enabled_locales:
            if locale_.startswith(lang):
                lang = locale_
    elif lang.split("-")[1].islower():
        lang = lang.split("-")
        lang[1] = lang[1].upper()
        lang = "-".join(lang)
    return lang if lang in enabled_locales else default_language


def bahasa():
    def decorator(func):
        @wraps(func)
        async def wrapper(c, m):
            lang = await get_lang(c)

            dic = langdict.get(lang, langdict[default_language])

            lfunc = partial(get_locale_string, dic.get(context, {}), lang, context)
            return await func(c, m, lfunc)

        return wrapper

    return decorator
