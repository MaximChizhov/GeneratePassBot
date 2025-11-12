import urllib.request
import urllib.parse
import json
from bot.config import config


def get_updates(offset: int = 0, timeout: int = 3):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": timeout}

    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    with urllib.request.urlopen(full_url) as response:
        data = response.read().decode('utf-8')
        return json.loads(data)


def send_message(chat_id: int, text: str, parse_mode: str = None, reply_markup=None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    request = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result


def edit_message_text(chat_id: int, message_id: int, text: str, reply_markup=None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    request = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode('utf-8'))


def answer_callback_query(callback_query_id: str, text: str = None):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/answerCallbackQuery"
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text

    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    request = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode('utf-8'))


def delete_message(chat_id: int, message_id: int):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }

    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    request = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode('utf-8'))