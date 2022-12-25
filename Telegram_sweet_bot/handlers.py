import random

from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from config import dp
import text
import game
import emoji


@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    star = emoji.emojize(":star:")
    await message.answer(text=f'{text.greeting}'
                         f'{star} {message.from_user.first_name} {star} \n\n'
                         f' {text.rules}\n'
                         f' {text.agree}')
   

@dp.message_handler(commands=['new_game'])
async def start_new_game(message: Message):
    game.new_game()
    if game.check_game():
        toss = random.choice([True, False])
        if toss:
            await player_turn(message)
        else:
            await bot_turn(message)


async def player_turn(message: Message):
    await message.answer(f'{message.from_user.first_name},'
                         f' твой ход! Сколько возьмешь конфет?')


@dp.message_handler()
async def take(message: Message):
    name = message.from_user.first_name
    alien = emoji.emojize(":alien:")
    if game.check_game():
        if message.text.isdigit():
            take = int(message.text)
            if (0 < take < 29) and take <= game.get_total():
                game.take_candies(take)
                if await check_win(message, take, 'player'):
                    return
                await message.answer(f'{name} взял {take} конфет и на столе осталоcь '
                                     f'{game.get_total()}. \nХодит бот ...')
                await bot_turn(message)
            else:
                await message.answer(f'{alien} Так нельзя!!! Можно брать от 1 до 28')
        else:
            pass


async def bot_turn(message):
    total = game.get_total()
    if total <= 28:
        take = total
    else:
        take = random.randint(1, 28)
    game.take_candies(take)
    await message.answer(f'Бот взял {take} конфет и их осталось {game.get_total()}')
    if await check_win(message, take, 'Бот'):
        return
    await player_turn(message)


async def check_win(message, take: int, player: str):
    if game.get_total() <= 0:
        if player == 'player':
            await message.answer(f'{message.from_user.first_name} взял {take} и '
                                 f' одержал победу над железякой')
        else:
            await message.answer(f'Ну ты и лошара, {message.from_user.first_name} ! '
                                 f'Бот взял {take} и ПОБЕДИЛ!!!!! \n'
                                 f'Хочешь мачт-реванш - кликай /new_game')
        game.new_game()
        return True
    else:
        return False
