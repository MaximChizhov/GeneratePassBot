import random
import string
import math


class PasswordGenerator:
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate_password(self, settings: dict) -> str:
        characters = ""
        required_sets = []

        # Собираем доступные символы и обязательные типы
        if settings["use_uppercase"]:
            characters += self.uppercase
            required_sets.append(self.uppercase)
        if settings["use_lowercase"]:
            characters += self.lowercase
            required_sets.append(self.lowercase)
        if settings["use_digits"]:
            characters += self.digits
            required_sets.append(self.digits)
        if settings["use_special"]:
            characters += self.special
            required_sets.append(self.special)

        # Если ничего не выбрано, используем буквы и цифры по умолчанию
        if not characters:
            characters = self.lowercase + self.digits
            required_sets = [self.lowercase, self.digits]

        # Создаем список для пароля
        password = []

        # На первые позиции ставим по одному символу из каждого обязательного типа
        for i, char_set in enumerate(required_sets):
            if i < settings["length"]:  # Проверяем, что длина пароля позволяет
                password.append(random.choice(char_set))

        # Заполняем оставшиеся позиции случайными символами из общего набора
        remaining_length = settings["length"] - len(password)
        if remaining_length > 0:
            password.extend(random.choices(characters, k=remaining_length))

        # Перемешиваем пароль для случайности
        random.shuffle(password)

        return ''.join(password)

    def calculate_entropy(self, settings: dict) -> float:
        charset_size = 0

        if settings["use_lowercase"]:
            charset_size += 26
        if settings["use_uppercase"]:
            charset_size += 26
        if settings["use_digits"]:
            charset_size += 10
        if settings["use_special"]:
            charset_size += len(self.special)

        if charset_size == 0:
            return 0

        entropy = settings["length"] * math.log2(charset_size)
        return round(entropy, 1)

    def get_strength_rating(self, entropy: float) -> tuple:
        if entropy < 28:
            return ("Очень слабый", "🔴")
        elif entropy < 36:
            return ("Слабый", "🟠")
        elif entropy < 60:
            return ("Средний", "🟡")
        elif entropy < 80:
            return ("Сильный", "🟢")
        else:
            return ("Очень сильный", "🔵")

    def generate_multiple_passwords(self, settings: dict, count: int = 10) -> list:
        return [self.generate_password(settings) for _ in range(count)]


password_generator = PasswordGenerator()
