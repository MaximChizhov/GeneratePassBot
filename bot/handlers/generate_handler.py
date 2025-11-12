from bot import telegram_client
from bot.settings import get_user_settings
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards import password_options_menu


class GeneratePasswordHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        if "message" not in update:
            return False

        message = update["message"]
        return "text" in message and message["text"] == "🔐 Сгенерировать пароль"

    def handle(self, update: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]
        settings = get_user_settings(chat_id)

        telegram_client.send_message(
            chat_id,
            "⚙️ Настройте параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        return HandlerStatus.STOP