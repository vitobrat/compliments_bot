from aiogram import types, F, Router, Bot
from bot.keyboards import back_keyboard

router = Router()


@router.callback_query(F.data == "contacts")
@router.message(F.text == "Contacts")
async def contacts_handler(update) -> None:
    if isinstance(update, types.Message):
        await update.edit_text(f"My contacts:{(await bot.get_me()).full_name}")
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"My contacts:{(await bot.get_me()).full_name}", reply_markup=back_keyboard)


@router.callback_query(F.data == "about_project")
@router.message(F.text == "About project")
async def about_handler(update) -> None:
    if isinstance(update, types.Message):
        await update.edit_text(f"Some information about project:{update.from_user.full_name}")
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"Some information about project:{update.message.from_user.full_name}", reply_markup=back_keyboard)
