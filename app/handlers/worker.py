from aiogram import F, Router
from aiogram.types import Message

router = Router(name="worker")


@router.message(F.text == "Встать в работу")
async def start_shift(message: Message) -> None:
    await message.answer("Смена открыта. Теперь вам могут назначаться новые заказы.")


@router.message(F.text == "Завершить смену")
async def end_shift(message: Message) -> None:
    await message.answer("Смена завершена. Новые заказы не будут назначаться.")
