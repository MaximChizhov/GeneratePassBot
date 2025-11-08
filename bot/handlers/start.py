from bot.keyboards import main_menu
from bot import telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class StartHandler(Handler):
    def can_handle(self, update: dict, state: str, user_data: dict) -> bool:
        if "message" not in update:
            return False

        message = update["message"]
        if "entities" not in message:
            return False

        return (message["entities"][0]["type"] == "bot_command" and
                message["text"].split()[0] == "/start")

    def handle(self, update: dict, state: str, user_data: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]

        telegram_client.send_message(
            chat_id,
            "👋 Привет! Я бот для генерации паролей.\n\n"
            "Нажми 'Сгенерировать пароль' чтобы начать!",
            reply_markup=main_menu()
        )
        return HandlerStatus.STOP


class BackHandler(Handler):
    def can_handle(self, update: dict, state: str, user_data: dict) -> bool:
        if "message" not in update:
            return False

        message = update["message"]
        return "text" in message and message["text"] == "⬅️ Назад"

    def handle(self, update: dict, state: str, user_data: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]

        telegram_client.send_message(
            chat_id,
            "Главное меню:",
            reply_markup=main_menu()
        )
        return HandlerStatus.STOP