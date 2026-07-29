from aiogram.fsm.state import State, StatesGroup


class SettingsStates(StatesGroup):
    waiting_prime_time = State()