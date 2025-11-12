from bot.config import config

# Глобальное хранилище настроек пользователей
_user_settings = {}

def get_user_settings(user_id: int) -> dict:

    if user_id not in _user_settings:
        _user_settings[user_id] = {
            'length': config.DEFAULT_LENGTH,
            'use_uppercase': False,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': False
        }
    return _user_settings[user_id]