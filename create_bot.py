from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
token = os.getenv('TOKEN')
bot = Bot(token='5318034841:AAE8LwugFT2Ne-cRpFH6QdJ0mD398M2WiYU')
dp = Dispatcher(bot, storage=storage)
#'5318034841:AAE8LwugFT2Ne-cRpFH6QdJ0mD398M2WiYU'
