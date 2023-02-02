import json
import smtplib

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.exceptions import BadRequest

from crud import CRUDAnswer, CRUDQuestions, CRUDUser
from keyboards.inline.users.registration import main_cb
from loader import bot
from states.users.userStates import UserStates
import random


class MainForms:

    @staticmethod
    async def main_menu_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Начать тест", callback_data=main_cb.new("StartTest", 0, 0, 0))
                ]
            ]
        )

    @staticmethod
    async def answer_ikb(count: int,
                         user_id: int) -> InlineKeyboardMarkup:
        answers_data = []
        for answer in await CRUDAnswer.get_all():
            if count == 61:
                if 'L3' in answer:
                    answers_data.append("L3 (Закрытие ресторана)")
                else:
                    answers_data.append(answer.id)
            else:
                answers_data.append(answer.id)

        result = {}

        random.shuffle(answers_data)
        for i in answers_data:
            a = await CRUDAnswer.get(answer_id=i)
            result[a.name_answer] = {"id": a.id}

        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=answer,
                                                         callback_data=main_cb.new("NextTest",
                                                                                   answer_items["id"],
                                                                                   user_id,
                                                                                   count))
                                ]
                                for answer, answer_items in result.items()
                            ]
        )

    @staticmethod
    async def check_answer(answer_id: int,
                           question_id: int,
                           user_id: int):

        question = await CRUDQuestions.get_question_and_answer(question_id=question_id,
                                                               answer_id=answer_id)
        user = await CRUDUser.get(user_id=user_id)
        if user:
            if question:
                get = user.correct_answer
                user.correct_answer = get + 1
                await CRUDUser.update(user=user)
            else:
                user.wrong_answers.append(str(question_id))
                user.wrong_answer_selected.append(str(answer_id))
                await CRUDUser.update(user=user)
        else:
            pass

    @staticmethod
    async def send_mail(user_id):
        user = await CRUDUser.get(user_id=user_id)
        wrong_answer = user.wrong_answers
        wrong_answer_selected = user.wrong_answer_selected

        a = {}
        text1 = ""
        for answer in wrong_answer:
            for answer_selected in wrong_answer_selected:
                question = await CRUDQuestions.get(question_id=int(answer))
                answer_sel = await CRUDAnswer.get(answer_id=int(answer_selected))
                a[answer] = {"answer_descr": question.description, "answer_selected": answer_sel.name_answer}
                wrong_answer_selected.pop(0)
                break

        for i, j in a.items():
            text1 += f"Вопрос № {i}\n" \
                     f"{j['answer_descr']}\n" \
                     f"Дал ответ - {j['answer_selected']}\n\n"

        text = f"{user.lname} {user.fname} {user.mname} - {user.restaurant}\n\n" \
               f"Прошел тест на {(user.correct_answer / 100) * 100} %\n\n" \
               f"{text1}"


        user = "pavle4kovlad@yandex.by"
        passwd = "345789652Qq"
        server = "smtp.yandex.ru"
        port = 587

        # тема письма
        subject = "Пользователь прошел тест"
        # кому
        to = "pavle4kovlad@yandex.by"
        to2 = "kristina.pastushenko@kfc-vostok.by"
        to3 = "marina.avchinikova@kfc-vostok.by"
        # кодировка письма
        charset = 'Content-Type: text/plain; charset=utf-8'
        mime = 'MIME-Version: 1.0'

        # формируем тело письма
        body = "\r\n".join((f"From: {user}", f"To: {to}",
                            f"Subject: {subject}", mime, charset, "", text))

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
            smtp.sendmail(user, to3, body.encode('utf-8'))
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            print('Письмо успешно отправлено')
            smtp.quit()

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("main"):
                data = main_cb.parse(callback_data=callback.data)

                if data.get("target") == "StartTest":
                    question = await CRUDQuestions.get(question_id=1)
                    photo = open(f'/opt/git/StandardsTestBot/img/{question.img_id}.png', 'rb')
                    #photo = open(f'img/{question.img_id}.png', 'rb')
                    await callback.message.delete()
                    await callback.message.answer_photo(photo=photo,
                                                        caption=question.description,
                                                        reply_markup=await MainForms.answer_ikb(count=1,
                                                                                                user_id=callback.from_user.id)
                                                        )

                elif data.get("target") == "NextTest":
                    question_id = int(data.get("count"))

                    next_question = question_id + 1
                    user_id = callback.from_user.id

                    all_questions = len(await CRUDQuestions.get_all())

                    if all_questions >= next_question:
                        answer_id = data.get("id")
                        await MainForms.check_answer(answer_id=answer_id, question_id=question_id, user_id=user_id)

                        question = await CRUDQuestions.get(question_id=next_question)
                        await callback.message.delete()
                        photo = open(f'/opt/git/StandardsTestBot/img/{question.img_id}.png', 'rb')
                        #photo = open(f'img/{question.img_id}.png', 'rb')
                        await callback.message.answer_photo(photo=photo,
                                                            caption=f"Вопрос № {question_id + 1}\n\n"
                                                                    f"{question.description}",
                                                            reply_markup=await MainForms.answer_ikb(count=next_question,
                                                                                                    user_id=user_id)
                                                            )
                    else:
                        user = await CRUDUser.get(user_id=user_id)
                        correct_answer = user.correct_answer
                        user.is_passet = True
                        await CRUDUser.update(user=user)
                        i = (correct_answer % 100)

                        await MainForms.send_mail(user_id=user_id)
                        await callback.message.delete()
                        await callback.message.answer(text=f"Поздравляю вы прошли тест на {i} %")

        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                pass
                # if await state.get_state() == "UserStates:FIO":
                #     fio: list = message.text.split()
                #     user_id: int = int(message.from_user.id)
                #     nickname = "None"
                #     if message.from_user.username:
                #         nickname = message.from_user.username
                #
                #     if len(fio) < 3:
                #         await message.answer(text="Введите полное ФИО!")
                #         await UserStates.FIO.set()
                #     else:
                #         await state.update_data(user_id=user_id)
                #         await state.update_data(lname=fio[0].title())
                #         await state.update_data(fname=fio[1].title())
                #         await state.update_data(mname=fio[2].title())
                #         await state.update_data(checked=False)
                #         await state.update_data(nickname=nickname)
                #
                #         data = await state.get_data()
                #
                #         try:
                #             if await CRUDUser.add(user=UserSchema(**data)):
                #                 await message.answer(text=f"{fio[0].title()} {fio[1].title()} {fio[2].title()}\n"
                #                                           "Вы успешно зарег. в системе\n\n"
                #                                           "Главное меню",
                #                                      reply_markup=await MainForms.main_menu_ikb(user_id=user_id))
                #                 await state.finish()
                #             else:
                #                 await message.answer(text=f"Возникла небольшая проблема Обратитесь к менеджеру")
                #         except Exception as e:
                #             await message.answer(text=f"Возникла небольшая проблема Обратитесь к менеджеру")

                # if await state.get_state() == "UserStates:Back":
                #     try:
                #         if message.content_type == "web_app_data":
                #             webAppMes = message.web_app_data.data
                #             json_string = json.loads(webAppMes)
                #
                #             text = f"Понедельник - <b>{json_string['Monday']}</b>\n" \
                #                    f"Вторник - <b>{json_string['Tuesday']}</b>\n" \
                #                    f"Среда - <b>{json_string['Wednesday']}</b>\n" \
                #                    f"Четверг - <b>{json_string['Thursday']}</b>\n" \
                #                    f"Пятница - <b>{json_string['Friday']}</b>\n" \
                #                    f"Суббота - <b>{json_string['Saturday']}</b>\n" \
                #                    f"Воскресенье - <b>{json_string['Sunday']}</b>\n" \
                #                    f"Пожелание - <b>{json_string['Description']}</b>"
                #             user = await CRUDUser.get(user_id=message.from_user.id)
                #
                #             await state.update_data(user_id=user.id)
                #             await state.update_data(Monday=json_string['Monday'])
                #             await state.update_data(Tuesday=json_string['Tuesday'])
                #             await state.update_data(Wednesday=json_string['Wednesday'])
                #             await state.update_data(Thursday=json_string['Thursday'])
                #             await state.update_data(Friday=json_string['Friday'])
                #             await state.update_data(Saturday=json_string['Saturday'])
                #             await state.update_data(Sunday=json_string['Sunday'])
                #             await state.update_data(description=json_string['Description'])
                #
                #             await bot.send_message(text=f"‼️Нажми еще раз 'Отправить'\n"
                #                                         f"что бы твои пожеления увидел менеджер‼️\n\n"
                #                                         f"Ваши пожелания:\n{text}",
                #                                    chat_id=message.chat.id,
                #                                    reply_markup=await MainForms.approved_ikb(),
                #                                    parse_mode="HTML")
                #     except Exception as e:
                #         await message.answer(text=f"Ошибка расписание не добавлено\n\n"
                #                                   f"Обратись к разработчику Владислав и покажи эту ошибку\n\n"
                #                                   f"{e}")
                #     if message.text == "Назад":
                #         await message.answer(text="Главное меню",
                #                              reply_markup=await MainForms.main_menu_ikb(
                #                                  user_id=message.from_user.id))
                #         await state.finish()