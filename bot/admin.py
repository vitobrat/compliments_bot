from aiogram import types, F, Router
from aiogram.filters import Command
from bot.keyboards import admin_keyboard, back_admin_keyboard
from bot.my_filters import AdminFilter
from aiosqlitedatabase.database import get_all_users, count_users

router = Router()


@router.callback_query(F.data == "admin_panel", AdminFilter())
@router.message(Command("admin"), AdminFilter())
async def admin_cmd(update):
    if isinstance(update, types.Message):
        await update.answer("Admin panel", reply_markup=admin_keyboard)
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text("Admin panel", reply_markup=admin_keyboard)

@router.callback_query(F.data == "admin_statistic", AdminFilter())
async def admin_statistic(call: types.CallbackQuery) -> None:
    users = "\n".join([f"{i}) ID - {user[0]}; Full name - {user[1]}; User name - {user[2]}; Admin - {user[3]}" for i, user in enumerate(await get_all_users())])
    await call.message.edit_text(f"Users: {users}\n"
                                 f"Users count: {await count_users()}", reply_markup=back_admin_keyboard)

@router.callback_query(F.data == 'admin_newsletter', AdminFilter())
async def admin_newsletter(call: types.CallbackQuery):
    await call.message.edit_text('News letter for all users\n\nInput the message:', reply_markup=back_admin_keyboard)