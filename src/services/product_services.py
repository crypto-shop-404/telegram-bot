import os
import pathlib
import shutil
import uuid

import typing_extensions
from sqlalchemy import orm

import config
from services import db_api
from services.db_api import queries


class ProductLifeCycle:

    def __init__(self, category_id: int = None, subcategory_id: int = None, product_id: int = None,
                 product_picture_filename: str = None, pending_dir_path: pathlib.Path | str = None):
        self.__category_id = category_id
        self.__subcategory_id = subcategory_id
        self.__product_id = product_id
        self.__product_name: str | None = None
        self.__product_description: str | None = None
        self.__product_price: float | None = None
        self.__product_units: list[ProductUnitLifeCycle] = []
        self.__pending_dir_path = pending_dir_path
        self.__product_picture_filename = product_picture_filename

    def create_product(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            product = queries.add_product(
                session, self.__product_name, self.__product_description, self.__product_price,
                len(self.__product_units), self.__product_picture_filename,
                self.__category_id, self.__subcategory_id
            )
            if self.__product_picture_filename is not None:
                shutil.move(
                    self.__pending_dir_path / self.__product_picture_filename, config.PRODUCT_PICTURE_PATH
                )
            for unit in self.__product_units:
                unit.add_product_id(product.id)
                unit.create_product_unit(session)
        return self

    def delete(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            queries.delete_product(session, self.__product_id)
            if (self.__product_picture_filename is not None and
                    (config.PRODUCT_PICTURE_PATH / self.__product_picture_filename).exists()):
                os.remove(config.PRODUCT_PICTURE_PATH / self.__product_picture_filename)
            self.delete_product_units(session)
        self.__product_name = self.__product_description = self.__product_price = None
        self.__category_id = self.__subcategory_id = self.__product_picture_filename = None
        return self

    def delete_product_units(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            queries.reset_product_quantity(session, self.__product_id)
            queries.delete_not_sold_product_units(session, self.__product_id)
            for unit in self.__product_units:
                unit.delete_product_unit(session)
            self.__product_units = []
        return self

    def load_from_db(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            product = queries.get_product(session, self.__product_id)
            self.__product_name = product.name
            self.__product_description = product.description
            self.__product_price = product.price
            self.__category_id = product.category_id
            self.__subcategory_id = product.subcategory_id
            if product.picture is not None:
                self.__product_picture_filename = product.picture
            self.__product_units = [
                ProductUnitLifeCycle(self.__product_id, unit.id, unit.content, unit.type)
                for unit in queries.get_not_sold_product_units(session, self.__product_id)
            ]
        return self

    def add_product_name(self, name: str) -> typing_extensions.Self:
        self.__product_name = name
        return self

    def add_product_description(self, description: str) -> typing_extensions.Self:
        self.__product_description = description
        return self

    def add_product_price(self, price: float) -> typing_extensions.Self:
        self.__product_price = price
        return self

    def add_pending_dir_path(self, pending_path: pathlib.Path | str) -> typing_extensions.Self:
        self.__pending_dir_path = pending_path
        return self

    def add_product_picture_filename(self, filename: str = None,
                                     extension: str = None) -> typing_extensions.Self:
        self.__product_picture_filename = f'{filename or uuid.uuid4()}' + (extension and f'.{extension}' or '')
        return self

    def add_product_unit(self, product_unit_content: str, product_unit_type: str,
                         pending_dir_path: pathlib.Path = None) -> typing_extensions.Self:
        self.__product_units.append(
            ProductUnitLifeCycle(
                product_unit_content=product_unit_content,
                product_unit_type=product_unit_type,
                pending_dir_path=pending_dir_path
            )
        )
        return self

    def get_product_name(self) -> str:
        return self.__product_name

    def get_product_description(self) -> str:
        return self.__product_description

    def get_product_price(self) -> float:
        return self.__product_price

    def get_pending_dir_path(self) -> pathlib.Path | str:
        return self.__pending_dir_path

    def get_product_picture_filename(self) -> str:
        return self.__product_picture_filename

    def get_product_units(self) -> list['ProductUnitLifeCycle']:
        return self.__product_units


class ProductUnitLifeCycle:
    def __init__(self, product_id: int = None, product_unit_id: int = None, product_unit_content: str = None,
                 product_unit_type: str = None, pending_dir_path: pathlib.Path | str = None):
        self.__path = None
        self.__product_id = product_id
        self.__product_unit_id = product_unit_id
        self.__product_unit_type = product_unit_type
        self.__product_unit_content = product_unit_content
        self.__pending_dir_path = pending_dir_path

    def create_product_unit(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            product_unit = queries.add_product_unit(
                session, self.__product_id,
                self.__product_unit_type, self.__product_unit_content)
        self.__product_unit_id = product_unit.id
        if self.__product_unit_type == 'document':
            shutil.move(self.__pending_dir_path / self.__product_unit_content, config.PRODUCT_UNITS_PATH)
        return self

    def delete_product_unit(self, session: orm.Session = None) -> typing_extensions.Self:
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            queries.delete_product_unit(session, self.__product_unit_id)
        if (self.__product_unit_type == 'document' and
                (config.PRODUCT_UNITS_PATH / self.__product_unit_content).exists()):
            os.remove(config.PRODUCT_UNITS_PATH / self.__product_unit_content)
        self.__product_unit_id = self.__product_unit_type = self.__product_unit_content = None
        self.__path = self.__product_id = None
        return self

    def load_from_db(self, session: orm.Session = None):
        with db_api.create_session() if session is None else session.begin_nested() as nested_session:
            session = session or nested_session
            product_unit = queries.get_product_unit(session, self.__product_unit_id)
            if product_unit.type == 'document':
                self.add_product_unit_content(product_unit.content, product_unit.type)

    def add_product_unit_content(self, content: str, product_unit_type: str) -> typing_extensions.Self:
        self.__product_unit_content = content
        self.__product_unit_type = product_unit_type
        return self

    def add_product_id(self, product_id: int) -> typing_extensions.Self:
        self.__product_id = product_id
        return self

    def add_pending_dir_path(self, pending_dir_path: pathlib.Path | str) -> typing_extensions.Self:
        self.__pending_dir_path = pending_dir_path
        return self

    def get_product_unit_content(self) -> str:
        return self.__product_unit_content

    def get_product_unit_type(self) -> str:
        return self.__product_unit_type

    def get_product_id(self) -> int:
        return self.__product_id

    def get_pending_dir_path(self) -> pathlib.Path | str:
        return self.__pending_dir_path
