from aiogram import types, F, Router, Bot
from bot.keyboards import back_keyboard
from aiosqlitedatabase.database import get_user, switch_off_send_mode_by_id, switch_on_send_mode_by_id
from bot.compliments.send_compliment import Compliment
import asyncio

router = Router()


@router.callback_query(F.data == "contacts")
async def contacts_handler(call: types.CallbackQuery, bot: Bot) -> None:
    await call.message.edit_text(f"My contacts: @BratkoVictor",
                                 reply_markup=back_keyboard)


@router.callback_query(F.data == "about_project")
async def about_handler(call: types.CallbackQuery) -> None:
    await call.message.edit_text(f"Some information about project:{call.message.from_user.full_name}",
                                 reply_markup=back_keyboard)


@router.callback_query(F.data == "send_mode")
async def send_mode_handler(call: types.CallbackQuery) -> None:
    send_mode_keyboard_list = [
        [
            types.InlineKeyboardButton(text="Back", callback_data='menu')
        ]
    ]
    user = await get_user(call.from_user.id)
    try:
        user_mode = user[-1]
    except:
        await call.message.edit_text("You are not a user. Write /start, please", reply_markup=back_keyboard)
        return

    if user_mode:
        send_mode_keyboard_list.append([types.InlineKeyboardButton(text="Switch off",
                                                                   callback_data='send_mode_switch_off')])
        mode = "on"
    else:
        send_mode_keyboard_list.append([types.InlineKeyboardButton(text="Switch on",
                                                                   callback_data='send_mode_switch_on')])
        mode = "off"
    send_mode_keyboard = types.InlineKeyboardMarkup(inline_keyboard=send_mode_keyboard_list)
    await call.message.edit_text(f"Currently your send mode: {mode}", reply_markup=send_mode_keyboard)


@router.callback_query(F.data == "send_mode_switch_off")
async def send_mode_switch_off(call: types.CallbackQuery):
    await switch_off_send_mode_by_id([call.from_user.id])
    await send_mode_handler(call)


@router.callback_query(F.data == "send_mode_switch_on")
async def send_mode_switch_on(call: types.CallbackQuery):
    await switch_on_send_mode_by_id([call.from_user.id])
    await send_mode_handler(call)


@router.callback_query(F.data == "send_compliment")
async def send_compliment(call: types.CallbackQuery, bot: Bot):
    compliment = Compliment()
    asyncio.create_task(compliment.send_compliment(call.from_user.id, bot))


@router.message(F.text)
async def print_text(message: types.Message):
    print(message.text)
