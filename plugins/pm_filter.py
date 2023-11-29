# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
import random
import pytz
from datetime import datetime, timedelta, date, time
lock = asyncio.Lock()

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, get_tutorial, send_all, get_cap
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
    del_allg
)
import logging
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash, get_media_file_size

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTON = {}
BUTTONS = {}
FRESH = {}
BUTTONS0 = {}
BUTTONS1 = {}
BUTTONS2 = {}
SPELL_CHECK = {}
# ENABLE_SHORTLINK = ""

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.id != SUPPORT_CHAT_ID:
        manual = await manual_filters(client, message)
        if manual == False:
            settings = await get_settings(message.chat.id)
            try:
                if settings['auto_ffilter']:
                    await auto_filter(client, message)
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_ffilter', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_ffilter']:
                    await auto_filter(client, message) 
    else: #a better logic to avoid repeated lines of code in auto_filter function
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return
        else:
            return await message.reply_text(f"<b>Há´‡Ê {message.from_user.mention}, {str(total_results)} Ê€á´‡sá´œÊŸá´›s á´€Ê€á´‡ Ò“á´á´œÉ´á´… ÉªÉ´ á´Ê á´…á´€á´›á´€Ê™á´€sá´‡ Ò“á´Ê€ Êá´á´œÊ€ á´Ì¨á´œá´‡Ê€Ê {search}. \n\nTÊœÉªs Éªs á´€ sá´œá´˜á´˜á´Ê€á´› É¢Ê€á´á´œá´˜ sá´ á´›Êœá´€á´› Êá´á´œ á´„á´€É´'á´› É¢á´‡á´› Ò“ÉªÊŸá´‡s Ò“Ê€á´á´ Êœá´‡Ê€á´‡...\n\nJá´ÉªÉ´ á´€É´á´… Sá´‡á´€Ê€á´„Êœ Há´‡Ê€á´‡ - https://t.me/vj_bots</b>")

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    if user_id in ADMINS: return # ignore admins
    await message.reply_text(
         text=f"<b>Êœá´‡Ê {user} ðŸ˜ ,\n\nÊá´á´œ á´„á´€É´'á´› É¢á´‡á´› á´á´á´ Éªá´‡s êœ°Ê€á´á´ Êœá´‡Ê€á´‡. Ê€á´‡Ç«á´œá´‡sá´› Éªá´› ÉªÉ´ á´á´œÊ€ <a href=https://t.me/+UexCvjiPgXljNDRl>á´á´á´ Éªá´‡ É¢Ê€á´á´œá´˜</a> á´Ê€ á´„ÊŸÉªá´„á´‹ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ Ê™á´œá´›á´›á´É´ Ê™á´‡ÊŸá´á´¡ ðŸ‘‡</b>",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ“ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ ", url=f"https://t.me/+UexCvjiPgXljNDRl")]])
    )
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#ððŒ_ðŒð’ð†\n\nNá´€á´á´‡ : {user}\n\nID : {user_id}\n\nMá´‡ssá´€É¢á´‡ : {content}</b>"
    )

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    if BUTTONS.get(key)!=None:
        search = BUTTONS.get(key)
    else:
        search = FRESH.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return

    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    temp.GETALL[key] = files
    temp.SHORT[query.from_user.id] = query.message.chat.id
    settings = await get_settings(query.message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]

        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
    try:
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', True)
        if 0 < offset <= 10:
            off_set = 0
        elif offset == 0:
            off_set = None
        else:
            off_set = offset - 10
        if n_offset == 0:
            btn.append(
                [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
            )
        elif off_set is None:
            btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
        else:
            btn.append(
                [
                    InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                    InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                    InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                ],
            )
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    movie = re.sub(r"[:\-]", " ", movie)
    movie = re.sub(r"\s+", " ", movie).strip()
    await query.answer(script.TOP_ALRT_MSG)
    gl = await global_filters(bot, query.message, text=movie)
    if gl == False:
        k = await manual_filters(bot, query.message, text=movie)
        if k == False:
            files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
            if files:
                k = (movie, files, offset, total_results)
                await auto_filter(bot, query, k)
            else:
                reqstr1 = query.from_user.id if query.from_user else 0
                reqstr = await bot.get_users(reqstr1)
                if NO_RESULTS_MSG:
                    await bot.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, movie)))
                k = await query.message.edit(script.MVE_NT_FND)
                await asyncio.sleep(10)
                await k.delete()

#languages

@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):

    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    _, key = query.data.split("#")
    # if BUTTONS.get(key+"1")!=None:
    #     search = BUTTONS.get(key+"1")
    # else:
    #     search = BUTTONS.get(key)
    #     BUTTONS[key+"1"] = search
    search = FRESH.get(key)
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(LANGUAGES)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=LANGUAGES[i].title(),
                callback_data=f"fl#{LANGUAGES[i].lower()}#{key}"
            ),
            InlineKeyboardButton(
                text=LANGUAGES[i+1].title(),
                callback_data=f"fl#{LANGUAGES[i+1].lower()}#{key}"
            ),
        ])

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="ðŸ‘‡ ð–²ð–¾ð—…ð–¾ð–¼ð— ð–¸ð—ˆð—Žð—‹ ð–«ð–ºð—‡ð—€ð—Žð–ºð—€ð–¾ð—Œ ðŸ‘‡", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="â†­ Ê™á´€á´„á´‹ á´›á´ êœ°ÉªÊŸá´‡s â€‹â†­", callback_data=f"fl#homepage#{key}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
    

@Client.on_callback_query(filters.regex(r"^fl#"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    baal = lang in search
    if baal:
        search = search.replace(lang, "")
    else:
        search = search
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    if lang != "homepage":
        search = f"{search} {lang}" 
    BUTTONS[key] = search

    files, offset, total_results = await get_search_results(chat_id, search, offset=0, filter=True)
    if not files:
        await query.answer("ðŸš« ð—¡ð—¼ ð—™ð—¶ð—¹ð—² ð—ªð—²ð—¿ð—² ð—™ð—¼ð˜‚ð—»ð—± ðŸš«", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])

    if offset != "":
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
                )
    
            else:
                btn.append(
                    [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(query.message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="ððŽ ðŒðŽð‘ð„ ðð€ð†ð„ð’ ð€ð•ð€ðˆð‹ð€ðð‹ð„",callback_data="pages")]
        )
    
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total_results, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()
    
    
    
