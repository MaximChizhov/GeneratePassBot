import requests
from bot.config import config


def get_updates(offset: int = 0, timeout: int = 30):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": timeout}
    response = requests.get(url, params=params)
    return response.json()


def send_message(chat_id: int, text: str, reply_markup=None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    response = requests.post(url, json=payload)
    return response.json()


def edit_message_text(chat_id: int, message_id: int, text: str, reply_markup=None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    response = requests.post(url, json=payload)
    return response.json()


def answer_callback_query(callback_query_id: str, text: str = None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/answerCallbackQuery"
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text

    response = requests.post(url, json=payload)
    return response.json()


def delete_message(chat_id: int, message_id: int):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }

    response = requests.post(url, json=payload)
    return response.json()