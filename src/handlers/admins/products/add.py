import decimal
import uuid

import aiogram
from aiogram import dispatcher
from aiogram import filters

import config
import responses.main_menu
import responses.product_management
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import product_services
from states import product_states


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='add', product_id=''), is_admin.IsUserAdmin()
)
async def add_product(query: aiogram.types, callback_data: dict[str, str]):
    category_id, subcategory_id = callback_data['category_id'], callback_data['subcategory_id']
    category_id = int(category_id) if category_id != '' else None
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    await product_states.AddProduct.waiting_name.set()
    await dp.current_state().update_data(
        {'product_life_cycle': product_services.ProductLifeCycle(category_id, subcategory_id)}
    )
    await responses.product_management.AddProductNameResponse(query)


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.AddProduct.waiting_name)
async def product_name(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product_life_cycle = (await state.get_data())['product_life_cycle']
    product_life_cycle.add_product_name(message.text)
    await state.update_data({'product_life_cycle': product_life_cycle})
    await product_states.AddProduct.next()
    await responses.product_management.AddProductDescriptionResponse(message)


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.AddProduct.waiting_description)
async def product_description(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product_life_cycle = (await state.get_data())['product_life_cycle']
    product_life_cycle.add_product_description(message.text)
    await state.update_data({'product_life_cycle': product_life_cycle})
    await product_states.AddProduct.next()
    await responses.product_management.AddProductImageResponse(message)


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.AddProduct.waiting_picture,
                    content_types=['document', 'photo', 'text'])
async def product_picture(message: aiogram.types.Message, state: dispatcher.FSMContext):
    filename = None
    if message.document is not None and message.document.mime_type == 'image':
        filename = f'{uuid.uuid4()}.{message.document.mime_subtype}'
    elif len(message.photo) > 0:
        filename = f'{uuid.uuid4()}.jpg'
    if filename is not None:
        pending_dir = config.PENDING_DIR_PATH / str(message.from_user.id)
        await message.photo[-1].download(destination_file=pending_dir / filename)
        product_life_cycle = (await state.get_data())['product_life_cycle']
        product_life_cycle.add_product_picture_filename(filename).add_pending_dir_path(pending_dir)
        await state.update_data({'product_life_cycle': product_life_cycle})
    await product_states.AddProduct.next()
    await responses.product_management.AddProductPriceResponse(message)


@dp.message_handler(is_admin.IsUserAdmin(), state=product_states.AddProduct.waiting_price)
async def product_price(message: aiogram.types.Message, state: dispatcher.FSMContext):
    price = message.text
    if not price.replace('.', '').isdigit():
        await responses.product_management.IncorrectPriceResponse(message)
        raise dispatcher.handler.CancelHandler
    product_life_cycle = (await state.get_data())['product_life_cycle']
    product_life_cycle.add_product_price(float(decimal.Decimal(message.text)))
    await state.update_data({'product_life_cycle': product_life_cycle})
    await product_states.AddProduct.next()
    await responses.product_management.SuccessProductAddingResponse(
        message, product_life_cycle.get_product_name()
    )
    await responses.product_management.AddProductUnitResponse(message)


@dp.message_handler(filters.Text('✅ Complete'), is_admin.IsUserAdmin(),
                    state=product_states.AddProduct.waiting_content)
async def complete_product_adding(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product = (await state.get_data())['product_life_cycle']
    await state.finish()
    product.create_product()
    await responses.main_menu.AdminMainMenuResponse(message)


@dp.message_handler(content_types=['text', 'photo', 'document'], state=product_states.AddProduct.waiting_content)
async def add_product_unit(message: aiogram.types.Message, state: dispatcher.FSMContext):
    product = (await state.get_data())['product_life_cycle']
    pending_dir = config.PENDING_DIR_PATH / str(message.from_user.id)
    if message.document is not None:
        product_data_file = pending_dir / f'{uuid.uuid4()}.{message.document.mime_subtype}'
        await message.document.download(destination_file=product_data_file)
        product.add_product_unit(product_data_file.name, 'document', pending_dir)
    elif len(message.photo) > 0:
        product_data_file = pending_dir / f'{uuid.uuid4()}.jpg'
        await message.photo[-1].download(destination_file=product_data_file)
        product.add_product_unit(product_data_file.name, 'document', pending_dir)
    elif message.text is not None:
        for product_unit in message.text.split('\n'):
            product.add_product_unit(product_unit, 'text')
    await state.update_data({'product_life_cycle': product})
    await responses.product_management.SuccessUnitAddingResponse(message)
