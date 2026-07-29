from aiogram.fsm.state import State, StatesGroup


class EpicsStates(StatesGroup):
    waiting_schedule = State()