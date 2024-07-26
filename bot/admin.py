from aiogram import types, F, Router
from aiogram.filters import Command
from bot.keyboards import admin_keyboard, back_admin_keyboard
from bot.my_filters import AdminFilter

router = Router()


class Admin:
    @router.callback_query(F.data == "admin_panel")
    @router.message(Command("admin"), AdminFilter())
    async def admin_cmd(message: types.Message):
        await message.answer("Admin panel", reply_markup=admin_keyboard)

    @router.callback_query(F.data == "admin_statistic", AdminFilter())
    async def admin_statistic(call: types.CallbackQuery) -> None:
        await call.message.edit_text(f"Users count: {1}", reply_markup=back_admin_keyboard)