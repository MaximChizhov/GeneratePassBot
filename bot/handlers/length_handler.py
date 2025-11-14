from bot import telegram_client
from bot.settings import get_user_settings
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards import password_options_menu
from bot.config import config


class LengthHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        if "callback_query" not in update:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["length_incr", "length_decr"]

    def handle(self, update: dict) -> HandlerStatus:
        callback_query = update["callback_query"]
        user_id = callback_query["from"]["id"]
        message = callback_query["message"]
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        settings = get_user_settings(user_id)
        callback_data = callback_query["data"]

        if callback_data == "length_incr" and settings["length"] < config.MAX_LENGTH:
            settings["length"] += 1
        elif callback_data == "length_decr" and settings["length"] > config.MIN_LENGTH:
            settings["length"] -= 1

        telegram_client.edit_message_text(
            chat_id,
            message_id,
            "⚙️ Настрой параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        telegram_client.answer_callback_query(callback_query["id"])
        return HandlerStatus.STOP