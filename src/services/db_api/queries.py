import decimal

import sqlalchemy
from sqlalchemy import orm

from services.db_api import schemas


def add_user(session: orm.Session, telegram_id: int, username: str) -> None:
    user = schemas.User(telegram_id=telegram_id, username=username)
    session.merge(user)


def add_category(session: orm.Session, name: str) -> schemas.Category:
    category = schemas.Category(name=name)
    session.add(category)
    session.flush()
    session.refresh(category)
    return category


def add_subcategory(session: orm.Session, name: str, category_id: int) -> schemas.Subcategory:
    subcategory = schemas.Subcategory(name=name, category_id=category_id)
    session.add(subcategory)
    session.flush()
    session.refresh(subcategory)
    return subcategory


def add_categories(session: orm.Session, categories: list[str]) -> None:
    for category_name in categories:
        add_category(session, category_name)


def add_subcategories(session: orm.Session, subcategories: list[str], category_id: int) -> None:
    for category_name in subcategories:
        add_subcategory(session, category_name, category_id)


def add_product(session: orm.Session, name: str, description: str,
                price: float, quantity: int, picture: str, category_id: int,
                subcategory_id: int = None) -> schemas.Product:
    product = schemas.Product(
        category_id=category_id,
        subcategory_id=subcategory_id,
        name=name, description=description,
        picture=picture, price=price, quantity=quantity
    )
    session.add(product)
    session.flush()
    session.refresh(product)
    return product


def add_product_unit(session: orm.Session, product_id: int, content_type: str, content: str) -> schemas.ProductUnit:
    product_unit = schemas.ProductUnit(
        product_id=product_id,
        content=content,
        type=content_type
    )
    session.add(product_unit)
    session.flush()
    session.refresh(product_unit)
    return product_unit


def add_sale(session: orm.Session, user_id: int, username: str,
             product_id: int, amount: float,
             quantity: int, payment_type: str) -> schemas.Sale:
    sale = schemas.Sale(
        user_id=user_id, product_id=product_id, username=username,
        amount=amount, quantity=quantity, payment_type=payment_type
    )
    session.add(sale)
    session.flush()
    session.refresh(sale)
    return sale


def add_support_request(session: orm.Session, user_id: int, username: str,
                        subject_id: int, issue: str) -> schemas.SupportRequest:
    support_request = schemas.SupportRequest(
        user_id=user_id, username=username,
        subject_id=subject_id, issue=issue
    )
    session.add(support_request)
    session.flush()
    session.refresh(support_request)
    return support_request


def add_support_subject(session: orm.Session, subject_name: str) -> None:
    if not check_is_support_subject_exists(session, subject_name):
        session.merge(schemas.SupportSubject(name=subject_name))


def get_users(session: orm.Session, limit: int = None, offset: int = None,
              usernames: list[str] = (), ids: list[int] = ()) -> list[schemas.User]:
    statement = sqlalchemy.select(schemas.User)
    if len(usernames) > 0:
        statement = statement.filter(schemas.User.username.in_(usernames))
    if len(ids) > 0:
        statement = statement.filter(schemas.User.id.in_(ids))
    if limit is not None:
        statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
    return session.scalars(statement).all()


def get_buyers(session: orm.Session) -> list[tuple[int, str | None, int, float]]:
    statement = sqlalchemy.select(
        schemas.User.telegram_id, schemas.User.username,
        sqlalchemy.func.sum(schemas.Sale.quantity),
        sqlalchemy.func.sum(schemas.Sale.amount)
    ).join(schemas.Sale)
    statement = statement.group_by(schemas.User.id)
    return session.execute(statement).all()


def get_users_telegram_id(session: orm.Session) -> list[int]:
    return session.scalars(sqlalchemy.select(schemas.User.telegram_id)).all()


def get_user(session: orm.Session, user_id: int = None, telegram_id: int = None) -> schemas.User | None:
    statement = sqlalchemy.select(schemas.User)
    if user_id is not None:
        statement = statement.filter_by(id=user_id)
    elif telegram_id is not None:
        statement = statement.filter_by(telegram_id=telegram_id)
    else:
        return None
    return session.scalars(statement).first()


def get_category(session: orm.Session, category_id: int) -> schemas.Category | None:
    return session.get(schemas.Category, category_id)


