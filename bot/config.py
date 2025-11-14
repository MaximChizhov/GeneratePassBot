import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Настройки паролей
    DEFAULT_LENGTH = 12
    MIN_LENGTH = 6
    MAX_LENGTH = 20


config = Config()