from asyncio import sleep
from contextlib import suppress

from aiogram import types, F, Router
from aiogram.filters import Command
from bot.keyboards import admin_keyboard, back_admin_keyboard
from bot.my_filters import AdminFilter
from aiosqlitedatabase.database import (get_all_users, count_users, get_all_users_id_with_send_mode,
                                        switch_on_send_mode_by_id, switch_off_send_mode_by_id)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class AdminState(StatesGroup):
    newsletter = State()
    input_ids = State()


async def all_users():
    return "\n".join([f"{i}) ID - {user[0]}; Full name - {user[1]}; User name - {user[2]};"
                      f" Send mode - {user[3]}" for i, user in enumerate(await get_all_users())])


@router.callback_query(F.data == "admin_panel", AdminFilter())
@router.message(Command("admin"), AdminFilter())
async def admin_cmd(update, state: FSMContext):
    await state.clear()
    if isinstance(update, types.Message):
        await update.answer("Admin panel", reply_markup=admin_keyboard)
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text("Admin panel", reply_markup=admin_keyboard)


@router.callback_query(F.data == "admin_statistic", AdminFilter())
async def admin_statistic(call: types.CallbackQuery) -> None:
    await call.message.edit_text(f"Users: {await all_users()}\n"
                                 f"Users count: {await count_users()}", reply_markup=back_admin_keyboard)


@router.callback_query(F.data == 'admin_newsletter', AdminFilter())
async def admin_newsletter(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('News letter for all users\n\n'
                                 'Input the message:', reply_markup=back_admin_keyboard)
    await state.set_state(AdminState.newsletter)


@router.callback_query(F.data == 'admin_send_mode_off', AdminFilter())
async def admin_send_mode_on(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Input ids list whose you want to switch off send mode (separated by a space):\n\n'
                                 f'Users: {await all_users()}',
                                 reply_markup=back_admin_keyboard)
    await state.set_state(AdminState.input_ids)
    await state.set_data({"mode": 0})


@router.callback_query(F.data == 'admin_send_mode_on', AdminFilter())
async def admin_send_mode_on(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Input ids list whose you want to switch on send mode (separated by a space):\n\n'
                                 f'Users: {await all_users()}',
                                 reply_markup=back_admin_keyboard)
    await state.set_state(AdminState.input_ids)
    await state.set_data({"mode": 1,
                          "message": call.message})


@router.message(AdminState.input_ids, AdminFilter())
async def admin_send_mode_step_2(message: types.Message, state: FSMContext):
    ids = message.text.split()
    print(ids)
    state_data = await state.get_data()
    if state_data.get("mode"):
        await switch_on_send_mode_by_id(ids)
    else:
        await switch_off_send_mode_by_id(ids)
    await state_data.get("message").edit_text(f"Users: {await all_users()}\n",
                                              reply_markup=back_admin_keyboard)
    await state.clear()


@router.message(AdminState.newsletter, AdminFilter())
async def admin_newsletter_step_2(message: types.Message, state: FSMContext):
    users_id = [id[0] for id in await get_all_users_id_with_send_mode()]
    await state.update_data(message_newsletter=message)
    for id in users_id:
        with suppress():
            await message.send_copy(id)
            await sleep(0.3)
    await state.clear()
