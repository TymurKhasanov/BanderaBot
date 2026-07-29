from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    waiting_prime_time = State()
    waiting_epics = State()
    waiting_announcement = State()