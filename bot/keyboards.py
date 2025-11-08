def main_menu():
    markup = {
        "keyboard": [
            [{"text": "🔐 Сгенерировать пароль"}],
            [{"text": "ℹ️ Помощь"}]
        ],
        "resize_keyboard": True
    }
    return markup


def back_button():
    markup = {
        "keyboard": [
            [{"text": "⬅️ Назад"}]
        ],
        "resize_keyboard": True
    }
    return markup


def password_options_menu(current_settings):
    markup = {
        "inline_keyboard": [
            # Длина пароля - отдельная строка
            [{"text": f"📏 Длина пароля: {current_settings['length']}", "callback_data": "length_display"}],

            # Кнопки - и + на одной строке
            [
                {"text": "➖ Уменьшить", "callback_data": "length_decr"},
                {"text": "➕ Увеличить", "callback_data": "length_incr"}
            ],

            # Чекбоксы
            *[
                [{
                    "text": f"{'✅' if current_settings[key] else '❌'} {text}",
                    "callback_data": f"toggle_{key}"
                }]
                for key, text in {
                    "use_uppercase": "🔠 Большие буквы",
                    "use_lowercase": "🔡 Маленькие буквы",
                    "use_digits": "🔢 Цифры",
                    "use_special": "🔣 Символы"
                }.items()
            ],

            # Кнопка генерации
            [{"text": "🎲 Сгенерировать пароль", "callback_data": "generate_password"}]
        ]
    }
    return markup