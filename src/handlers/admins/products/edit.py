import os
import uuid

import aiogram
from aiogram import dispatcher

import config
import responses.main_menu
import responses.product_management
from filters import is_user_in_db, is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import product_states


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='edit_title'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def edit_product_title(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.EditProductResponse(query)
    await product_states.EditProductTitle.waiting_title.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB(),
                    state=product_states.EditProductTitle.waiting_title)
async def edit_product_title(message: aiogram.types.Message, state: dispatcher.FSMContext):
    state_data = await state.get_data()
    await state.finish()
    product_id, subcategory_id = int(state_data['product_id']), state_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        queries.edit_product_name(session, product_id, message.text)
        product = queries.get_product(session, product_id)
        await responses.product_management.SuccessProductChangeResponse(message)
        await responses.product_management.ProductResponse(
            message, category_id=int(state_data['category_id']),
            product=product, subcategory_id=subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='edit_description'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def edit_product_description(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.EditProductResponse(query)
    await product_states.EditProductDescription.waiting_description.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB(),
                    state=product_states.EditProductDescription.waiting_description)
async def edit_product_description(message: aiogram.types.Message, state: dispatcher.FSMContext):
    state_data = await state.get_data()
    await state.finish()
    product_id, subcategory_id = int(state_data['product_id']), state_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        queries.edit_product_description(session, product_id, message.text)
        product = queries.get_product(session, product_id)
        await responses.product_management.SuccessProductChangeResponse(message)
        await responses.product_management.ProductResponse(
            message, category_id=int(state_data['category_id']),
            product=product, subcategory_id=subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='edit_picture'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def edit_product_picture(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        product = queries.get_product(session, int(callback_data['product_id']))
        if product.picture is not None:
            file_path = config.PRODUCT_PICTURE_PATH / product.picture
            await query.message.answer_photo(file_path)
    await responses.product_management.EditProductResponse(query)
    await product_states.EditProductPicture.waiting_picture.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB(),
                    state=product_states.EditProductPicture.waiting_picture,
                    content_types=['photo', 'document', 'text']
                    )
async def edit_product_picture(message: aiogram.types.Message, state: dispatcher.FSMContext):
    state_data = await state.get_data()
    await state.finish()
    product_id, subcategory_id = int(state_data['product_id']), state_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        product = queries.get_product(session, product_id)
        if message.document is not None and message.document.mime_type == 'image':
            picture = message.document
            picture_type = picture.mime_subtype
        elif len(message.photo) > 0:
            picture, picture_type = message.photo[-1], 'jpg'
        else:
            picture, picture_type = None, None
        if picture is not None and picture_type is not None:
            if product.picture is not None and (config.PRODUCT_PICTURE_PATH / product.picture).exists():
                os.remove(config.PRODUCT_PICTURE_PATH / product.picture)
            filename = f'{product.picture or uuid.uuid4()}.{picture_type}'
            file_path = config.PRODUCT_PICTURE_PATH / filename
            queries.edit_product_picture(session, product.id, filename)
            await picture.download(destination_file=file_path)

        await responses.product_management.SuccessProductChangeResponse(message)
        await responses.product_management.ProductResponse(
            message, category_id=int(state_data['category_id']),
            product=product, subcategory_id=subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='edit_price'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def edit_product_title(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.EditProductResponse(query)
    await product_states.EditProductPrice.waiting_price.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB(), state=product_states.EditProductPrice)
async def edit_product_price(message: aiogram.types.Message, state: dispatcher.FSMContext):
    if not message.text.replace('.', '').isdigit():
        await responses.product_management.IncorrectPriceResponse(message)
        raise dispatcher.handler.CancelHandler
    state_data = await state.get_data()
    await state.finish()
    product_id, subcategory_id = int(state_data['product_id']), state_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None

    with db_api.create_session() as session:
        queries.edit_product_price(session, product_id, float(message.text))
        product = queries.get_product(session, product_id)
        await responses.product_management.SuccessProductChangeResponse(message)
        await responses.product_management.ProductResponse(
            message, category_id=int(state_data['category_id']),
            product=product, subcategory_id=subcategory_id
        )
