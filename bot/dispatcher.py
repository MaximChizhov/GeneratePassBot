from bot.handlers.handler import Handler, HandlerStatus


class Dispatcher:
    def __init__(self):
        self.handlers = []

    def add_handler(self, *handlers: Handler) -> None:
        self.handlers.extend(handlers)

    def dispatch(self, update: dict) -> None:
        for handler in self.handlers:
            if handler.can_handle(update):
                result = handler.handle(update)
                if result == HandlerStatus.STOP:
                    break