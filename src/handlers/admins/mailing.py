import aiogram
from aiogram import filters, dispatcher

import exceptions
import responses.mailing
import responses.main_menu
from loader import dp
from filters import is_admin, is_user_in_db
from services import db_api
from services.db_api import queries
from states import mailing_states


@dp.message_handler(filters.Text('📧 Newsletter'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def create_newsletter(message: aiogram.types.Message):
    await responses.mailing.MailingResponse(message)


@dp.message_handler(filters.Text('📮 Create Newsletter'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def create_newsletter(message: aiogram.types.Message):
    await responses.mailing.CreateNewsletterResponse(message)
    await mailing_states.MailingStates.waiting_newsletter.set()


@dp.message_handler(is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(),
                    state=mailing_states.MailingStates.waiting_newsletter, content_types='any')
async def send_newsletter(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        users_id = queries.get_users_telegram_id(session)
    await responses.mailing.MailingStartResponse(message)
    successfully_newsletters = unsuccessfully_newsletters = 0
    for user_id in users_id:
        try:
            try:
                await message.copy_to(user_id)
            except Exception:
                raise exceptions.SendMailError
        except exceptions.SendMailError:
            unsuccessfully_newsletters += 1
        else:
            successfully_newsletters += 1
    await responses.mailing.MailingFinishResponse(
        message, successfully_newsletters, unsuccessfully_newsletters
    )
    await responses.main_menu.AdminMainMenuResponse(message)
