from aiogram.utils import callback_data


class ProductCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('product', 'category_id', 'subcategory_id', 'product_id', 'action')


class ProductUnitCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__(
            'product_unit', 'category_id', 'subcategory_id',
            'product_id', 'id', 'action'
        )


class BuyProductCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('buy_product', 'product_id', 'available_quantity', 'quantity', 'payment_method')


class TopUpBalanceCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('top_up_balance', 'amount', 'payment_method')


class CategoriesCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('categories', 'action')


class CategoryCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('category', 'category_id', 'subcategory_id', 'action')


class MailingCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('mailing', 'markup')


class ShopInformationFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('shop_information', 'object', 'action')


class UserCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('users', 'filter', 'page', 'id', 'action', 'is_confirmed')


class EditUserBalanceCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('edit_balance', 'user_id', 'balance', 'reason', 'is_confirmed')


class TopUpUserBalanceCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('top_up_balance', 'user_id', 'balance_delta', 'payment_method', 'is_confirmed')


class SupportCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('support', 'is_open', 'user_id', 'request_id', 'action')


class CreateSupportCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('create_support', 'subject_id')


class PaymentSystemCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('payment_system', 'system', 'action')
