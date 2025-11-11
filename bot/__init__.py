from .telegram_client import (
    get_updates,
    send_message,
    edit_message_text,
    answer_callback_query,
    delete_message
)

__all__ = [
    'get_updates',
    'send_message',
    'edit_message_text',
    'answer_callback_query',
    'delete_message'
]