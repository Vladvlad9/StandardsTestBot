from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData

main_cb = CallbackData("main", "target", "id", "editId", "count")


class RegistrationForms:
    @staticmethod
    async def open_site_kb() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Регистрация',
                                   web_app=WebAppInfo(url="https://starlit-faloodeh-d05fb5.netlify.app" + "/form")
                                   )
                ]
            ]
        )