def get_all_categories(session: orm.Session) -> list[schemas.Category]:
    return session.scalars(sqlalchemy.select(schemas.Category)).all()


def get_subcategory(session: orm.Session, subcategory_id: int) -> schemas.Subcategory | None:
    return session.get(schemas.Subcategory, subcategory_id)


def get_subcategories(session: orm.Session, category_id: int) -> list[schemas.Subcategory]:
    statement = sqlalchemy.select(schemas.Subcategory).filter_by(category_id=category_id)
    return session.scalars(statement).all()


def get_category_items(session: orm.Session, category_id: int,
                       limit: int = None, offset: int = None) -> list[tuple[int, str, str]]:
    statement = sqlalchemy.select(
        schemas.Subcategory.id,
        sqlalchemy.literal_column("subcategory.name"), sqlalchemy.literal('subcategory')).filter_by(
        category_id=category_id
    )
    statement = statement.union(sqlalchemy.select(
        schemas.Product.id,
        sqlalchemy.literal_column('product.name') + ' | $' +
        sqlalchemy.literal_column('product.price') + ' | ' +
        sqlalchemy.literal_column('product.quantity') + ' pc(s)',
        sqlalchemy.literal('product')).filter_by(
        category_id=category_id, subcategory_id=None
    ))
    if limit is not None:
        statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
    return session.execute(statement).all()


def get_category_products(session: orm.Session, category_id: int = None,
                          subcategory_id: int = None,
                          limit: int = None, offset: int = None) -> list[schemas.Product]:
    if subcategory_id:
        statement = sqlalchemy.select(schemas.Product).filter_by(subcategory_id=subcategory_id)
    else:
        statement = sqlalchemy.select(schemas.Product).filter_by(
            category_id=category_id, subcategory_id=None
        )
    if limit is not None:
        statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
    categories = session.scalars(statement).all()
    return categories


def get_product(session: orm.Session, product_id: int) -> schemas.Product | None:
    return session.get(schemas.Product, product_id)


def get_product_unit(session: orm.Session, product_unit_id: int) -> schemas.ProductUnit | None:
    return session.get(schemas.ProductUnit, product_unit_id)


def get_all_product_unit(session: orm.Session, product_id: int) -> list[schemas.ProductUnit]:
    statement = sqlalchemy.select(schemas.ProductUnit).filter_by(product_id=product_id)
    return session.scalars(statement).all()


def get_not_sold_product_units(session: orm.Session, product_id: int,
                               quantity: int = None) -> list[schemas.ProductUnit]:
    statement = sqlalchemy.select(schemas.ProductUnit).filter_by(product_id=product_id, sale_id=None)
    if quantity is not None:
        statement = statement.limit(quantity)
    return session.scalars(statement).all()


def get_purchases(session: orm.Session, user_id: int = None, limit: int = None,
                  offset: int = None) -> list[tuple[str, int, float]]:
    statement = sqlalchemy.select(
        schemas.Product.name,
        sqlalchemy.func.sum(schemas.Sale.quantity),
        sqlalchemy.func.sum(schemas.Sale.amount)
    ).join(schemas.Sale).group_by(schemas.Sale.product_id)
    if user_id is not None:
        statement = statement.filter(schemas.Sale.user_id == user_id)
    if limit is not None:
        statement = statement.limit(limit)
    if offset is not None:
        statement = statement.offset(offset)
    return session.execute(statement.order_by(schemas.Sale.created_at.desc())).all()


def get_sales_by_user_id(session: orm.Session, user_id: int) -> list[schemas.Sale]:
    statement = sqlalchemy.select(schemas.Sale).filter_by(user_id=user_id)
    return session.scalars(statement).all()


def get_support_request(session: orm.Session, support_request_id: int) -> schemas.SupportRequest:
    return session.get(schemas.SupportRequest, support_request_id)


def get_user_support_requests(session: orm.Session, user_id: int) -> list[schemas.SupportRequest]:
    statement = sqlalchemy.select(schemas.SupportRequest).filter_by(user_id=user_id)
    return session.scalars(statement).all()


def get_all_support_subjects(session: orm.Session) -> list[schemas.SupportSubject]:
    return session.scalars(sqlalchemy.select(schemas.SupportSubject)).all()


