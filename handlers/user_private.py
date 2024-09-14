from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет 👋😄 Я бот для трекинга твоих привычек. Пожалуйста введи доступную команду или напиши /help для помощи с ботом")


@user_private_router.message((F.text.lower().contains('добав')) | (F.text.lower() == 'Добавить привычку'))
@user_private_router.message(Command('addition'))
async def addition_cmd(message: types.Message):
    await message.answer("Добавить привычку")

@user_private_router.message((F.text.lower().contains('удал')) | (F.text.lower() == 'Удалить привычку'))
@user_private_router.message(Command('delete'))
async def delete_cmd(message: types.Message):
    await message.answer("Удалить привычку")

@user_private_router.message((F.text.lower().contains('ред')) | (F.text.lower() == 'Редактировать привычки'))
@user_private_router.message(Command('edit'))
async def edit_cmd(message: types.Message):
    await message.answer("Редактировать привычки")

@user_private_router.message((F.text.lower().contains('пом')) | (F.text.lower() == 'Помощь с ботом'))
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer("Помощь с ботом")