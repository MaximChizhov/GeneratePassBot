from bot.config import config
from bot.keyboards import password_options_menu, main_menu
from bot import telegram_client
from bot.generate_password import password_generator
from bot.handlers.handler import Handler, HandlerStatus

# Временное хранилище настроек пользователей
user_settings = {}


def get_user_settings(user_id):
    if user_id not in user_settings:
        user_settings[user_id] = {
            'length': config.DEFAULT_LENGTH,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': False
        }
    return user_settings[user_id]


class GeneratePasswordHandler(Handler):
    def can_handle(self, update: dict, state: str, user_data: dict) -> bool:
        if "message" not in update:
            return False

        message = update["message"]
        return "text" in message and message["text"] == "🔐 Сгенерировать пароль"

    def handle(self, update: dict, state: str, user_data: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]
        settings = get_user_settings(chat_id)

        telegram_client.send_message(
            chat_id,
            "⚙️ Настрой параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        return HandlerStatus.STOP


class CallbackHandler(Handler):
    def can_handle(self, update: dict, state: str, user_data: dict) -> bool:
        return "callback_query" in update

    def handle(self, update: dict, state: str, user_data: dict) -> HandlerStatus:
        callback_query = update["callback_query"]
        user_id = callback_query["from"]["id"]
        message = callback_query["message"]
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        callback_data = callback_query["data"]

        settings = get_user_settings(user_id)

        if callback_data == "length_incr" and settings['length'] < config.MAX_LENGTH:
            settings['length'] += 1
        elif callback_data == "length_decr" and settings['length'] > config.MIN_LENGTH:
            settings['length'] -= 1
        elif callback_data.startswith("toggle_"):
            key = callback_data.replace("toggle_", "")
            settings[key] = not settings[key]
        elif callback_data == "generate_password":
            password = password_generator.generate_password(settings)
            password_info = (
                f"🔐 Ваш пароль:\n\n"
                f"`{password}`\n\n"
                f"📊 Параметры:\n"
                f"• Длина: {settings['length']} символов\n"
                f"• Большие буквы: {'✅' if settings['use_uppercase'] else '❌'}\n"
                f"• Маленькие буквы: {'✅' if settings['use_lowercase'] else '❌'}\n"
                f"• Цифры: {'✅' if settings['use_digits'] else '❌'}\n"
                f"• Символы: {'✅' if settings['use_special'] else '❌'}\n\n"
                f"💡 Скопируйте пароль выше"
            )
            telegram_client.send_message(chat_id, password_info, reply_markup=main_menu())
            telegram_client.answer_callback_query(callback_query["id"])
            return HandlerStatus.STOP

        telegram_client.edit_message_text(
            chat_id,
            message_id,
            "⚙️ Настрой параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        telegram_client.answer_callback_query(callback_query["id"])
        return HandlerStatus.STOP