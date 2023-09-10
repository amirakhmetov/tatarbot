import logging
import sqlite3
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import tatar_token
from aiogram.dispatcher import FSMContext


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=tatar_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class Info(StatesGroup):
    Name = State()
    Age = State()
    City = State()

class Keyb(StatesGroup):
    Check = State()

class Add(StatesGroup):
    Word = State()
    Conf = State()

class Learn(StatesGroup):
    Start = State()
    class Type(StatesGroup):
        class New(StatesGroup):
            Continue = State()
            Confirm = State()
        class Old(StatesGroup):
            Continue = State()
            Confirm = State()

class Del(StatesGroup):
    Confirm_del = State()

videos = InlineKeyboardMarkup()
video1 = InlineKeyboardButton(text='Первое видео', url='https://youtu.be/SFP3sWtkO7A?si=7FRRLDkAmbCa-Djz')
video2 = InlineKeyboardButton(text='Второе видео', url='https://youtu.be/G5ETrGr7iwE?si=JT0aVc7T4ZLFX1ZO')
video3 = InlineKeyboardButton(text='Третье видео', url='https://youtu.be/rh4QDVOYe8k?si=BxB2hEbLGo_OFWkM')
video4 = InlineKeyboardButton(text='Четвёртое видео', url='https://youtu.be/82i4JKZop8I?si=zG-NEK4YnnOpDGYV')
video5 = InlineKeyboardButton(text='Пятое видео', url='https://youtu.be/ucP_3RIDUSc?si=DOu3-ZvoRJAYxot3')
videos.add(video1).add(video2).add(video3).add(video4).add(video5)

websites = InlineKeyboardMarkup()
web1 = InlineKeyboardButton(text='Салават күпере', url='http://salavatkupere.com/')
web2 = InlineKeyboardButton(text='Шаян ТВ', url='https://shayantv.ru/')
web3 = InlineKeyboardButton(text='Анимационные сюжеты', url='https://mon.tatarstan.ru/anime_tat.htm')
web4 = InlineKeyboardButton(text='Мультфильмы на татарском языке', url='http://mon.tatarstan.ru/rus/info.php?id=539365')
web5 = InlineKeyboardButton(text="Библиотека 'Бала'", url='http://balarf.ru')
websites.add(web1).add(web2).add(web3).add(web4).add(web5)

material = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = KeyboardButton(text='Полезные видео')
btn2 = KeyboardButton(text='Полезные сайты')
material.add(btn1).add(btn2)

kb_confirm = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
yes_button = KeyboardButton('Да')
no_button = KeyboardButton('Нет')
kb_confirm.add(yes_button).add(no_button)

kb_words = ReplyKeyboardMarkup(resize_keyboard=True)
new_btn = KeyboardButton(text='Новые')
old_btn = KeyboardButton(text='Выученные')
home_btn = KeyboardButton('Главное меню')
kb_words.add(new_btn).add(old_btn).add(home_btn)

def menu_kb():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu_btn1 = KeyboardButton(text='Учить слова')
    menu_btn2 = KeyboardButton(text='Добавить слова')
    menu_btn3 = KeyboardButton(text='Полезные материалы')
    menu.add(menu_btn1)
    menu.add(menu_btn2)
    menu.add(menu_btn3)
    return menu

back_kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
back_btn = KeyboardButton('Главное меню')
back_kb.add(back_btn)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, name, age, city)")
    conn.commit()
    user = cursor.execute(f"SELECT * FROM users WHERE id = {id1}").fetchall()
    if user:
        await message.answer(
            f'Сәлам, {user[0][1]}! Вас приветствует Телеграм Бот "Мәг" 🤚\nГлавная цель бота "Мәг" увеличить количество носителей татарского языка 📚', reply_markup=menu_kb())
    else:
        await message.answer(
            f'Сәлам, {message.from_user.first_name}! Вас приветствует Телеграм Бот "Мәг" 🤚\nГлавная цель бота "Мәг" увеличить количество носителей татарского языка 📚')
        await message.answer('Для моей дальнейшей работы нужно пройти анкетирование')
        await message.answer('Как тебя зовут?')
        await Info.Name.set()

