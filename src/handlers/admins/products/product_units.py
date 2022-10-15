import os
import uuid

import aiogram.types
from aiogram import dispatcher, filters

import config
import responses.product_management
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services import product_services
from services.db_api import queries
from states import product_states


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='add_units'), is_admin.IsUserAdmin())
async def add_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.AddProductUnitResponse(query)
    await product_states.AddProductUnit.waiting_content.set()
    await dp.current_state().update_data(callback_data | {'units': []})


@dp.message_handler(filters.Text('✅ Complete'), is_admin.IsUserAdmin(),
                    state=product_states.AddProductUnit.waiting_content)
async def complete_units_loading(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    product_id = data['product_id']
    units = data['units']
    await state.finish()
    with db_api.create_session() as session:
        for unit in units:
            unit.create_product_unit(session)
        queries.edit_product_quantity(session, product_id, len(units))
        product = queries.get_product(session, product_id)
        await responses.product_management.CompleteUnitLoadingResponse(message, product.name)
        await responses.product_management.ProductResponse(
            message, product, product.category_id, product.subcategory_id
        )


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.AddProductUnit.waiting_content,
                    content_types=['text', 'photo', 'document'])
async def add_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    units, product_id = data['units'], data['product_id']
    pending_dir = config.PENDING_DIR_PATH / str(message.from_user.id)
    if message.document is not None:
        filename = f'{uuid.uuid4()}.{message.document.mime_subtype}'
        await message.document.download(destination_file=pending_dir / filename)
        units.append(
            product_services.ProductUnitLifeCycle(
                product_id, product_unit_content=filename, product_unit_type='document',
                pending_dir_path=pending_dir)
        )
    elif len(message.photo) > 0:
        filename = f'{uuid.uuid4()}.jpg'
        await message.photo[-1].download(destination_file=pending_dir / filename)
        units.append(
            product_services.ProductUnitLifeCycle(
                product_id, product_unit_content=filename, product_unit_type='document',
                pending_dir_path=pending_dir)
        )
    elif message.text is not None:
        for unit in message.text.split('\n'):
            units.append(product_services.ProductUnitLifeCycle(
                product_id, product_unit_content=unit,
                product_unit_type='text'
            ))
    await state.update_data({'units': units})
    await responses.product_management.SuccessUnitAddingResponse(message)


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='units'), is_admin.IsUserAdmin())
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


@dp.callback_query_handler(
    callback_factories.ProductUnitCallbackFactory().filter(action='manage'), is_admin.IsUserAdmin())
async def product_unit_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    unit_id = int(callback_data['id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        unit = queries.get_product_unit(session, unit_id)
        await responses.product_management.ProductUnitResponse(
            query, int(callback_data['product_id']), unit,
            int(callback_data['category_id']), subcategory_id
        )


@dp.callback_query_handler(
    callback_factories.ProductUnitCallbackFactory().filter(action='edit'), is_admin.IsUserAdmin())
async def edit_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.product_management.EditProductUnitsResponse(query)
    await product_states.EditProductUnit.waiting_content.set()
    await dp.current_state().update_data(callback_data)


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.EditProductUnit.waiting_content,
                    content_types=['photo', 'document'])
async def edit_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    subcategory_id = data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    unit_id = int(data['id'])
    await state.finish()
    with db_api.create_session() as session:
        product_unit = queries.get_product_unit(session, unit_id)
        filename = product_unit.content if product_unit.type == 'document' else str(uuid.uuid4())
        if len(message.photo) > 0:
            filename = f'{filename}.jpg'
            await message.photo[-1].download(destination_file=config.PRODUCT_UNITS_PATH / filename)
        elif message.document is not None:
            filename = f'{filename}.{message.document.mime_type}'
            await message.document.download(destination_file=config.PRODUCT_UNITS_PATH / filename)
        if product_unit.type != 'document':
            queries.edit_product_unit(session, unit_id, 'document', filename)
        await responses.product_management.ProductUnitResponse(
            message, int(data['product_id']), product_unit, int(data['category_id']), subcategory_id
        )


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.EditProductUnit.waiting_content)
async def edit_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    data = await state.get_data()
    await state.finish()
    product_unit_id = int(data['id'])
    subcategory_id = data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        product_unit = queries.get_product_unit(session, product_unit_id)
        if product_unit.type == 'document':
            if (config.PRODUCT_UNITS_PATH / product_unit.content).exists():
                os.remove(config.PRODUCT_UNITS_PATH / product_unit.content)
        queries.edit_product_unit(session, product_unit_id, 'text', message.text)
        await responses.product_management.ProductUnitResponse(
            message, int(data['product_id']), product_unit, int(data['category_id']), subcategory_id
        )


@dp.callback_query_handler(
    callback_factories.ProductUnitCallbackFactory().filter(action='delete'), is_admin.IsUserAdmin())
async def delete_product_unit(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    product_unit_life_cycle = product_services.ProductUnitLifeCycle(product_unit_id=int(callback_data['id']))
    with db_api.create_session() as session:
        product_unit_life_cycle.delete_product_unit(session)
        queries.edit_product_quantity(session, product_id, -1)
        units = queries.get_not_sold_product_units(session, product_id)
        await responses.product_management.SuccessRemovalUnitResponse(query)
        await responses.product_management.ProductUnitsResponse(
            query, int(callback_data['category_id']), product_id, units, subcategory_id
        )
