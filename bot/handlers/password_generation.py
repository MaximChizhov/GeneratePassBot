import threading
import time
from bot.config import config
from bot.keyboards import password_options_menu, main_menu
from bot import telegram_client
from bot.handlers.handler import Handler, HandlerStatus
from bot.generate_password import password_generator

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


def delete_message_after_delay(chat_id: int, message_id: int, delay: int = 15):
    """Удаляет сообщение через указанное количество секунд"""

    def delete():
        time.sleep(delay)
        telegram_client.delete_message(chat_id, message_id)

    thread = threading.Thread(target=delete)
    thread.daemon = True
    thread.start()


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
        elif callback_data in ["generate_single", "generate_multiple"]:
            self._handle_password_generation(callback_query, settings, callback_data)
            return HandlerStatus.STOP

        # Обновляем сообщение с новыми настройками
        telegram_client.edit_message_text(
            chat_id,
            message_id,
            "⚙️ Настрой параметры пароля:",
            reply_markup=password_options_menu(settings)
        )
        telegram_client.answer_callback_query(callback_query["id"])
        return HandlerStatus.STOP

    def _handle_password_generation(self, callback_query, settings, generate_type):
        """Обрабатывает генерацию паролей"""
        message = callback_query["message"]
        chat_id = message["chat"]["id"]

        # Рассчитываем энтропию для оценки надежности
        entropy = password_generator.calculate_entropy(settings)
        strength, color = password_generator.get_strength_rating(entropy)

        # Генерируем пароли
        if generate_type == "generate_single":
            passwords = [password_generator.generate_password(settings)]
            title = "🔐 Сгенерированный пароль:"
        else:  # generate_multiple
            passwords = password_generator.generate_multiple_passwords(settings, 10)
            title = "🔐 10 сгенерированных паролей:"

        # Формируем список паролей (БЕЗ кавычек)
        password_list = "\n\n".join([
            f"{i + 1}. {password}" for i, password in enumerate(passwords)
        ])

        # Создаем текст сообщения (БЕЗ энтропии)
        password_text = (
            f"{title}\n\n"
            f"{password_list}\n\n"
            f"📊 Надежность: {color} {strength}\n"
            f"📏 Длина: {settings['length']} символов\n\n"
            f"⏰ Сообщение удалится через 15 секунд"
        )

        # Отправляем сообщение
        result = telegram_client.send_message(chat_id, password_text, reply_markup=main_menu())
        telegram_client.answer_callback_query(callback_query["id"])

        # Удаляем сообщение через 15 секунд
        if "result" in result and "message_id" in result["result"]:
            delete_message_after_delay(chat_id, result["result"]["message_id"], 15)