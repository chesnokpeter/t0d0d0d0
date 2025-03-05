from aiogram.fsm.state import State, StatesGroup



class TaskState(StatesGroup):
    add_inbox = State()