from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

db = SQLAlchemy(app)

'''
This file defines data models
'''


class User(db.Model):
    """User model."""
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(165), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    shippingAddress = db.Column(db.String(64))
    postalCode = db.Column(db.String(36))

    sessions = relationship('Session', back_populates='user')
    products = relationship('Product', back_populates='user')
    reviews = relationship('Review', back_populates='user')
    buyTransactions = relationship('Transaction', back_populates='customer',
                                   foreign_keys="Transaction.customerId")
    sellTransactions = relationship('Transaction', back_populates='merchant',
                                    foreign_keys="Transaction.merchantId")
    __tablename__ = "user"

    def __repr__(self):
        return ("{\"user\":\"%s\",\"email\":\"%s\", \"shippingAddress\":\"%s\""
                % (self.username, self.email, self.shippingAddress)
                + ", \"postalCode\":\"%s\", \"balance\":\"%d\"}"
                % (self.postalCode, self.balance))


# Source:
#   https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html
# Used for including product image
class Product(db.Model):
    """Product model."""
    id = db.Column(db.String(36), primary_key=True)
    productName = db.Column(db.String(80), nullable=False)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    ownerEmail = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    lastModifiedDate = db.Column(db.DateTime, nullable=False)
    sold = db.Column(db.Boolean, nullable=False, default=False)
    # brand = db.Column(db.String(128))
    # size = db.Column(db.Float)
    # width = db.Column(db.Float)
    # height = db.Column(db.Float)
    # colour = db.Column(db.String(64))
    # startingBid = db.Column(db.Float, nullable=False)
    # address = db.Column(db.String(128), nullable=False)
    # shipCost = db.Column(db.Float, nullable=False)
    # category = db.Column(db.String(64))
    # bidder = db.Column(db.String(64))
    image = image_attachment('ProductPicture')

    user = relationship('User', back_populates='products')
    reviews = relationship('Review', back_populates='product')
    transaction = relationship('Transaction', back_populates='product')
    __tablename__ = "product"


class ProductPicture(db.Model, Image):
    """Product picture model."""

    productId = db.Column(db.String(36), ForeignKey('product.id'),
                          primary_key=True)
    product = relationship('Product', back_populates="image")
    __tablename__ = 'product_picture'


class Session(db.Model):
    """Session model."""
    sessionId = db.Column(db.String(36), primary_key=True)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    expiry = db.Column(db.DateTime)
    ipAddress = db.Column(db.String(15))
    csrfToken = db.Column(db.String(32))
    user = db.Column(db.String(36), ForeignKey('product.id'))

    user = relationship('User', back_populates='sessions')
    __tablename__ = "session"


# Used to process transactions
class Transaction(db.Model):
    """Transaction model."""
    paymentId = db.Column(db.String(36), primary_key=True)
    customerId = db.Column(db.String(36), ForeignKey('user.id'),
                           nullable=False)
    merchantId = db.Column(db.String(36), ForeignKey('user.id'),
                           nullable=False)
    productId = db.Column(db.String(36), ForeignKey('product.id'),
                          nullable=False)
    netAmount = db.Column(db.Float, nullable=False)
    cardId = db.Column(db.BigInteger, nullable=False, unique=True)
    cvv = db.Column(db.Integer, nullable=False)
    expiryDate = db.Column(db.Date(), nullable=False)
    billAddress = db.Column(db.String(128), nullable=False)

    customer = relationship('User', back_populates='buyTransactions',
                            uselist=False, foreign_keys=[customerId])
    merchant = relationship('User', back_populates='sellTransactions',
                            uselist=False, foreign_keys=[merchantId])
    product = relationship('Product', back_populates='transaction')
    __tablename__ = "transaction"


class Review(db.Model):
    """Product Review model."""
    id = db.Column(db.String(36), primary_key=True, unique=True)
    productId = db.Column(db.String(36), ForeignKey('product.id'),
                          nullable=False)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(32767), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    product = relationship('Product', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
    __tablename__ = "review"


# create all tables
db.create_all()
