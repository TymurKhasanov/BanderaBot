from aiogram.fsm.state import State, StatesGroup


class PrimeStates(StatesGroup):
    waiting_schedule = State()