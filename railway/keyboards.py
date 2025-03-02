from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="admin ➕"),
            KeyboardButton(text="admin ➖")
        ],

        [
            KeyboardButton(text="kanal ➕"),
            KeyboardButton(text="kanal ➖")
        ],
        [
            KeyboardButton(text="Post ✉️"),
        ]

    ], resize_keyboard=True)
    return main_menu_keyboard
