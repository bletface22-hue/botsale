from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main_menu import main_menu

router = Router(name="user")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Добро пожаловать в BotSale", reply_markup=main_menu())


@router.message(F.text == "Каталог")
async def open_catalog(message: Message) -> None:
    await message.answer("Каталог загружается. В этой версии добавлен каркас каталога/заказов/выдачи.")


@router.message(F.text == "Регламент")
async def regulations(message: Message) -> None:
    await message.answer("Регламент: соблюдайте условия сервиса и правила общения.")