def get_support_subject(session: orm.Session,
                        subject_id: int = None, name: str = None) -> schemas.SupportSubject | None:
    if subject_id is not None:
        return session.get(schemas.SupportRequest, subject_id)
    elif name is not None:
        return session.scalar(sqlalchemy.select(schemas.SupportSubject).filter_by(name=name))


def get_open_support_requests(session: orm.Session) -> list[schemas.SupportRequest]:
    statement = sqlalchemy.select(schemas.SupportRequest).filter_by(is_open=True)
    return session.scalars(statement).all()


def get_closed_support_requests(session: orm.Session) -> list[schemas.SupportRequest]:
    statement = sqlalchemy.select(schemas.SupportRequest).filter_by(is_open=False)
    return session.scalars(statement).all()


def get_faq(session: orm.Session) -> schemas.ShopInformation:
    statement = sqlalchemy.select(schemas.ShopInformation).filter_by(key='faq')
    return session.scalars(statement).first()


def get_rules(session: orm.Session) -> schemas.ShopInformation:
    statement = sqlalchemy.select(schemas.ShopInformation).filter_by(key='rules')
    return session.scalars(statement).first()


def get_greetings(session: orm.Session) -> schemas.ShopInformation:
    statement = sqlalchemy.select(schemas.ShopInformation).filter_by(key='greetings')
    return session.scalars(statement).first()


def get_comeback_message(session: orm.Session) -> schemas.ShopInformation:
    statement = sqlalchemy.select(schemas.ShopInformation).filter_by(key='comeback_message')
    return session.scalars(statement).first()


def ban_user(session: orm.Session, user_id: int) -> schemas.User | None:
    user = get_user(session, user_id)
    if user is not None:
        user.is_banned = True
        return user


def unban_user(session: orm.Session, user_id: int) -> schemas.User | None:
    user = get_user(session, user_id)
    if user is not None:
        user.is_banned = False
        return user


def top_up_balance(session: orm.Session, user_id: int, balance_delta: float | decimal.Decimal) -> None:
    user = get_user(session, user_id)
    if isinstance(balance_delta, float):
        balance_delta = decimal.Decimal(str(balance_delta))
    if user is not None:
        balance = decimal.Decimal(str(user.balance)) + balance_delta
        user.balance = float(balance)


def update_balance(session: orm.Session, user_id: int, new_balance: float) -> None:
    user = get_user(session, user_id)
    if user is not None:
        user.balance = new_balance


def edit_product_unit(session: orm.Session, product_unit_id: int, product_unit_type: str, content: str) -> None:
    product_unit = get_product_unit(session, product_unit_id)
    product_unit.content = content
    product_unit.type = product_unit_type


def add_sold_product_unit(session: orm.Session, sale_id: int, product_unit_id) -> None:
    product_unit = get_product_unit(session, product_unit_id)
    product_unit.sale_id = sale_id


def close_support_request(session: orm.Session, request_id: int, answer: str = None) -> schemas.SupportRequest:
    support_request = session.get(schemas.SupportRequest, request_id)
    support_request.is_open = False
    if answer is not None:
        support_request.answer = answer
    return support_request


def edit_product_name(session: orm.Session, product_id: int, name: str) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.name = name
    return product


def edit_product_description(session: orm.Session, product_id: int,
                             description: str) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.description = description
    return product


def edit_product_picture(session: orm.Session, product_id: int, picture: str) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.picture = picture
    return product


def edit_product_price(session: orm.Session, product_id: int, price: float) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.price = price
    return product


def edit_product_quantity(session: orm.Session, product_id: int, quantity_delta: int) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.quantity += quantity_delta
    return product


def reset_product_quantity(session: orm.Session, product_id: int) -> schemas.Product | None:
    product = get_product(session, product_id)
    if product is not None:
        product.quantity = 0
    return product


def edit_faq(session: orm.Session, faq_value: str):
    faq = get_faq(session)
    if faq is None:
        faq = schemas.ShopInformation(key='faq', value=faq_value)
        session.add(faq)
    else:
        faq.value = faq_value


def edit_rules(session: orm.Session, rules_value: str):
    rules = get_rules(session)
    if rules is None:
        rules = schemas.ShopInformation(key='rules', value=rules_value)
        session.add(rules)
    else:
        rules.value = rules_value


