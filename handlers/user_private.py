from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypeFilter
from keybords.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

USER_K = get_keyboard(
    'Добавить привычку',
    'Удалить привычку',
    'Редактировать привычки',
    'Помощь с ботом',
    placeholder='Что вы выбирите?',
    sizes=(2,2))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет 👋😄\nЯ бот для трекинга твоих привычек.\nПожалуйста, ознакомься, что я умею, введи доступную команду или напиши /help для помощи с ботом',
                         reply_markup=USER_K)


@user_private_router.message((F.text.lower().contains('удал')) | (F.text.lower() == 'Удалить привычку'))
@user_private_router.message(Command('delete'))
async def delete_cmd(message: types.Message, counter):
    print(counter)
    await message.answer("Выберите привычки для удаления")

@user_private_router.message((F.text.lower().contains('ред')) | (F.text.lower() == 'Редактировать привычки'))
@user_private_router.message(Command('edit'))
async def edit_cmd(message: types.Message):
    await message.answer("Выберите привычку для редактрования")

@user_private_router.message((F.text.lower().contains('пом')) | (F.text.lower() == 'Помощь с ботом'))
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer("Помощь с ботом")

class AddHabit(StatesGroup):
    name = State()
    image = State()

    texts = {
        'AddHabit:name': 'Введите название заново:',
        'AddHabit:image': 'Этот стейт последний, поэтому...',
    }

@user_private_router.message(StateFilter(None),(F.text.lower().contains('добав')) | (F.text.lower() == 'Добавить привычку'))
@user_private_router.message(Command('addition'))
async def addition_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введите название привычки: ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddHabit.name)

@user_private_router.message(StateFilter('*'), Command('отмена'))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer('Действия отменены', reply_markup=USER_K)

@user_private_router.message(StateFilter('*'), Command("назад"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddHabit.name:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddHabit.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddHabit.texts[previous.state]}")
            return
        previous = step

@user_private_router.message(AddHabit.name, F.text)
async def add_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer('Загрузите изображение')
    await state.set_state(AddHabit.name)

@user_private_router.message(AddHabit.name)
async def add_name(message: types.Message, state: FSMContext) -> None:
    await message.answer('Вы ввели недопустимые данные! Введите название заново!')


@user_private_router.message(F.photo)
async def add_image(message: types.Message, state: FSMContext) -> None:
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('Привычка добавлена', reply_markup=USER_K)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
