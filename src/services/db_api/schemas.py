import sqlalchemy
from sqlalchemy import orm, sql

from services.db_api import base


class BaseModel(base.Base):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sql.func.now())
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, onupdate=sql.func.current_timestamp())

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id})"


class User(BaseModel):
    __tablename__ = 'user'
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger(), nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String(32))
    balance = sqlalchemy.Column(sqlalchemy.Float(), default=0)
    is_banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class Category(BaseModel):
    __tablename__ = 'category'
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    subcategory = orm.relationship('Subcategory', backref='category', cascade="all, delete")

    product = orm.relationship('Product', backref='category', cascade="all, delete")


class Subcategory(BaseModel):
    __tablename__ = 'subcategory'
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    category_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id', ondelete='CASCADE'), nullable=False
    )
    product = orm.relationship('Product', backref='subcategory', cascade="all, delete")


class Product(BaseModel):
    __tablename__ = 'product'
    category_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id', ondelete='CASCADE'), nullable=False
    )
    subcategory_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('subcategory.id', ondelete='CASCADE')
    )
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    picture = sqlalchemy.Column(sqlalchemy.String(255))
    price = sqlalchemy.Column(sqlalchemy.Float(), nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)

    product_unit = orm.relationship('ProductUnit', backref='product')


class ProductUnit(BaseModel):
    __tablename__ = 'product_unit'
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('product.id'), nullable=False
    )
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, default='text')
    sale_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sale.id'))


class Sale(BaseModel):
    __tablename__ = 'sale'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String(255))
    product_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Float(), nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    payment_type = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    product_unit = orm.relationship('ProductUnit', lazy=False, backref='sale', cascade='all, delete')


class SupportSubject(BaseModel):
    __tablename__ = 'support_subject'
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)


class SupportRequest(BaseModel):
    __tablename__ = 'support_request'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.telegram_id'), nullable=False)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('support_subject.id'))
    username = sqlalchemy.Column(sqlalchemy.String())
    is_open = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    issue = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.Text())

    subject = orm.relationship(
        'SupportSubject', lazy=False, backref='support_request', cascade='all, delete',
    )
    user = orm.relationship('User', backref='support_request', lazy=False)
