import random
import string
from bot.config import config


class PasswordGenerator:
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate_password(self, settings: dict) -> str:
        characters = ""

        if settings['use_uppercase']:
            characters += self.uppercase
        if settings['use_lowercase']:
            characters += self.lowercase
        if settings['use_digits']:
            characters += self.digits
        if settings['use_special']:
            characters += self.special

        # Если ничего не выбрано, используем буквы и цифры по умолчанию
        if not characters:
            characters = self.lowercase + self.digits

        # Генерируем пароль
        password = ''.join(random.choice(characters) for _ in range(settings['length']))

        # Проверяем, что пароль содержит хотя бы один символ из каждого выбранного типа
        if settings['use_uppercase'] and not any(c in self.uppercase for c in password):
            password = self._ensure_character_type(password, self.uppercase, settings)
        if settings['use_lowercase'] and not any(c in self.lowercase for c in password):
            password = self._ensure_character_type(password, self.lowercase, settings)
        if settings['use_digits'] and not any(c in self.digits for c in password):
            password = self._ensure_character_type(password, self.digits, settings)
        if settings['use_special'] and not any(c in self.special for c in password):
            password = self._ensure_character_type(password, self.special, settings)

        return password

    def _ensure_character_type(self, password: str, char_set: str, settings: dict) -> str:
        """Гарантирует, что пароль содержит хотя бы один символ из указанного набора"""
        password_list = list(password)
        # Заменяем случайный символ на символ из нужного набора
        index = random.randint(0, len(password_list) - 1)
        password_list[index] = random.choice(char_set)
        return ''.join(password_list)


password_generator = PasswordGenerator()