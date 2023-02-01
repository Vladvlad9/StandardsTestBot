import json
import smtplib

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest

from crud.userCRUD import CRUDUser
from keyboards.inline.users.mainForm import MainForms
from keyboards.inline.users.registration import RegistrationForms, main_cb
from loader import dp, bot
from schemas import UserSchema
from states.users.userStates import UserStates


@dp.message_handler(content_types="web_app_data") #получаем отправленные данные
async def answer(webAppMes):
    user_id = webAppMes.chat.id

    webAppMes = webAppMes.web_app_data.data
    json_string = json.loads(webAppMes)

    text = f"Фамилия - <b>{json_string['Lname']}</b>\n" \
           f"Имя - <b>{json_string['Fname']}</b>\n" \
           f"Отчество - <b>{json_string['Mname']}</b>\n\n" \
           f"Ресторан - <b>{json_string['Restaurant']}</b>\n" \

    await bot.send_message(text=f"Вы Успешно зарегистрировались: \n\n{text}",
                           chat_id=user_id,
                           reply_markup=await MainForms.main_menu_ikb())

    await CRUDUser.add(user=UserSchema(user_id=user_id,
                                       fname=json_string['Fname'],
                                       lname=json_string['Lname'],
                                       mname=json_string['Mname'],
                                       restaurant=json_string['Restaurant'],
                                       is_passet=False,
                                       percent=0,
                                       correct_answer=0,
                                       wrong_answer_selected=[],
                                       wrong_answers=[],
                                       answered_question=[]
                                       )
                       )

@dp.message_handler(commands=["test"])
async def registration_start(message: types.Message):
    # данные почтового сервиса
    user = "pavle4kovlad@yandex.by"
    passwd = "345789652Qq"
    server = "smtp.yandex.ru"
    port = 587

    # тема письма
    subject = "Пользователь прошел тест"
    # кому
    to = "pavle4kovlad@yandex.by"
    to2 = "vlad9.ru@gmail.com"
    # кодировка письма
    charset = 'Content-Type: text/plain; charset=utf-8'
    mime = 'MIME-Version: 1.0'

    # формируем тело письма
    body = "\r\n".join((f"From: {user}", f"To: {to}",
                        f"Subject: {subject}", mime, charset, "", "asd"))

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(user, passwd)
        # пробуем послать письмо
        smtp.sendmail(user, to, body.encode('utf-8'))
        smtp.sendmail(user, to2, body.encode('utf-8'))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        print('Письмо успешно отправлено')
        smtp.quit()


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    user = await CRUDUser.get(user_id=message.from_user.id)
    if user:
        if user.is_passet:
            correct_answer = user.correct_answer % 100
            await message.answer(text=f"Вы прошли тест на { correct_answer}%")
        else:
            await message.answer(text="Гланое меню",
                                 reply_markup=await MainForms.main_menu_ikb())
    else:
        await message.answer('Что бы пройти тест необходимо пройти регистрацию',
                             reply_markup=await RegistrationForms.open_site_kb()
                             )



    # res = await db.get_id_users(message.from_user.id)
    #
    # if res is None:
    #     await message.answer('Что бы пройти тест необходимо пройти регистрацию', reply_markup=await registr_user())
    # else:
    #     if res[0] == 'Не прошел':
    #         await message.answer('Вы еще не прошли опрос', reply_markup=await main_kb())
    #     else:
    #         result = await db.get_percent_users(message.from_user.id)
    #         new_res = result[0]
    #         f_new = float(new_res)
    #         await message.answer('Вы уже проходили данный тест\n'
    #                              f'Вы прошли тест на {round(int(f_new), 1)} %')





@dp.callback_query_handler(main_cb.filter())
@dp.callback_query_handler(main_cb.filter(), state=UserStates.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)