@dp.message_handler(text=['Создать профиль', '/createprofile'])
async def newprof(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM users WHERE id = {id1}").fetchall()
    if not user:
        await message.answer('Как тебя зовут?', reply_markup=ReplyKeyboardRemove())
        await Info.Name.set()
    else:
        await message.answer("У вас уже есть аккаунт, если хотите создать новый, удалите старый с помощью команды /deleteprofile и создайте новый, используя команду /createprofile", reply_markup=menu_kb())

@dp.message_handler(text=['/deleteprofile', 'Удалить профиль'])
async def delprof(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM users WHERE id = {id1}").fetchall()
    if user:
        await message.answer("Вы точно хотите удалить свой профиль?", reply_markup=kb_confirm)
        await Del.Confirm_del.set()
    else:
        await message.answer("У вас нет профиля, создать его можно с помощью команды /createprofile", reply_markup=menu_kb())


@dp.message_handler(lambda message:message.text == "Да", state=Del.Confirm_del)
async def delyes(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {id1}")
    conn.commit()
    await message.answer("Вы удалили свой профиль", reply_markup=menu_kb())
    await Del.next()

@dp.message_handler(lambda message:message.text == "Нет", state=Del.Confirm_del)
async def delyes(message:types.Message):
    await message.answer("Вы отменили удаление вашего профиля", reply_markup=menu_kb())
    await Del.next()

@dp.message_handler(lambda message: message.text, state=Info.Name)
async def name(message:types.Message):
    id1 = message.from_user.id
    name = message.text
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    data = [id1, name, 0, 0]
    cursor.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?)", data)
    conn.commit()
    await message.answer("Теперь напиши свой возраст")
    await Info.Age.set()

@dp.message_handler(lambda message: message.text.isdigit(), state=Info.Age)
async def age(message:types.Message):
    id1 = message.from_user.id
    age = message.text
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET age = REPLACE(age, 0, '{age}')")
    conn.commit()
    await message.answer("Из какого ты города?")
    await Info.City.set()

@dp.message_handler(lambda message: message.text, state=Info.City)
async def city(message:types.Message):
    id1 = message.from_user.id
    city = message.text
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET city = REPLACE(city, 0, '{city}')")
    conn.commit()
    data1 = cursor.execute(f"SELECT * FROM users WHERE id = {id1}").fetchall()
    await message.answer("Афәрин, твой профиль успешно создан")
    await message.answer(f"Ваш профиль\n\n<b>Имя:</b> {data1[0][1]}\n<b>Возраст:</b> {data1[0][2]}\n<b>Город:</b> {data1[0][3]}")
    await message.answer('Всё верно?', reply_markup=kb_confirm)
    await Keyb.Check.set()


@dp.message_handler(lambda message:message.text=='Да', state=Keyb.Check)
async def yes(message:types.Message):
    await message.answer('Отлично, можно продолжать', reply_markup=menu_kb())
    await Keyb.next()

@dp.message_handler(lambda message:message.text=='Нет', state=Keyb.Check)
async def yes(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    user = cursor.execute(f"DELETE FROM users WHERE id = {id1}")
    conn.commit()
    await message.answer('Создайте профиль заново с помощью команды /createprofile', reply_markup=ReplyKeyboardRemove())
    await Keyb.next()

@dp.message_handler(text=['Мой профиль', '/profile'])
async def profile(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('tatarlar.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM users WHERE id = {id1}").fetchall()
    if not user:
        await message.answer('У вас еще нет профиля, чтобы создать его напишите "Создать профиль" или используйте команду /createprofile')
    else:
        await message.answer(
            f"Ваш профиль\n\n<b>Имя:</b> {user[0][1]}\n<b>Возраст:</b> {user[0][2]}\n<b>Город:</b> {user[0][3]}", reply_markup=menu_kb())

@dp.message_handler(text=['Добавить слова', '/add'])
async def add(message:types.Message):
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS words(id INTEGER, word, definition)")
    conn.commit()
    await message.answer("Напишите слово и его значение/перевод через дефис", reply_markup=ReplyKeyboardRemove())
    await Add.Word.set()

@dp.message_handler(lambda message:message.text, state=Add.Word)
async def word(message:types.Message):
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    mess_t = message.text.split('-')
    word = mess_t[0].strip().title()
    defin = mess_t[1].strip().title()
    data = [id1, word, defin, 0]
    cursor.execute("INSERT OR IGNORE INTO words VALUES(?, ?, ?, ?)", data)
    conn.commit()
    await message.answer("Вы добавили новое слово в свою коллекцию, добавить ещё", reply_markup=kb_confirm)
    await Add.Conf.set()

@dp.message_handler(lambda message: message.text == "Да", state=Add.Conf)
async def yes(message:types.Message):
    await message.answer("Напишите слово и его значение/перевод через дефис", reply_markup=ReplyKeyboardRemove())
    await Add.Word.set()

@dp.message_handler(lambda message: message.text == "Нет", state=Add.Conf)
async def no(message:types.Message):
    await message.answer("Ок, вы вернулись в главное меню", reply_markup=menu_kb())
    await Add.next()

@dp.message_handler(text = ['Учить слова', '/learn'])
async def learn(message:types.Message):
    global known, unknown
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    known = cursor.execute(f"SELECT word FROM words WHERE id = {id1} AND knowledge = 1").fetchall()
    unknown = cursor.execute(f"SELECT word FROM words WHERE id = {id1} AND knowledge = 0").fetchall()
    await message.answer("Выберите, какие слова вы будете учить", reply_markup=kb_words)
    await Learn.Start.set()


@dp.message_handler(text = ['Новые', '/learn_new'], state=Learn.Start)
async def start_words(message:types.Message, state=Learn.Start):
    global unknown
    # global un_words
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    use = unknown
    words = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchall()
    if use:
        use1 = unknown[0][0]
        defin = cursor.execute(f"SELECT definition FROM words WHERE id = {id1} AND word = '{use1}'").fetchone()[0]

        if words:
            ans = use1 + " - " + defin
            await message.answer(ans)
            await message.answer("Вы знаете это слово?", reply_markup=kb_confirm)
            await Learn.Type.New.Confirm.set()
            use.remove(use[0])
        else:
            await message.answer("У вас еще нет слов в коллекции, добавить их можно с помощью функции /add", reply_markup=ReplyKeyboardRemove())
            await FSMContext.finish(state)
    else:
        await message.answer('У вас нет новых слов, добавить их можно с помощью команды /add', reply_markup=menu_kb())
        await FSMContext.finish(state)


@dp.message_handler(text = ['Выученные', '/repeat'], state=Learn.Start)
async def start_words(message:types.Message, state=Learn.Start):
    global known
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    use = known
    words = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchall()
    if use:
        use1 = known[0][0]
        defin = cursor.execute(f"SELECT definition FROM words WHERE id = {id1} AND word = '{use1}' ").fetchone()[0]
        if words:
            ans = use1 + " - " + defin
            await message.answer(ans)
            await message.answer("Вы знаете это слово?", reply_markup=kb_confirm)
            await Learn.Type.Old.Confirm.set()
            known.remove(known[0])
        else:
            await message.answer("У вас еще нет слов в коллекции, добавить их можно с помощью функции /add", reply_markup=ReplyKeyboardRemove())
            await FSMContext.finish(state)
    else:
        await message.answer('У вас нет новых слов, добавить их можно с помощью команды /add', reply_markup=menu_kb())
        await FSMContext.finish(state)

@dp.message_handler(lambda message: message.text == 'Да', state=Learn.Type.New.Confirm)
async def yes(message:types.Message, state=Learn.Type.New.Confirm):
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    w_list = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchall()
    word = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchone()[1]
    cursor.execute(f"UPDATE words SET knowledge = 1 WHERE id = {id1} AND word = '{word}'")
    conn.commit()
    await message.answer("Слово выучено", reply_markup=ReplyKeyboardRemove())
    if len(w_list) == 1:
        await message.answer("У вас закончились невыученные слова", reply_markup=menu_kb())
        await FSMContext.finish(state)
    else:
        await Learn.Type.New.Continue.set()
        await message.answer('Напишите 1, если хотите продолжить учить слова, 0 если не хотите', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Да', state=Learn.Type.Old.Confirm)
async def yes(message:types.Message, state=Learn.Type.Old.Confirm):
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    w_list = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchall()
    word = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchone()[1]
    cursor.execute(f"UPDATE words SET knowledge = 1 WHERE id = {id1} AND word = '{word}'")
    conn.commit()
    await message.answer("Слово выучено", reply_markup=ReplyKeyboardRemove())
    if len(w_list) == 1:
        await message.answer("У вас закончились невыученные слова", reply_markup=menu_kb())
        await FSMContext.finish(state)
    else:
        await Learn.Type.Old.Continue.set()
        await message.answer('Напишите 1, если хотите продолжить учить слова, 0 если не хотите', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message:message.text == 'Нет', state=Learn.Type.New.Confirm)
async def no(message:types.Message, state=Learn.Type.New.Confirm):
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    w_list = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchall()
    word = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchone()[1]
    cursor.execute(f"UPDATE words SET knowledge = 0 WHERE id = {id1} AND word = '{word}'")
    conn.commit()
    await message.answer("Слово осталось в очереди обучения", reply_markup=ReplyKeyboardRemove())
    if len(w_list) == 1:
        await message.answer("У вас закончились невыученные слова", reply_markup=menu_kb())
        await FSMContext.finish(state)
    else:
        await Learn.Type.New.Continue.set()
        await message.answer('Напишите 1, если хотите продолжить учить слова, 0 если не хотите', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message:message.text == 'Нет', state=Learn.Type.Old.Confirm)
async def no(message:types.Message, state=Learn.Type.Old.Confirm):
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    w_list = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchall()
    word = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchone()[1]
    cursor.execute(f"UPDATE words SET knowledge = 0 WHERE id = {id1} AND word = '{word}'")
    conn.commit()
    await message.answer("Слово осталось в очереди обучения", reply_markup=ReplyKeyboardRemove())
    if len(w_list) == 1:
        await message.answer("У вас закончились невыученные слова", reply_markup=menu_kb())
        await FSMContext.finish(state)
    else:
        await Learn.Type.Old.Continue.set()
        await message.answer('Напишите 1, если хотите продолжить учить слова, 0 если не хотите', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message:message.text in [1, '1'], state=Learn.Type.New.Continue)
async def again(message:types.Message, state=Learn.Type.New.Continue):
    global unknown
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    use = unknown
    words = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 0").fetchall()
    if use:
        use1 = unknown[0][0]
        defin = cursor.execute(f"SELECT definition FROM words WHERE id = {id1} AND word = '{use1}'").fetchone()[0]
        if words:
            ans = use1 + " - " + defin
            await message.answer(ans)
            await message.answer("Вы знаете это слово?", reply_markup=kb_confirm)
            await Learn.Type.New.Confirm.set()
            unknown.remove(unknown[0])
        else:
            await message.answer("У вас еще нет слов в коллекции, добавить их можно с помощью функции /add", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('У вас нет новых слов, добавить их можно с помощью команды /add', reply_markup=menu_kb())
        await FSMContext.finish(state)

@dp.message_handler(lambda message:message.text in [1, '1'], state=Learn.Type.Old.Continue)
async def again(message:types.Message, state=Learn.Type.Old.Continue):
    global known
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    use = known
    words = cursor.execute(f"SELECT * FROM words WHERE id = {id1} AND knowledge = 1").fetchall()
    if use:
        use1 = known[0][0]
        defin = cursor.execute(f"SELECT definition FROM words WHERE id = {id1} AND word = '{use1}'").fetchone()[0]
        if words:
            ans = use1 + " - " + defin
            await message.answer(ans)
            await message.answer("Вы знаете это слово?", reply_markup=kb_confirm)
            await Learn.Type.Old.Confirm.set()
            known.remove(known[0])
        else:
            await message.answer("У вас еще нет слов в коллекции, добавить их можно с помощью функции /add", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('У вас нет новых слов, добавить их можно с помощью команды /add', reply_markup=menu_kb())
        await FSMContext.finish(state)

@dp.message_handler(text=['/menu', 'Главное меню'])
async def home(message:types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=menu_kb())

@dp.message_handler(lambda message:message.text in [0, '0'], state=Learn.Type.Old.Continue)
async def zero(message:types.Message, state=Learn.Type.Old.Continue):
    await message.answer("Ок, вы вернулись в главное меню", reply_markup=menu_kb())
    await FSMContext.finish(state)

@dp.message_handler(text=['/mycollection', 'Моя коллекция'])
async def mycol(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('words_list.db')
    cursor = conn.cursor()
    words = cursor.execute(f"SELECT word, definition FROM words WHERE id = {id1}").fetchall()
    ans = ''
    for i in words:
        ans += i[0] + ' - ' + i[1] + '\n'
    await message.answer(ans)

@dp.message_handler(text=['Полезные материалы', '/materials'])
async def materials(message:types.Message):
    await message.answer("Выберите нужную категорию", reply_markup=material)

@dp.message_handler(text=['Полезные видео', '/videos'])
async def video(message:types.Message):
    await message.answer("<b>Выучи татарский язык за 8 минут // Tatar language</b>\n\n"
                         "<b>Какие фразы татарского нужно выучить в первую очередь</b>\n\n"
                         "<b>Как произносить татарские звуки</b>\n\n"
                         "<b>Уроки татарского языка</b>\n\n"
                         "<b>Аудиокурс 'Татарский язык с нуля'</b>", reply_markup=videos)

@dp.message_handler(text=['Полезные сайты', '/websites'])
async def sites(message:types.Message):
    await message.answer("<b>Сайт детского журнала 'Салават күпере'</b>\n\n"
                         "<b>Шаян ТВ</b>\n\n"
                         "<b>Анимационные сюжеты к занятию по обучению детей татарскому языку</b>\n\n"
                         "<b>Мультфильмы на татарском языке</b>\n\n"
                         "<b>Интерактивная звуковая мультимедийная библиотека 'Бала'</b>", reply_markup=websites)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


