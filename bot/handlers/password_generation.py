import threading
import time
from bot import telegram_client
from bot.settings import get_user_settings
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards import main_menu
from bot.generate_password import password_generator
import html


def delete_message_after_delay(chat_id: int, message_id: int, delay: int = 15):
    def delete():
        time.sleep(delay)
        telegram_client.delete_message(chat_id, message_id)

    thread = threading.Thread(target=delete)
    thread.daemon = True
    thread.start()


class GenerateHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        if "callback_query" not in update:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["generate_single", "generate_multiple"]

    def handle(self, update: dict) -> HandlerStatus:
        callback_query = update["callback_query"]
        user_id = callback_query["from"]["id"]
        message = callback_query["message"]
        chat_id = message["chat"]["id"]

        settings = get_user_settings(user_id)
        callback_data = callback_query["data"]

        # Рассчитываем энтропию для оценки надежности
        entropy = password_generator.calculate_entropy(settings)
        strength, color = password_generator.get_strength_rating(entropy)

        # Генерируем пароли
        if callback_data == "generate_single":
            passwords = [password_generator.generate_password(settings)]
            title = "🔐 Сгенерированный пароль:"
        else:  # generate_multiple
            passwords = password_generator.generate_multiple_passwords(settings, 10)
            title = "🔐 10 сгенерированных паролей:"

        # Формируем список паролей
        password_list = "\n\n".join([
            f"<pre>{html.escape(password)}</pre>" for i, password in enumerate(passwords)
        ])

        # Создаем текст сообщения
        password_text = (
            f"{title}\n\n"
            f"{password_list}\n\n"
            f"📊 Надежность: {color} {strength}\n"
            f"📏 Длина: {settings['length']} символов\n\n"
            f"⏰ Сообщение удалится через 15 секунд"
        )

        # Отправляем сообщение
        result = telegram_client.send_message(chat_id, password_text, parse_mode="HTML", reply_markup=main_menu())
        telegram_client.answer_callback_query(callback_query["id"])

        # Удаляем сообщение через 15 секунд
        if "result" in result and "message_id" in result["result"]:
            delete_message_after_delay(chat_id, result["result"]["message_id"], 15)

        return HandlerStatus.STOP