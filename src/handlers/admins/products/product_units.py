import uuid

import aiogram.types
from aiogram import dispatcher, filters

import config
import responses.product_management
from loader import dp
from keyboards.inline import callback_factories
from services import db_api
from services import products
from services.db_api import queries
from states import product_states


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='add_units'))
async def add_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.AddProductUnitResponse(query)
    await product_states.AddProductUnit.waiting_content.set()
    await dp.current_state().update_data(callback_data | {'units': []})


@dp.message_handler(state=product_states.AddProduct.waiting_content)
async def add_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    units, product_id = data['units'], data['product_id']
    pending_dir = config.PENDING_PATH / str(message.from_user.id)
    if message.document is not None:
        filename = f'{uuid.uuid4()}.{message.document.mime_subtype}'
        await message.document.download(destination_file=pending_dir / filename)
        units.append(products.ProductUnit(product_id, content=filename, product_type='document'))
    elif len(message.photo) > 0:
        filename = f'{uuid.uuid4()}.jpg'
        await message.photo[-1].download(destination_file=pending_dir / filename)
        units.append(products.ProductUnit(product_id, content=filename, product_type='document'))
    elif message.text is not None:
        units.append(products.ProductUnit(product_id, content=message.text, product_type='text'))
    await responses.product_management.SuccessUnitAddingResponse(message)


@dp.message_handler(filters.Text('✅ Complete'), state=product_states.AddProductUnit.waiting_content)
async def complete_units_loading(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    product_id = data['product_id']
    units = data['units']
    await state.finish()
    for unit in units:
        unit.create()
    with db_api.create_session() as session:
        queries.edit_product_quantity(session, product_id, len(units))
        product = queries.get_product(session, product_id)
        await responses.product_management.CompleteUnitLoadingResponse(message, product.name)
        await responses.product_management.ProductResponse(
            message, product, product.category_id, product.subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='units'))
async def product_units(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        units = queries.get_not_sold_product_units(session, product_id)
        await responses.product_management.ProductUnitsResponse(
            query, int(callback_data['category_id']), product_id,
            units, subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductUnitCallbackFactory().filter(action='manage'))
async def product_unit_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    unit_id = int(callback_data['id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        unit = queries.get_product_unit(session, unit_id)
        await responses.product_management.ProductUnitResponse(
            query, int(callback_data['product_id']), unit_id,
            unit, int(callback_data['category_id']), subcategory_id
        )


@dp.callback_query_handler(callback_factories.ProductUnitCallbackFactory().filter(action='edit'))
async def edit_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.EditProductUnitsResponse(query)
    await product_states.EditProductUnit.waiting_content.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(state=product_states.EditProductUnit.waiting_content, content_types=['photo', 'document'])
async def edit_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    subcategory_id = data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    unit_id = int(data['id'])
    await state.finish()
    unit = products.ProductUnit(unit_id=unit_id)
    unit.delete_document()
    filename = str(uuid.uuid4())
    if len(message.photo) > 0:
        filename = f'{filename}.jpg'
        await message.photo[-1].download(config.PRODUCT_UNITS_PATH / filename)
    elif message.document is not None:
        filename = f'{filename}.{message.document.mime_type}'
        await message.document.download(config.PRODUCT_UNITS_PATH / filename)
    await responses.product_management.ProductUnitResponse(
        message, int(data['product_id']), unit_id,
        open(config.PRODUCT_UNITS_PATH / filename, 'wb'), int(data['category_id']), subcategory_id,
    )


@dp.message_handler(state=product_states.EditProductUnit.waiting_content)
async def edit_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    await state.finish()
    product_unit_id = int(data['id'])
    subcategory_id = data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        queries.edit_product_unit(session, product_unit_id, 'text', message.text)
        await responses.product_management.ProductUnitResponse(
            message, int(data['product_id']), product_unit_id,
            message.text, subcategory_id, int(data['category_id'])
        )


@dp.callback_query_handler(callback_factories.ProductUnitCallbackFactory().filter(action='delete'))
async def delete_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    unit = products.ProductUnit(unit_id=int(callback_data['id']))
    with db_api.create_session() as session:
        unit.delete(session)
        queries.edit_product_quantity(session, product_id, -1)
        units = queries.get_not_sold_product_units(session, product_id)
        await responses.product_management.SuccessRemovalUnitResponse(query)
        await responses.product_management.ProductUnitsResponse(
            query, int(callback_data['category_id']), product_id, units, subcategory_id
        )
