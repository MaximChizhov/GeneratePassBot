from bot.keyboards import main_menu
from bot import telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class HelpHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        if "message" not in update:
            return False

        message = update["message"]
        return "text" in message and message["text"] == "ℹ️ Помощь"

    def handle(self, update: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]

        telegram_client.send_message(
            chat_id,
            "ℹ️ Помощь по боту:\n\n"
            "• 🔐 Сгенерировать пароль - создание пароля с настройками. Диапазон: 6 - 20 символов\n"
            "• ℹ️ Помощь - это сообщение\n\n"
            "Просто нажми 'Сгенерировать пароль' и выбери нужные параметры!",
            reply_markup=main_menu()
        )
        return HandlerStatus.STOP