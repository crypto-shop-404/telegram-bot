import decimal
import uuid

import aiogram
from aiogram import dispatcher
from aiogram import filters

import config
import responses.main_menu
import responses.product_management
from loader import dp
from keyboards.inline import callback_factories
from services import products
from states import product_states


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='add', product_id=''))
async def add_product(query: aiogram.types, callback_data: dict[str, str]):
    category_id, subcategory_id = callback_data['category_id'], callback_data['subcategory_id']
    category_id = int(category_id) if category_id != '' else None
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    await product_states.AddProduct.waiting_name.set()
    await dp.current_state().update_data(
        {'product': products.Product(category_id, subcategory_id)}
    )
    await responses.product_management.AddProductNameResponse(query)


@dp.message_handler(state=product_states.AddProduct.waiting_name)
async def product_name(message: aiogram.types.Message, state: dispatcher.FSMContext):
    (await state.get_data())['product'].add_name(message.text)
    await product_states.AddProduct.next()
    await responses.product_management.AddProductDescriptionResponse(message)


@dp.message_handler(state=product_states.AddProduct.waiting_description)
async def product_description(message: aiogram.types.Message, state: dispatcher.FSMContext):
    (await state.get_data())['product'].add_description(message.text)
    await product_states.AddProduct.next()
    await responses.product_management.AddProductImageResponse(message)


@dp.message_handler(state=product_states.AddProduct.waiting_picture, content_types=['document', 'photo', 'text'])
async def product_picture(message: aiogram.types.Message, state: dispatcher.FSMContext):
    file_path = None
    pending_dir = config.PENDING_PATH / str(message.from_user.id)
    if message.document is not None and message.document.mime_type == 'image':
        file_path = pending_dir / f'{uuid.uuid4()}.{message.document.mime_subtype}'
    elif len(message.photo) > 0:
        file_path = pending_dir / f'{uuid.uuid4()}.jpg'
    if file_path is not None:
        await message.photo[-1].download(destination_file=file_path)
        (await state.get_data())['product'].add_picture(file_path)
    await product_states.AddProduct.next()
    await responses.product_management.AddProductPriceResponse(message)


@dp.message_handler(state=product_states.AddProduct.waiting_price)
async def product_price(message: aiogram.types.Message, state: dispatcher.FSMContext):
    price = message.text
    if not price.replace('.', '').isdigit():
        await responses.product_management.IncorrectPriceResponse(message)
        raise dispatcher.handler.CancelHandler
    await state.update_data({'price': float(decimal.Decimal(message.text))})
    product = (await state.get_data())['product']
    await product_states.AddProduct.next()
    await responses.product_management.SuccessProductAddingResponse(message, product.name)
    await responses.product_management.AddProductUnitResponse(message)


@dp.message_handler(state=product_states.AddProduct.waiting_content)
async def add_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product = (await state.get_data())['product']
    pending_dir = config.PENDING_PATH / str(message.from_user.id)
    if message.document is not None:
        product_data_file = pending_dir / f'{uuid.uuid4()}.{message.document.mime_subtype}'
        await message.document.download(destination_file=product_data_file)
        product.add_unit(product_data_file, 'document')
    elif len(message.photo) > 0:
        product_data_file = pending_dir / f'{uuid.uuid4()}.jpg'
        await message.photo[-1].download(destination_file=product_data_file)
        product.add_unit(product_data_file, 'document')
    elif message.text is not None:
        product.add_unit(message.text, 'text')
    await responses.product_management.SuccessUnitAddingResponse(message)


@dp.message_handler(filters.Text('✅ Complete'), state=product_states.AddProduct.waiting_content)
async def complete_product_adding(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product = (await state.get_data())['product']
    await state.finish()
    product.create()
    await responses.main_menu.AdminMainMenuResponse(message)
