import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from common.bot_cmd_list import private

from middlewares.db import CounterMiddleware


ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

dp.update.outer_middleware(CounterMiddleware())

dp.include_routers(user_private_router, user_group_router)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())