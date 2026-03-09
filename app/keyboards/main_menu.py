from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Профиль"), KeyboardButton(text="Каталог")],
            [KeyboardButton(text="Пополнить"), KeyboardButton(text="Рейтинг")],
            [KeyboardButton(text="Сделать заказ")],
            [KeyboardButton(text="Поддержка"), KeyboardButton(text="Регламент")],
        ],
        resize_keyboard=True,
    )
