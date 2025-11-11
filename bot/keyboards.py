def main_menu():
    return {
        "keyboard": [
            [{"text": "🔐 Сгенерировать пароль"}],
            [{"text": "ℹ️ Помощь"}]
        ],
        "resize_keyboard": True
    }


def back_button():
    return {
        "keyboard": [
            [{"text": "⬅️ Назад"}]
        ],
        "resize_keyboard": True
    }


def password_options_menu(current_settings):
    inline_keyboard = []

    # Длина пароля
    inline_keyboard.append([
        {"text": f"📏 Длина пароля: {current_settings['length']}", "callback_data": "length_display"}
    ])

    # Кнопки изменения длины
    inline_keyboard.append([
        {"text": "➖ Уменьшить", "callback_data": "length_decr"},
        {"text": "➕ Увеличить", "callback_data": "length_incr"}
    ])

    # Чекбоксы
    options = {
        "use_uppercase": "🔠 Большие буквы",
        "use_lowercase": "🔡 Маленькие буквы",
        "use_digits": "🔢 Цифры",
        "use_special": "🔣 Символы"
    }

    for key, text in options.items():
        icon = "✅" if current_settings[key] else "❌"
        inline_keyboard.append([
            {"text": f"{icon} {text}", "callback_data": f"toggle_{key}"}
        ])

    # Кнопки генерации
    inline_keyboard.append([
        {"text": "🎲 Сгенерировать 1 пароль", "callback_data": "generate_single"}
    ])
    inline_keyboard.append([
        {"text": "🚀 Сгенерировать 10 паролей", "callback_data": "generate_multiple"}
    ])

    return {"inline_keyboard": inline_keyboard}