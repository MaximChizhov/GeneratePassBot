from bot.handlers.handler import Handler, HandlerStatus


class Dispatcher:
    def __init__(self):
        self.handlers = []

    def add_handler(self, *handlers: Handler) -> None:
        self.handlers.extend(handlers)

    def dispatch(self, update: dict) -> None:
        state = "main"  # Пока не используем, но оставляем для будущего
        user_data = {}  # Пока не используем, но оставляем для будущего

        for handler in self.handlers:
            if handler.can_handle(update, state, user_data):
                result = handler.handle(update, state, user_data)
                if result == HandlerStatus.STOP:
                    break