from aiogram import types, F, Router
from aiogram.filters import Command
from bot.keyboards import menu_keyboard
from aiosqlitedatabase.database import add_user

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """
    handler of command /start; print some start information
    :param message: obj message, consist information about user
    :return: None
    """
    await message.answer("Welcome, nahui")
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    print(message.from_user.id, message.from_user.full_name)


@router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """
    handler of command /help; print useful information
    :param message: obj message, consist information about user
    :return: None
    """
    await message.answer("This is project about...\n"
                         "There are some useful commands:")


@router.callback_query(F.data == "menu")
@router.message(Command("menu"))
async def menu_command(update) -> None:
    if isinstance(update, types.Message):
        await update.answer(f"Menu:", reply_markup=menu_keyboard)
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"Menu:", reply_markup=menu_keyboard)