import aiogram
from aiogram import filters

import responses.shop_information
from filters import is_admin
from loader import dp
from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('ℹ️ FAQ'), ~is_admin.IsUserAdmin())
async def faq_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        faq = queries.get_faq(session)
        await responses.shop_information.FAQResponse(
            message, faq.value if faq is not None else 'FAQ', False
        )


@dp.message_handler(filters.Text('📗 Rules'), ~is_admin.IsUserAdmin())
async def rules_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        rules = queries.get_rules(session)
        await responses.shop_information.RulesResponse(
            message, rules.value if rules is not None else 'Rules', False
        )
