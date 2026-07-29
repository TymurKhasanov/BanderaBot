from aiogram.fsm.state import State, StatesGroup


class AnnouncementStates(StatesGroup):
    waiting_text = State()