import os

from sqlalchemy import orm

import config
from services import db_api
from services.db_api import queries
from utils import file_system


class Product:

    def __init__(self, category_id, subcategory_id: int = None, product_id: int = None):
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.product_id = product_id
        self.name: str | None = None
        self.description: str | None = None
        self.price: float | None = None
        self.__units: list[ProductUnit] = []
        self.__picture_path: str | None = None

    def add_name(self, name: str):
        self.name = name

    def add_description(self, description: str):
        self.description = description

    def add_price(self, price: float):
        self.price = price

    def add_picture(self, picture_file: str):
        self.__picture_path = picture_file

    def add_unit(self, content: str, product_type: str):
        self.__units.append(
            ProductUnit(content=content, product_type=product_type)
        )

    def load_from_db(self):
        with db_api.create_session() as session:
            product = queries.get_product(session, self.product_id)
            self.name = product.name
            self.description = product.description
            self.price = product.price
            self.category_id = product.category_id
            self.subcategory_id = product.subcategory_id
            self.__picture_path = config.PRODUCT_PICTURE_PATH / product.picture
            self.__units = [
                ProductUnit(self.product_id, unit.id, unit.content, unit.type)
                for unit in queries.get_not_sold_product_units(session, self.product_id)
            ]

    def create(self):
        with db_api.create_session() as session:
            product = queries.add_product(
                session, self.name, self.description, self.price, len(self.__units),
                self.__picture_path and os.path.split(self.__picture_path)[-1], self.category_id, self.subcategory_id
            )
            if self.__picture_path is not None:
                file_system.move_file(self.__picture_path, config.PRODUCT_PICTURE_PATH)
            for unit in self.__units:
                unit.add_product_id(product.id)
                unit.create(session)

    def delete(self):
        with db_api.create_session() as session:
            queries.delete_product(session, self.product_id)
            queries.delete_not_sold_product_units(session, self.product_id)
            file_system.delete_file(self.__picture_path)
            for unit in self.__units:
                unit.delete_document()
            self.name = self.description = self.price = None
            self.category_id = self.subcategory_id = self.__picture_path = None
            self.__units = []


class ProductUnit:
    def __init__(self, product_id: int = None, unit_id: int = None, content: str = None, product_type: str = None):
        self.__path = None
        self.__product_id = product_id
        self.__id = unit_id
        self.__type = product_type
        self.__content = content

    def add_content(self, content: str, product_type: str):
        self.__content = content
        self.__type = product_type

    def add_product_id(self, product_id: int):
        self.__product_id = product_id

    def load_from_db(self, session: orm.Session = None):
        product_unit = queries.get_product_unit(session, self.__id)
        self.add_content(product_unit.content, product_unit.type)

    def create(self, session: orm.Session):
        product_unit = queries.add_product_unit(session, self.__product_id, self.__content, self.__type)
        self.__id = product_unit.id
        if self.__type == 'document':
            file_system.move_file(config.PENDING_PATH / self.__content, config.PRODUCT_UNITS_PATH)

    def delete(self, session: orm.Session = None):
        queries.delete_product_unit(session, self.__id)
        self.delete_document()
        self.__id = self.__type = self.__content = None
        self.__path = self.__product_id = None

    def delete_document(self):
        if self.__type == 'document':
            file_system.delete_file(config.PRODUCT_UNITS_PATH / self.__content)
