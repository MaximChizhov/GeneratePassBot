from .menu_handler import MenuHandler

def get_handlers():
    return [
        MenuHandler()  # Только один агрегирующий хэндлер
    ]