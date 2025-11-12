from bot import telegram_client
from bot.settings import get_user_settings
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards import password_options_menu


class ToggleHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        if "callback_query" not in update:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("toggle_")

    def handle(self, update: dict) -> HandlerStatus:
        callback_query = update["callback_query"]
        user_id = callback_query["from"]["id"]
        message = callback_query["message"]
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        settings = get_user_settings(user_id)
        callback_data = callback_query["data"]

        key = callback_data.replace("toggle_", "")
        settings[key] = not settings[key]

        telegram_client.edit_message_text(
            chat_id,
            message_id,
            "⚙️ Настрой параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        telegram_client.answer_callback_query(callback_query["id"])
        return HandlerStatus.STOP