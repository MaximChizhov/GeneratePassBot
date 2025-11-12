from bot.handlers.handler import Handler, HandlerStatus
from bot.handlers import start_handler, password_generation, help_handler, length_handler, toogle_handler, generate_handler


class MenuHandler(Handler):
    def __init__(self):
        self.handlers = []
        self.setup_handlers()

    def setup_handlers(self):
        # Команда /start
        self.handlers.append(start_handler.StartHandler())
        # Текстовые сообщения
        self.handlers.append(password_generation.GenerateHandler())
        self.handlers.append(help_handler.HelpHandler())
        # Callback queries
        self.handlers.append(generate_handler.GeneratePasswordHandler())
        self.handlers.append(length_handler.LengthHandler())
        self.handlers.append(toogle_handler.ToggleHandler())

    def can_handle(self, update: dict) -> bool:
        for handler in self.handlers:
            if handler.can_handle(update):
                return True
        return False

    def handle(self, update: dict) -> HandlerStatus:
        for handler in self.handlers:
            if handler.can_handle(update):
                return handler.handle(update)
        return HandlerStatus.CONTINUE