@Client.on_callback_query(filters.regex(r"^seasons#"))
async def seasons_cb_handler(client: Client, query: CallbackQuery):

    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    
    _, key = query.data.split("#")
    # if BUTTONS.get(key+"2")!=None:
    #     search = BUTTONS.get(key+"2")
    # else:
    #     search = BUTTONS.get(key)
    #     BUTTONS[key+"2"] = search
    search = FRESH.get(key)
    BUTTONS[key] = None
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(SEASONS)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=SEASONS[i].title(),
                callback_data=f"fs#{SEASONS[i].lower()}#{key}"
            ),
            InlineKeyboardButton(
                text=SEASONS[i+1].title(),
                callback_data=f"fs#{SEASONS[i+1].lower()}#{key}"
            ),
        ])

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="ðŸ‘‡ ð–²ð–¾ð—…ð–¾ð–¼ð— Season ðŸ‘‡", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="â†­ Ê™á´€á´„á´‹ á´›á´ êœ°ÉªÊŸá´‡s â€‹â†­", callback_data=f"next_{req}_{key}_{offset}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r"^fs#"))
async def filter_seasons_cb_handler(client: Client, query: CallbackQuery):
    _, seas, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    sea = ""
    season_search = ["s01","s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "season 01","season 02","season 03","season 04","season 05","season 06","season 07","season 08","season 09","season 10", "season 1","season 2","season 3","season 4","season 5","season 6","season 7","season 8","season 9"]
    for x in range (len(season_search)):
        if season_search[x] in search:
            sea = season_search[x]
            break
    if sea:
        search = search.replace(sea, "")
    else:
        search = search
    
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    
    searchagn = search
    search1 = search
    search2 = search
    search = f"{search} {seas}"
    BUTTONS0[key] = search
    
    files, _, _ = await get_search_results(chat_id, search, max_results=10)
    files = [file for file in files if re.search(seas, file.file_name, re.IGNORECASE)]
    
    seas1 = "s01" if seas == "season 1" else "s02" if seas == "season 2" else "s03" if seas == "season 3" else "s04" if seas == "season 4" else "s05" if seas == "season 5" else "s06" if seas == "season 6" else "s07" if seas == "season 7" else "s08" if seas == "season 8" else "s09" if seas == "season 9" else "s10" if seas == "season 10" else ""
    search1 = f"{search1} {seas1}"
    BUTTONS1[key] = search1
    files1, _, _ = await get_search_results(chat_id, search1, max_results=10)
    files1 = [file for file in files1 if re.search(seas1, file.file_name, re.IGNORECASE)]
    
    if files1:
        files.extend(files1)
    
    seas2 = "season 01" if seas == "season 1" else "season 02" if seas == "season 2" else "season 03" if seas == "season 3" else "season 04" if seas == "season 4" else "season 05" if seas == "season 5" else "season 06" if seas == "season 6" else "season 07" if seas == "season 7" else "season 08" if seas == "season 8" else "season 09" if seas == "season 9" else "s010"
    search2 = f"{search2} {seas2}"
    BUTTONS2[key] = search2
    files2, _, _ = await get_search_results(chat_id, search2, max_results=10)
    files2 = [file for file in files2 if re.search(seas2, file.file_name, re.IGNORECASE)]

    if files2:
        files.extend(files2)
        
    if not files:
        await query.answer("ðŸš« ð—¡ð—¼ ð—™ð—¶ð—¹ð—² ð—ªð—²ð—¿ð—² ð—™ð—¼ð˜‚ð—»ð—± ðŸš«", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, [
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}"),
            InlineKeyboardButton("Sá´‡ÊŸá´‡á´„á´› á´€É¢á´€ÉªÉ´", callback_data=f"seasons#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
        
    offset = 0

    btn.append([
            InlineKeyboardButton(
                text="â†­ Ê™á´€á´„á´‹ á´›á´ êœ°ÉªÊŸá´‡s â€‹â†­",
                callback_data=f"next_{req}_{key}_{offset}"
                ),
    ])
    
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        total_results = len(files)
        cap = await get_cap(settings, remaining_seconds, files, query, total_results, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
        except MessageNotModified:
            pass
    await query.answer()

                
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    lazyData = query.data
    try:
        link = await client.create_chat_invite_link(int(REQST_CHANNEL))
    except:
        pass
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("Done !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("Process Cancelled !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Má´€á´‹á´‡ sá´œÊ€á´‡ I'á´ á´˜Ê€á´‡sá´‡É´á´› ÉªÉ´ Êá´á´œÊ€ É¢Ê€á´á´œá´˜!!", quote=True)
                    return await query.answer(MSG_ALRT)
            else:
                await query.message.edit_text(
                    "I'á´ É´á´á´› á´„á´É´É´á´‡á´„á´›á´‡á´… á´›á´ á´€É´Ê É¢Ê€á´á´œá´˜s!\nCÊœá´‡á´„á´‹ /connections á´Ê€ á´„á´É´É´á´‡á´„á´› á´›á´ á´€É´Ê É¢Ê€á´á´œá´˜s",
                    quote=True
                )
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(MSG_ALRT)

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("Yá´á´œ É´á´‡á´‡á´… á´›á´ Ê™á´‡ GÊ€á´á´œá´˜ Oá´¡É´á´‡Ê€ á´Ê€ á´€É´ Aá´œá´›Êœ Usá´‡Ê€ á´›á´ á´…á´ á´›Êœá´€á´›!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("TÊœá´€á´›'s É´á´á´› Ò“á´Ê€ Êá´á´œ!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"GÊ€á´á´œá´˜ Ná´€á´á´‡ : **{title}**\nGÊ€á´á´œá´˜ ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(MSG_ALRT)
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cá´É´É´á´‡á´„á´›á´‡á´… á´›á´ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Sá´á´á´‡ á´‡Ê€Ê€á´Ê€ á´á´„á´„á´œÊ€Ê€á´‡á´…!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(MSG_ALRT)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"DÉªsá´„á´É´É´á´‡á´„á´›á´‡á´… Ò“Ê€á´á´ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sá´á´á´‡ á´‡Ê€Ê€á´Ê€ á´á´„á´„á´œÊ€Ê€á´‡á´…!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ á´…á´‡ÊŸá´‡á´›á´‡á´… á´„á´É´É´á´‡á´„á´›Éªá´É´ !"
            )
        else:
            await query.message.edit_text(
                f"Sá´á´á´‡ á´‡Ê€Ê€á´Ê€ á´á´„á´„á´œÊ€Ê€á´‡á´…!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "TÊœá´‡Ê€á´‡ á´€Ê€á´‡ É´á´ á´€á´„á´›Éªá´ á´‡ á´„á´É´É´á´‡á´„á´›Éªá´É´s!! Cá´É´É´á´‡á´„á´› á´›á´ sá´á´á´‡ É¢Ê€á´á´œá´˜s Ò“ÉªÊ€sá´›.",
            )
            return await query.answer(MSG_ALRT)
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Yá´á´œÊ€ á´„á´É´É´á´‡á´„á´›á´‡á´… É¢Ê€á´á´œá´˜ á´…á´‡á´›á´€ÉªÊŸs ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
        
    if query.data.startswith("file"):
        clicked = query.from_user.id
        try:
            typed = query.message.reply_to_message.from_user.id
        except:
            typed = query.from_user.id
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Ná´ sá´œá´„Êœ Ò“ÉªÊŸá´‡ á´‡xÉªsá´›.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if settings['is_shortlink'] and clicked not in PREMIUM_USER:
                if clicked == typed:
                    temp.SHORT[clicked] = query.message.chat.id
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=short_{file_id}")
                    return
                else:
                    await query.answer(f"Há´‡Ê {query.from_user.first_name}, TÊœÉªs Is Ná´á´› Yá´á´œÊ€ Má´á´ Éªá´‡ Rá´‡Ç«á´œá´‡sá´›. Rá´‡Ç«á´œá´‡sá´› Yá´á´œÊ€'s !", show_alert=True)
            else:
                if clicked == typed:
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Há´‡Ê {query.from_user.first_name}, TÊœÉªs Is Ná´á´› Yá´á´œÊ€ Má´á´ Éªá´‡ Rá´‡Ç«á´œá´‡sá´›. Rá´‡Ç«á´œá´‡sá´› Yá´á´œÊ€'s !", show_alert=True)
        except UserIsBlocked:
            await query.answer('UÉ´Ê™ÊŸá´á´„á´‹ á´›Êœá´‡ Ê™á´á´› á´á´€ÊœÉ´ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
            
    elif query.data.startswith("sendfiles"):
        clicked = query.from_user.id
        ident, key = query.data.split("#")
        settings = await get_settings(query.message.chat.id)
        try:
            if settings['is_shortlink'] and clicked not in PREMIUM_USER:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles1_{key}")
                return
            else:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=allfiles_{key}")
                return
        except UserIsBlocked:
            await query.answer('UÉ´Ê™ÊŸá´á´„á´‹ á´›Êœá´‡ Ê™á´á´› á´á´€ÊœÉ´ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles3_{key}")
        except Exception as e:
            logger.exception(e)
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles4_{key}")
    
    elif query.data.startswith("del"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Ná´ sá´œá´„Êœ Ò“ÉªÊŸá´‡ á´‡xÉªsá´›.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
    
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Já´ÉªÉ´ á´á´œÊ€ Bá´€á´„á´‹-á´œá´˜ á´„Êœá´€É´É´á´‡ÊŸ á´á´€ÊœÉ´! ðŸ˜’", show_alert=True)
            return
        ident, kk, file_id = query.data.split("#")
        await query.answer(url=f"https://t.me/{temp.U_NAME}?start={kk}_{file_id}")
    
    elif query.data == "pages":
        await query.answer()
    
    elif query.data.startswith("send_fsall"):
        temp_var, ident, key, offset = query.data.split("#")
        search = BUTTON0.get(key)
        if not search:
            await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
            return
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        search = BUTTONS1.get(key)
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        search = BUTTONS2.get(key)
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        await query.answer(f"Hey {query.from_user.first_name}, All files on this page has been sent successfully to your PM !", show_alert=True)
        
    elif query.data.startswith("send_fall"):
        temp_var, ident, key, offset = query.data.split("#")
        if BUTTONS.get(key)!=None:
            search = BUTTONS.get(key)
        else:
            search = FRESH.get(key)
        if not search:
            await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
            return
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        await query.answer(f"Hey {query.from_user.first_name}, All files on this page has been sent successfully to your PM !", show_alert=True)
        
    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        #await query.message.edit_text(f"<b>Fetching Files for your query {keyword} on DB... Please wait...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text("<b>File deletion process will start in 5 seconds !</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        logger.info(f'File Found for your query {keyword}! Successfully deleted {file_name} from database.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>Process started for deleting files from DB. Successfully deleted {str(deleted)} files from DB for your query {keyword} !\n\nPlease wait...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Error: {e}')
            else:
                await query.message.edit_text(f"<b>Process Completed for file deletion !\n\nSuccessfully deleted {str(deleted)} files from database for your query {keyword}.</b>")
    
    elif query.data.startswith("opnsetgrp"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yá´á´œ Dá´É´'á´› Há´€á´ á´‡ TÊœá´‡ RÉªÉ¢Êœá´›s Tá´ Dá´ TÊœÉªs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rá´‡sá´œÊŸá´› Pá´€É¢á´‡',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Bá´œá´›á´›á´É´' if settings["button"] else 'Tá´‡xá´›',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('FÉªÊŸá´‡ Sá´‡É´á´… Má´á´…á´‡', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Má´€É´á´œá´€ÊŸ Sá´›á´€Ê€á´›' if settings["botpm"] else 'Aá´œá´›á´ Sá´‡É´á´…',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('PÊ€á´á´›á´‡á´„á´› Cá´É´á´›á´‡É´á´›',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["file_secure"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iá´á´…Ê™', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["imdb"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sá´˜á´‡ÊŸÊŸ CÊœá´‡á´„á´‹',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["spell_check"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wá´‡ÊŸá´„á´á´á´‡ MsÉ¢', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["welcome"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-Dá´‡ÊŸá´‡á´›á´‡',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('5 MÉªÉ´s' if settings["auto_delete"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-FÉªÊŸá´›á´‡Ê€',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["auto_ffilter"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Má´€x Bá´œá´›á´›á´É´s',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SÊœá´Ê€á´›LÉªÉ´á´‹',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["is_shortlink"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"<b>CÊœá´€É´É¢á´‡ Yá´á´œÊ€ Sá´‡á´›á´›ÉªÉ´É¢s Fá´Ê€ {title} As Yá´á´œÊ€ WÉªsÊœ âš™</b>",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_reply_markup(reply_markup)
        
    elif query.data.startswith("opnsetpm"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yá´á´œ Dá´É´'á´› Há´€á´ á´‡ TÊœá´‡ RÉªÉ¢Êœá´›s Tá´ Dá´ TÊœÉªs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        btn2 = [[
                 InlineKeyboardButton("CÊœá´‡á´„á´‹ PM", url=f"telegram.me/{temp.U_NAME}")
               ]]
        reply_markup = InlineKeyboardMarkup(btn2)
        await query.message.edit_text(f"<b>Yá´á´œÊ€ sá´‡á´›á´›ÉªÉ´É¢s á´á´‡É´á´œ Ò“á´Ê€ {title} Êœá´€s Ê™á´‡á´‡É´ sá´‡É´á´› á´›á´ Êá´á´œÊ€ PM</b>")
        await query.message.edit_reply_markup(reply_markup)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rá´‡sá´œÊŸá´› Pá´€É¢á´‡',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Bá´œá´›á´›á´É´' if settings["button"] else 'Tá´‡xá´›',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('FÉªÊŸá´‡ Sá´‡É´á´… Má´á´…á´‡', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Má´€É´á´œá´€ÊŸ Sá´›á´€Ê€á´›' if settings["botpm"] else 'Aá´œá´›á´ Sá´‡É´á´…',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('PÊ€á´á´›á´‡á´„á´› Cá´É´á´›á´‡É´á´›',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["file_secure"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iá´á´…Ê™', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["imdb"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sá´˜á´‡ÊŸÊŸ CÊœá´‡á´„á´‹',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["spell_check"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wá´‡ÊŸá´„á´á´á´‡ MsÉ¢', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["welcome"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-Dá´‡ÊŸá´‡á´›á´‡',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('5 MÉªÉ´s' if settings["auto_delete"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-FÉªÊŸá´›á´‡Ê€',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["auto_ffilter"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Má´€x Bá´œá´›á´›á´É´s',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SÊœá´Ê€á´›LÉªÉ´á´‹',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["is_shortlink"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.send_message(
                chat_id=userid,
                text=f"<b>CÊœá´€É´É¢á´‡ Yá´á´œÊ€ Sá´‡á´›á´›ÉªÉ´É¢s Fá´Ê€ {title} As Yá´á´œÊ€ WÉªsÊœ âš™</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=query.message.id
            )

    elif query.data.startswith("show_option"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("UÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡", callback_data=f"unavailable#{from_user}"),
                InlineKeyboardButton("Uá´˜ÊŸá´á´€á´…á´‡á´…", callback_data=f"uploaded#{from_user}")
             ],[
                InlineKeyboardButton("AÊŸÊ€á´‡á´€á´…Ê Aá´ á´€ÉªÊŸá´€Ê™ÊŸá´‡", callback_data=f"already_available#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("VÉªá´‡á´¡ Sá´›á´€á´›á´œs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Há´‡Ê€á´‡ á´€Ê€á´‡ á´›Êœá´‡ á´á´˜á´›Éªá´É´s !")
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢Êœá´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)
        
    elif query.data.startswith("unavailable"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("âš ï¸ UÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ âš ï¸", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Já´ÉªÉ´ CÊœá´€É´É´á´‡ÊŸ', url=link.invite_link),
                 InlineKeyboardButton("VÉªá´‡á´¡ Sá´›á´€á´›á´œs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sá´‡á´› á´›á´ UÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Há´‡Ê {user.mention}, Sá´Ê€Ê€Ê Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Éªs á´œÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡. Sá´ á´á´œÊ€ á´á´á´…á´‡Ê€á´€á´›á´Ê€s á´„á´€É´'á´› á´œá´˜ÊŸá´á´€á´… Éªá´›.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Há´‡Ê {user.mention}, Sá´Ê€Ê€Ê Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Éªs á´œÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡. Sá´ á´á´œÊ€ á´á´á´…á´‡Ê€á´€á´›á´Ê€s á´„á´€É´'á´› á´œá´˜ÊŸá´á´€á´… Éªá´›.\n\nNá´á´›á´‡: TÊœÉªs á´á´‡ssá´€É¢á´‡ Éªs sá´‡É´á´› á´›á´ á´›ÊœÉªs É¢Ê€á´á´œá´˜ Ê™á´‡á´„á´€á´œsá´‡ Êá´á´œ'á´ á´‡ Ê™ÊŸá´á´„á´‹á´‡á´… á´›Êœá´‡ Ê™á´á´›. Tá´ sá´‡É´á´… á´›ÊœÉªs á´á´‡ssá´€É¢á´‡ á´›á´ Êá´á´œÊ€ PM, Má´œsá´› á´œÉ´Ê™ÊŸá´á´„á´‹ á´›Êœá´‡ Ê™á´á´›.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢Êœá´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)

    elif query.data.startswith("uploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("âœ… Uá´˜ÊŸá´á´€á´…á´‡á´… âœ…", callback_data=f"upalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Já´ÉªÉ´ CÊœá´€É´É´á´‡ÊŸ', url=link.invite_link),
                 InlineKeyboardButton("VÉªá´‡á´¡ Sá´›á´€á´›á´œs", url=f"{query.message.link}")
               ],[
                 InlineKeyboardButton("Rá´‡á´Ì¨á´œá´‡sá´› GÊ€á´á´œá´˜ LÉªÉ´á´‹", url="https://t.me/Deendayal_dhakad")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sá´‡á´› á´›á´ Uá´˜ÊŸá´á´€á´…á´‡á´… !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Há´‡Ê {user.mention}, Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Êœá´€s Ê™á´‡á´‡É´ á´œá´˜ÊŸá´á´€á´…á´‡á´… Ê™Ê á´á´œÊ€ á´á´á´…á´‡Ê€á´€á´›á´Ê€s. KÉªÉ´á´…ÊŸÊ sá´‡á´€Ê€á´„Êœ ÉªÉ´ á´á´œÊ€ GÊ€á´á´œá´˜.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Há´‡Ê {user.mention}, Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Êœá´€s Ê™á´‡á´‡É´ á´œá´˜ÊŸá´á´€á´…á´‡á´… Ê™Ê á´á´œÊ€ á´á´á´…á´‡Ê€á´€á´›á´Ê€s. KÉªÉ´á´…ÊŸÊ sá´‡á´€Ê€á´„Êœ ÉªÉ´ á´á´œÊ€ GÊ€á´á´œá´˜.\n\nNá´á´›á´‡: TÊœÉªs á´á´‡ssá´€É¢á´‡ Éªs sá´‡É´á´› á´›á´ á´›ÊœÉªs É¢Ê€á´á´œá´˜ Ê™á´‡á´„á´€á´œsá´‡ Êá´á´œ'á´ á´‡ Ê™ÊŸá´á´„á´‹á´‡á´… á´›Êœá´‡ Ê™á´á´›. Tá´ sá´‡É´á´… á´›ÊœÉªs á´á´‡ssá´€É¢á´‡ á´›á´ Êá´á´œÊ€ PM, Má´œsá´› á´œÉ´Ê™ÊŸá´á´„á´‹ á´›Êœá´‡ Ê™á´á´›.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢á´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)

    elif query.data.startswith("already_available"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("ðŸŸ¢ AÊŸÊ€á´‡á´€á´…Ê Aá´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ ðŸŸ¢", callback_data=f"alalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Já´ÉªÉ´ CÊœá´€É´É´á´‡ÊŸ', url=link.invite_link),
                 InlineKeyboardButton("VÉªá´‡á´¡ Sá´›á´€á´›á´œs", url=f"{query.message.link}")
               ],[
                 InlineKeyboardButton("Rá´‡á´Ì¨á´œá´‡sá´› GÊ€á´á´œá´˜ LÉªÉ´á´‹", url="https://t.me/Deendayal_dhakad")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sá´‡á´› á´›á´ AÊŸÊ€á´‡á´€á´…Ê Aá´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Há´‡Ê {user.mention}, Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Éªs á´€ÊŸÊ€á´‡á´€á´…Ê á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ á´É´ á´á´œÊ€ Ê™á´á´›'s á´…á´€á´›á´€Ê™á´€sá´‡. KÉªÉ´á´…ÊŸÊ sá´‡á´€Ê€á´„Êœ ÉªÉ´ á´á´œÊ€ GÊ€á´á´œá´˜.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Há´‡Ê {user.mention}, Yá´á´œÊ€ Ê€á´‡á´Ì¨á´œá´‡sá´› Éªs á´€ÊŸÊ€á´‡á´€á´…Ê á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ á´É´ á´á´œÊ€ Ê™á´á´›'s á´…á´€á´›á´€Ê™á´€sá´‡. KÉªÉ´á´…ÊŸÊ sá´‡á´€Ê€á´„Êœ ÉªÉ´ á´á´œÊ€ GÊ€á´á´œá´˜.\n\nNá´á´›á´‡: TÊœÉªs á´á´‡ssá´€É¢á´‡ Éªs sá´‡É´á´› á´›á´ á´›ÊœÉªs É¢Ê€á´á´œá´˜ Ê™á´‡á´„á´€á´œsá´‡ Êá´á´œ'á´ á´‡ Ê™ÊŸá´á´„á´‹á´‡á´… á´›Êœá´‡ Ê™á´á´›. Tá´ sá´‡É´á´… á´›ÊœÉªs á´á´‡ssá´€É¢á´‡ á´›á´ Êá´á´œÊ€ PM, Má´œsá´› á´œÉ´Ê™ÊŸá´á´„á´‹ á´›Êœá´‡ Ê™á´á´›.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢á´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)

    elif query.data.startswith("alalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Há´‡Ê {user.first_name}, Yá´á´œÊ€ Rá´‡á´Ì¨á´œá´‡sá´› Éªs AÊŸÊ€á´‡á´€á´…Ê Aá´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ !", show_alert=True)
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢á´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)

    elif query.data.startswith("upalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Há´‡Ê {user.first_name}, Yá´á´œÊ€ Rá´‡á´Ì¨á´œá´‡sá´› Éªs Uá´˜ÊŸá´á´€á´…á´‡á´… !", show_alert=True)
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢á´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)
        
    elif query.data.startswith("unalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Há´‡Ê {user.first_name}, Yá´á´œÊ€ Rá´‡á´Ì¨á´œá´‡sá´› Éªs UÉ´á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ !", show_alert=True)
        else:
            await query.answer("Yá´á´œ á´…á´É´'á´› Êœá´€á´ á´‡ sá´œÒ“Ò“Éªá´„Éªá´€É´á´› Ê€ÉªÉ¢á´›s á´›á´ á´…á´ á´›ÊœÉªs !", show_alert=True)

    elif lazyData.startswith("generate_stream_link"):
        _, file_id = lazyData.split(":")
        try:
            user_id = query.from_user.id
            username =  query.from_user.mention 

            log_msg = await client.send_cached_media(
                chat_id=LOG_CHANNEL,
                file_id=file_id,
            )
            fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            xo = await query.message.reply_text(f'ðŸ”')
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"â€¢â€¢ ÊŸÉªÉ´á´‹ É¢á´‡É´á´‡Ê€á´€á´›á´‡á´… êœ°á´Ê€ Éªá´… #{user_id} \nâ€¢â€¢ á´œêœ±á´‡Ê€É´á´€á´á´‡ : {username} \n\nâ€¢â€¢ á–´áŽ¥á’ªá—´ Ná—©á—°á—´ : {fileName}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸš€ Fast Download ðŸš€", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('ðŸ–¥ï¸ Watch online ðŸ–¥ï¸', url=lazy_stream)]])  # web stream Link
            )
            await query.message.reply_text(
                text="â€¢â€¢ ÊŸÉªÉ´á´‹ É¢á´‡É´á´‡Ê€á´€á´›á´‡á´… â˜ ï¸Žâš”",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸš€ Fast Download ðŸš€", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('ðŸ–¥ï¸ Watch online ðŸ–¥ï¸', url=lazy_stream)]])  # web stream Link
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"â˜£something went wrong sweetheart\n\n{e}", show_alert=True)
            return
    # don't change anything without contacting me @creatorrio

    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "select":
        await query.answer(text=script.SELECT, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)

    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('â¤¬ Aá´…á´… Má´‡ Tá´ Yá´á´œÊ€ GÊ€á´á´œá´˜ â¤¬', url=f'http://telegram.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('Eá´€Ê€É´ Má´É´á´‡Ê ðŸ’¸', callback_data="shortlink_info"),
                    InlineKeyboardButton('âŒ¬ Má´á´ Éªá´‡ GÊ€á´á´œá´˜', url=GRP_LNK)
                ],[
                    InlineKeyboardButton('ã€„ Há´‡ÊŸá´˜', callback_data='help'),
                    InlineKeyboardButton('âŸ AÊ™á´á´œá´›', callback_data='about')
                ],[
                  InlineKeyboardButton('âœ‡ Já´ÉªÉ´ Uá´˜á´…á´€á´›á´‡s CÊœá´€É´É´á´‡ÊŸ âœ‡', url=CHNL_LNK)
                  ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)

    elif query.data == "filters":
        buttons = [[
            InlineKeyboardButton('Má´€É´á´œá´€ÊŸ FIÊŸá´›á´‡Ê€', callback_data='manuelfilter'),
            InlineKeyboardButton('Aá´œá´›á´ FIÊŸá´›á´‡Ê€', callback_data='autofilter')
        ],[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help'),
            InlineKeyboardButton('GÊŸá´Ê™á´€ÊŸ FÉªÊŸá´›á´‡Ê€s', callback_data='global_filters')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ALL_FILTERS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "global_filters":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "help":
        buttons = [[
             InlineKeyboardButton('âš™ï¸ á´€á´…á´ÉªÉ´ á´É´ÊŸÊ ðŸ”§', callback_data='admin'),
         ], [ 
             InlineKeyboardButton('êœ°ÉªÊŸá´‡ êœ±á´›á´Ê€á´‡', callback_data='store_file'),   
             InlineKeyboardButton('á´›á´‡ÊŸá´‡É¢Ê€á´€á´˜Êœ', callback_data='tele') 
         ], [ 
             InlineKeyboardButton('á´„á´É´É´á´‡á´„á´›Éªá´É´êœ±', callback_data='coct'), 
             InlineKeyboardButton('êœ°ÉªÊŸá´›á´‡Ê€êœ±', callback_data='filters'),  
             InlineKeyboardButton('Êá´›-á´…ÊŸ', callback_data='ytdl') 
         ], [ 
             InlineKeyboardButton('êœ±Êœá´€Ê€á´‡ á´›á´‡xá´›', callback_data='share'), 
             InlineKeyboardButton('êœ±á´É´É¢', callback_data='song') 
         ], [
             InlineKeyboardButton('á´‡á´€Ê€É´ á´á´É´á´‡Ê', callback_data='shortlink_info'),
             InlineKeyboardButton('êœ±á´›Éªá´„á´‹á´‡Ê€-Éªá´…', callback_data='sticker'),
             InlineKeyboardButton('á´Š-êœ±á´É´', callback_data='json'),  
         ], [             
             InlineKeyboardButton('ðŸ  ð™·ð™¾ð™¼ð™´ ðŸ ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('Sá´œá´˜á´˜á´Ê€á´› GÊ€á´á´œá´˜', url=GRP_LNK),
            InlineKeyboardButton('Sá´á´œÊ€á´„á´‡ Cá´á´…á´‡', callback_data='source')
        ],[
            InlineKeyboardButton('Há´á´á´‡', callback_data='start'),
            InlineKeyboardButton('CÊŸá´sá´‡', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('â‡šBack', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='filters'),
            InlineKeyboardButton('Bá´œá´›á´›á´É´s', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='manuelfilter')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help'),
            InlineKeyboardButton('á´‡xá´›Ê€á´€', callback_data='extra')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "store_file":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FILE_STORE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='admin')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRA_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help'),
            InlineKeyboardButton('âŸ² Rá´‡Ò“Ê€á´‡sÊœ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('âŸ¸ Bá´€á´„á´‹', callback_data='help'),
            InlineKeyboardButton('âŸ² Rá´‡Ò“Ê€á´‡sÊœ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "shortlink_info":
            btn = [[
                InlineKeyboardButton("ðŸ‘‡Select Your Language ðŸ‘‡", callback_data="laninfo")
        ], [
            InlineKeyboardButton("Tamil", callback_data="tamil_info"),
            InlineKeyboardButton("English", callback_data="english_info"),
            InlineKeyboardButton("Hindi", callback_data="hindi_info")
        ], [
            InlineKeyboardButton("Malayalam", callback_data="malayalam_info"),
            InlineKeyboardButton("Urdu", callback_data="urdu_info"),
            InlineKeyboardButton("Bangla", callback_data="bangladesh_info")
        ], [
            InlineKeyboardButton("Telugu", callback_data="telugu_info"),
            InlineKeyboardButton("Kannada", callback_data="kannada_info"),
            InlineKeyboardButton("Gujarati", callback_data="gujarati_info"),
            InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start")

            ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "tele":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="help"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.TELE_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "ytdl":
        buttons = [[
            InlineKeyboardButton('â‡ Ê™á´€á´„á´‹ â‡', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="â— â—Œ â—Œ"
        )
        await query.message.edit_text(
            text="â— â— â—Œ"
        )
        await query.message.edit_text(
            text="â— â— â—"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.YTDL_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
)
    elif query.data == "share":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="help"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHARE_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "song":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="help"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SONG_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "json":
        buttons = [[
            InlineKeyboardButton('â‡ Ê™á´€á´„á´‹ â‡', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="â— â—Œ â—Œ"
        )
        await query.message.edit_text(
            text="â— â— â—Œ"
        )
        await query.message.edit_text(
            text="â— â— â—"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.JSON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
)
    elif query.data == "sticker":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="help"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.STICKER_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "tamil_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.TAMIL_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "english_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.ENGLISH_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "hindi_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.HINDI_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "telugu_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.TELUGU_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "malayalam_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.MALAYALAM_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "urdu_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.URDU_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "bangladesh_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]

            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.BANGLADESH_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "kannada_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.KANNADA_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "gujarati_info":
            btn = [[
                    InlineKeyboardButton("âŸ¸ Bá´€á´„á´‹", callback_data="start"),
                    InlineKeyboardButton("Cá´É´á´›á´€á´„á´›", url="telegram.me/Deendayal_dhakad")
                  ]]
        
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.GUJARATI_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Yá´á´œÊ€ Aá´„á´›Éªá´ á´‡ Cá´É´É´á´‡á´„á´›Éªá´É´ Há´€s Bá´‡á´‡É´ CÊœá´€É´É¢á´‡á´…. Gá´ Tá´ /connections á´€É´á´… á´„Êœá´€É´É¢á´‡ Êá´á´œÊ€ á´€á´„á´›Éªá´ á´‡ á´„á´É´É´á´‡á´„á´›Éªá´É´.")
            return await query.answer(MSG_ALRT)

        if set_type == 'is_shortlink' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hey {query.from_user.first_name}, You can't change shortlink settings for your group !\n\nIt's an admin only setting !", show_alert=True)

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rá´‡sá´œÊŸá´› Pá´€É¢á´‡',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Bá´œá´›á´›á´É´' if settings["button"] else 'Tá´‡xá´›',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('FÉªÊŸá´‡ Sá´‡É´á´… Má´á´…á´‡', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Má´€É´á´œá´€ÊŸ Sá´›á´€Ê€á´›' if settings["botpm"] else 'Aá´œá´›á´ Sá´‡É´á´…',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('PÊ€á´á´›á´‡á´„á´› Cá´É´á´›á´‡É´á´›',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["file_secure"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iá´á´…Ê™', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["imdb"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sá´˜á´‡ÊŸÊŸ CÊœá´‡á´„á´‹',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["spell_check"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wá´‡ÊŸá´„á´á´á´‡ MsÉ¢', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["welcome"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-Dá´‡ÊŸá´‡á´›á´‡',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('5 MÉªÉ´s' if settings["auto_delete"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aá´œá´›á´-FÉªÊŸá´›á´‡Ê€',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["auto_ffilter"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Má´€x Bá´œá´›á´›á´É´s',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SÊœá´Ê€á´›LÉªÉ´á´‹',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('âœ” OÉ´' if settings["is_shortlink"] else 'âœ˜ OÒ“Ò“',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
                                                                             ]

            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer(MSG_ALRT)

    
async def auto_filter(client, msg, spoll=False):
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    # reqstr1 = msg.from_user.id if msg.from_user else 0
    # reqstr = await client.get_users(reqstr1)
    
    if not spoll:
        message = msg
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text
            m=await message.reply_text(f"<b><i> ð–²ð–¾ð–ºð—‹ð–¼ð—ð—‚ð—‡ð—€ ð–¿ð—ˆð—‹ '{search}' ðŸ”Ž</i></b>")
            search = search.lower()
            find = search.split(" ")
            search = ""
            removes = ["in","upload", "series", "full", "horror", "thriller", "mystery", "print", "file"]
            for x in find:
                if x in removes:
                    continue
                else:
                    search = search + x + " "
            search = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", search, flags=re.IGNORECASE)
            search = re.sub(r"\s+", " ", search).strip()
            search = search.replace("-", " ")
            search = search.replace(":","")
            files, offset, total_results = await get_search_results(message.chat.id ,search, offset=0, filter=True)
            settings = await get_settings(message.chat.id)
            if not files:
                await m.delete()
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                else:
                    # if NO_RESULTS_MSG:
                    #     await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, search)))
                    return
        else:
            return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
        m=await message.reply_text(f"<b><i> ð–²ð–¾ð–ºð—‹ð–¼ð—ð—‚ð—‡ð—€ ð–¿ð—ˆð—‹ '{search}' ðŸ”Ž</i></b>")
        settings = await get_settings(message.chat.id)
        await msg.message.delete()
    pre = 'filep' if settings['file_secure'] else 'file'
    key = f"{message.chat.id}-{message.id}"
    FRESH[key] = search
    temp.GETALL[key] = files
    temp.SHORT[message.from_user.id] = message.chat.id
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s", callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Sá´‡ÊŸá´‡á´„á´› âž¢', 'select'),
                InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Sá´‡á´€sá´É´s", callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Sá´›á´€Ê€á´› Bá´á´›", url=f"https://telegram.me/{temp.U_NAME}"),
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}")
        ])
    if offset != "":
        req = message.from_user.id if message.from_user else 0
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ðð„ð—ð“ âžª",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="ððŽ ðŒðŽð‘ð„ ðð€ð†ð„ð’ ð€ð•ð€ðˆð‹ð€ðð‹ð„",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
    remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
    TEMPLATE = script.IMDB_TEMPLATE_TXT
    if imdb:
        cap = TEMPLATE.format(
            qurey=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
        temp.IMDB_CAP[message.from_user.id] = cap
        if not settings["button"]:
            cap+="<b>\n\n<u>ðŸ¿ Your Movie Files ðŸ‘‡</u></b>\n"
            for file in files:
                cap += f"<b>\nðŸ“ <a href='https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n</a></b>"
    else:
        if settings["button"]:
            cap = f"<b>TÊœá´‡ Rá´‡êœ±á´œÊŸá´›êœ± Fá´Ê€ â˜ž {search}\n\nRá´‡Ç«á´œá´‡sá´›á´‡á´… BÊ â˜ž {message.from_user.mention}\n\nÊ€á´‡sá´œÊŸá´› sÊœá´á´¡ ÉªÉ´ â˜ž {remaining_seconds} sá´‡á´„á´É´á´…s\n\ná´˜á´á´¡á´‡Ê€á´‡á´… Ê™Ê â˜ž : {message.chat.title} \n\nâš ï¸ á´€êœ°á´›á´‡Ê€ 5 á´ÉªÉ´á´œá´›á´‡êœ± á´›ÊœÉªêœ± á´á´‡êœ±êœ±á´€É¢á´‡ á´¡ÉªÊŸÊŸ Ê™á´‡ á´€á´œá´›á´á´á´€á´›Éªá´„á´€ÊŸÊŸÊ á´…á´‡ÊŸá´‡á´›á´‡á´… ðŸ—‘ï¸\n\n</b>"
        else:
            cap = f"<b>TÊœá´‡ Rá´‡êœ±á´œÊŸá´›êœ± Fá´Ê€ â˜ž {search}\n\nRá´‡Ç«á´œá´‡sá´›á´‡á´… BÊ â˜ž {message.from_user.mention}\n\nÊ€á´‡sá´œÊŸá´› sÊœá´á´¡ ÉªÉ´ â˜ž {remaining_seconds} sá´‡á´„á´É´á´…s\n\ná´˜á´á´¡á´‡Ê€á´‡á´… Ê™Ê â˜ž : {message.chat.title} \n\nâš ï¸ á´€êœ°á´›á´‡Ê€ 5 á´ÉªÉ´á´œá´›á´‡êœ± á´›ÊœÉªêœ± á´á´‡êœ±êœ±á´€É¢á´‡ á´¡ÉªÊŸÊŸ Ê™á´‡ á´€á´œá´›á´á´á´€á´›Éªá´„á´€ÊŸÊŸÊ á´…á´‡ÊŸá´‡á´›á´‡á´… ðŸ—‘ï¸\n\n</b>"
            cap+="<b><u>ðŸ¿ Your Movie Files ðŸ‘‡</u></b>\n\n"
            for file in files:
                cap += f"<b>ðŸ“ <a href='https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"

    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await hehe.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(300)
                await hehe.delete()
                await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg") 
            hmm = await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
               if settings['auto_delete']:
                    await asyncio.sleep(300)
                    m=await message.reply_text("ðŸ”Ž")
                    await hmm.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(300)
                await hmm.delete()
                await message.delete()
        except Exception as e:
            logger.exception(e)
            m=await message.reply_text("ðŸ”Ž") 
            fek = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await fek.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(300)
                await fek.delete()
                await message.delete()
    else:
        fuk = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        await m.delete()
        try:
            if settings['auto_delete']:
                await asyncio.sleep(300)
                await fuk.delete()
                await message.delete()
        except KeyError:
            await save_group_settings(message.chat.id, 'auto_delete', True)
            await asyncio.sleep(300)
            await fuk.delete()
            await message.delete()


async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    find = mv_rqst.split(" ")
    query = ""
    removes = ["in","upload", "series", "full", "horror", "thriller", "mystery", "print", "file"]
    for x in find:
        if x in removes:
            continue
        else:
            query = query + x + " "
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\s+", " ", query).strip() + "movie"
    try:
        g_s = await search_gagala(query)
        g_s += await search_gagala(msg.text)
        gs_parsed = []
        if not g_s:
            reqst_gle = query.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gá´á´É¢ÊŸá´‡", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
        gs = list(filter(regex.match, g_s))
        gs_parsed = [re.sub(
            r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
            '', i, flags=re.IGNORECASE) for i in gs]
        if not gs_parsed:
            reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                             re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
            for mv in g_s:
                match = reg.match(mv)
                if match:
                    gs_parsed.append(match.group(1))
        movielist = []
        gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
        if len(gs_parsed) > 3:
            gs_parsed = gs_parsed[:3]
        if gs_parsed:
            for mov in gs_parsed:
                imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
                if imdb_s:
                    movielist += [movie.get('title') for movie in imdb_s]
        movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
        movielist = list(dict.fromkeys(movielist))  # removing duplicates
        if not movielist:
            reqst_gle = query.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gá´á´É¢ÊŸá´‡", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        SPELL_CHECK[mv_id] = movielist
        btn = [[
            InlineKeyboardButton(
                text=movie.strip(),
                callback_data=f"spolling#{reqstr1}#{k}",
            )
        ] for k, movie in enumerate(movielist)]
        btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
        spell_check_del = await msg.reply_photo(
            photo=(SPELL_IMG),
            caption=(script.CUDNT_FND.format(mv_rqst)),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        try:
            if settings['auto_delete']:
                await asyncio.sleep(60)
                await spell_check_del.delete()
        except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(60)
                    await spell_check_del.delete()
    except:
        try:
            movies = await get_poster(mv_rqst, bulk=True)
        except Exception as e:
            logger.exception(e)
            reqst_gle = mv_rqst.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gá´á´É¢ÊŸá´‡", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        movielist = []
        if not movies:
            reqst_gle = mv_rqst.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gá´á´É¢ÊŸá´‡", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        movielist += [movie.get('title') for movie in movies]
        movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies]
        SPELL_CHECK[mv_id] = movielist
        btn = [
            [
                InlineKeyboardButton(
                    text=movie_name.strip(),
                    callback_data=f"spol#{reqstr1}#{k}",
                )
            ]
            for k, movie_name in enumerate(movielist)
        ]
        btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
        spell_check_del = await msg.reply_photo(
            photo=(SPELL_IMG),
            caption=(script.CUDNT_FND.format(mv_rqst)),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        try:
            if settings['auto_delete']:
                await asyncio.sleep(600)
                await spell_check_del.delete()
        except KeyError:
                grpid = await active_connection(str(msg.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(msg.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await spell_check_del.delete()


async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            
                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                                
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
