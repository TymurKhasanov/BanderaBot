from aiogram.fsm.state import State, StatesGroup


class ExperienceStates(StatesGroup):
    waiting_level = State()
    waiting_percent = State()
