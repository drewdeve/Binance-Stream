from aiogram.dispatcher.filters.state import State, StatesGroup

class MenuState(StatesGroup):
    coin_and_interval = State()

if __name__ == '__main__':
    print(MenuState.all())