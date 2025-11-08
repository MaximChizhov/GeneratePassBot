from bot.handlers.handler import Handler, HandlerStatus
from bot.handlers import start, password_generation, help


class MenuHandler(Handler):
    def __init__(self):
        self.handlers = []
        self.setup_handlers()

    def setup_handlers(self):
        # Команда /start
        self.handlers.append(start.StartHandler())
        # Текстовые сообщения
        self.handlers.append(start.BackHandler())
        self.handlers.append(password_generation.GeneratePasswordHandler())
        self.handlers.append(help.HelpHandler())
        # Callback queries
        self.handlers.append(password_generation.CallbackHandler())

    def can_handle(self, update: dict, state: str, user_data: dict) -> bool:
        for handler in self.handlers:
            if handler.can_handle(update, state, user_data):
                return True
        return False

    def handle(self, update: dict, state: str, user_data: dict) -> HandlerStatus:
        for handler in self.handlers:
            if handler.can_handle(update, state, user_data):
                return handler.handle(update, state, user_data)
        return HandlerStatus.CONTINUE