def edit_greetings(session: orm.Session, greetings_value: str):
    greetings = get_greetings(session)
    if greetings is None:
        greetings = schemas.ShopInformation(key='greetings', value=greetings_value)
        session.add(greetings)
    else:
        greetings.value = greetings_value


def edit_comeback_message(session: orm.Session, comeback_message_value: str):
    comeback_message = get_greetings(session)
    if comeback_message is None:
        comeback_message = schemas.ShopInformation(key='comeback_message', value=comeback_message_value)
        session.add(comeback_message)
    else:
        comeback_message.value = comeback_message_value


def delete_user(session: orm.Session, user_id: int) -> None:
    session.execute(sqlalchemy.delete(schemas.User).filter_by(id=user_id))


def delete_category(session: orm.Session, category_id: int) -> None:
    session.execute(sqlalchemy.delete(schemas.Category).filter_by(id=category_id))


def delete_subcategory(session: orm.Session, subcategory_id: int) -> None:
    session.execute(sqlalchemy.delete(schemas.Subcategory).filter_by(id=subcategory_id))


def delete_product(session: orm.Session, product_id: int) -> None:
    session.execute(sqlalchemy.delete(schemas.Product).filter_by(id=product_id))


def delete_product_unit(session: orm.Session, product_unit_id: int) -> None:
    statement = sqlalchemy.delete(schemas.ProductUnit).filter_by(id=product_unit_id)
    session.execute(statement)


def delete_not_sold_product_units(session: orm.Session, product_id: int) -> None:
    statement = sqlalchemy.delete(schemas.ProductUnit).filter_by(product_id=product_id, sale_id=None)
    session.execute(statement)


def delete_all_product_units(session: orm.Session, product_id: int) -> None:
    statement = sqlalchemy.delete(schemas.ProductUnit).filter_by(product_id=product_id)
    session.execute(statement)


def delete_support_request(session: orm.Session, support_request_id: int) -> None:
    session.execute(sqlalchemy.delete(schemas.SupportRequest).filter_by(id=support_request_id))


def count_users(session: orm.Session) -> int:
    return session.scalar(sqlalchemy.select(sqlalchemy.func.count(schemas.User.id)))


def count_user_orders(session: orm.Session, user_id: int) -> int:
    statement = sqlalchemy.select(sqlalchemy.func.count(schemas.Sale.id)).filter_by(
        user_id=user_id
    )
    return session.scalar(statement)


def count_purchases(session: orm.Session) -> int:
    statement = sqlalchemy.select(sqlalchemy.func.sum(schemas.Sale.quantity))
    return session.scalar(statement) or 0


def count_user_purchases(session: orm.Session, user_id: int) -> int:
    statement = sqlalchemy.select(sqlalchemy.func.sum(schemas.Sale.quantity))
    statement = statement.filter(schemas.Sale.user_id == user_id)
    return session.scalar(statement) or 0


def count_open_support_requests(session: orm.Session) -> int:
    statement = sqlalchemy.select(sqlalchemy.func.count(schemas.SupportRequest.id)).filter_by(is_open=True)
    return session.scalar(statement)


def get_total_orders_amount(session: orm.Session) -> float:
    return session.scalar(sqlalchemy.select(sqlalchemy.func.sum(schemas.Sale.amount))) or 0


def get_user_orders_amount(session: orm.Session, user_id: int):
    statement = sqlalchemy.select(sqlalchemy.func.sum(schemas.Sale.amount))
    return session.scalar(statement.filter(schemas.Sale.user_id == user_id)) or 0


def get_total_balance(session: orm.Session) -> float:
    return session.scalar(sqlalchemy.select(sqlalchemy.func.sum(schemas.User.balance)))


def check_is_user_exists(session: orm.Session, telegram_id: int) -> bool:
    statement = sqlalchemy.exists(sqlalchemy.select(schemas.User).filter_by(telegram_id=telegram_id))
    return session.scalar(statement.select())


def check_is_user_banned(session: orm.Session, telegram_id: int) -> bool:
    statement = sqlalchemy.exists(sqlalchemy.select(schemas.User).filter_by(telegram_id=telegram_id, is_banned=True))
    return session.scalar(statement.select())


def check_is_support_subject_exists(session: orm.Session, subject_name: str) -> bool:
    statement = sqlalchemy.exists(sqlalchemy.select(schemas.SupportSubject).filter_by(name=subject_name))
    return session.scalar(statement.select())
