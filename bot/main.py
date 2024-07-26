from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio

dp = Dispatcher()
#1044539451

back_keyboard = [
    [
        types.InlineKeyboardButton(text="Back", callback_data='menu')
    ],
]
menu_keyboard = [
    [types.InlineKeyboardButton(text="Contacts", callback_data="contacts"),],
    [types.InlineKeyboardButton(text="About project", callback_data="about_project")],
]


@dp.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """
    handler of command /start; print some start information
    :param message: obj message, consist information about user
    :return: None
    """
    await message.answer("Welcome, nahui")
    print(message.from_user.id)


@dp.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """
    handler of command /help; print useful information
    :param message: obj message, consist information about user
    :return: None
    """
    await message.answer("This is project about...\n"
                         "There are some useful commands:")


@dp.callback_query(F.data == "contacts")
@dp.message(F.text == "Contacts")
async def contacts_handler(update, bot: Bot) -> None:

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=back_keyboard)
    if isinstance(update, types.Message):
        await update.edit_text(f"My contacts:{(await bot.get_me()).full_name}")
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"My contacts:{(await bot.get_me()).full_name}", reply_markup=keyboard)


@dp.callback_query(F.data == "about_project")
@dp.message(F.text == "About project")
async def about_handler(update) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=back_keyboard)
    if isinstance(update, types.Message):
        await update.edit_text(f"Some information about project:{update.from_user.full_name}")
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"Some information about project:{update.message.from_user.full_name}", reply_markup=keyboard)


@dp.callback_query(F.data == "menu")
@dp.message(Command("menu"))
async def menu_command(update) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_keyboard)

    if isinstance(update, types.Message):
        await update.answer(f"Menu:", reply_markup=keyboard)
    elif isinstance(update, types.CallbackQuery):
        await update.message.edit_text(f"Menu:", reply_markup=keyboard)


async def main() -> None:
    TOKEN = "7260863728:AAGaCtZX8M1L1Pbw6gqy_1XitdyU9noPwn4"
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
