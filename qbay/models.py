from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

import datetime as dt

db = SQLAlchemy(app)

'''
This file defines data models and related business logics
'''


class User(db.Model):
    """User model."""
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    sessions = relationship('sessions', back_populates='user')
    products = relationship('product', back_populates='user')
    reviews = relationship('review', back_populates='user')
    buyTransactions = relationship('transaction', back_populates='user')
    sellTransactions = relationship('transaction', back_populates='user')
    __tablename__ = "user"

    def __repr__(self):
        return '<User %r>' % self.username


# Source:
#   https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html
# Used for including product image
class Product(db.Model):
    """Product model."""
    id = db.Column(db.String(36), primary_key=True)
    productName = db.Column(db.String(80), nullable=False, unique=True)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    ownerEmail = db.Column(db.String(120), ForeignKey('user.email'),
                           nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    lastModifiedDate = db.Column(db.DateTime, nullable=False)
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

    user = relationship('user', back_populates='products')
    reviews = relationship('product', back_populates='reviews')
    __tablename__ = "product"


class ProductPicture(db.Model, Image):
    """Product picture model."""

    productId = db.Column(db.String(36), ForeignKey('product.id'),
                          primary_key=True)
    product = relationship('Product')
    __tablename__ = 'product_picture'


class Sessions(db.Model):
    """Session model."""
    sessionId = db.Column(db.String(36), primary_key=True)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    expiry = db.Column(db.DateTime)
    ipAddress = db.Column(db.String(15))
    csrfToken = db.Column(db.String(32))
    user = db.Column(db.String(36), ForeignKey('product.id'))

    user = relationship('user', back_populates='sessions')
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

    customer = relationship('user', back_populates='buyTransactions')
    merchant = relationship('user', back_populates='sellTransactions')
    product = relationship('product', back_populates='transaction')
    __tablename__ = "transaction"


class Review(db.Model):
    """Product Review model."""
    id = db.Column(db.String(36), primary_key=True, unique=True)
    productId = db.Column(db.String(36), ForeignKey('product.id'),
                          nullable=False)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(65535), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    product = relationship('product', back_populates='reviews')
    user = relationship('user', back_populates='reviews')
    __tablename__ = "review"


# create all tables
db.create_all()


# def register(name, email, password):
#     """
#     Register a new user
#       Parameters:
#         name (string):     user name
#         email (string):    user email
#         password (string): user password
#       Returns:
#         True if registration succeeded, otherwise False
#     """
#     # Check if the email has been used:
#     existed = User.query.filter_by(email=email).all()
#     if len(existed) > 0:
#         return False

#     # Create a new user
#     user = User(username=name, email=email, password=password)
#     # Add it to the current database session
#     db.session.add(user)
#     # Save the user object
#     db.session.commit()

#     return True


# def login(email, password):
#     """
#     Check login information
#       Parameters:
#         email (string):    user email
#         password (string): user password
#       Returns:
#         The user object if login succeeded otherwise None
#     """
#     valids = User.query.filter_by(email=email, password=password).all()
#     if len(valids) != 1:
#         return None
#     return valids[0]

def createProduct(title, description, price, last_modified_date, owner_email):
    """
    Create a Product
      Parameters:
        title (string):                 product title
        description (string):           product description
        price (float):                  product price
        last_modified_date (DateTime):  product object last modified date
        owner_email:                    product owner's email
      Returns:
        True if product creation succeeded, otherwise False
    """
    # If the title without spaces is not alphanumeric-only,
    # or begins or ends in a space
    # or is longer than 80 chars, return False
    if (not title.replace(" ", "").isalnum() or
            title[0] == " " or
            title[-1] == " " or
            len(title) > 80):
        return False

    # If description is less than 20 or greater than 20
    # or length of description is less than or equal to length of title,
    # return False
    if ((len(description) < 20 or len(description) > 2000) or
            len(description) <= len(title)):
        return False

    # Check acceptable price range [10, 10000]
    if (price < 10.0 or price > 10000.0):
        return False

    # Check acceptable last_modified_date range
    if (last_modified_date < dt.datetime(2021, 1, 2) or
            last_modified_date > dt.datetime(2025, 1, 2)):
        return False

    # Check if owner of the corresponding product exists
    owner = Product.query.filter_by(ownerEmail=owner_email).all()
    if (len(owner) == 0):
        return False

    # Check if user has already used this title
    userProducts = Product.query.filter_by(ownerEmail=owner_email,
                                           productName=title)
    if (len(userProducts) == 1):
        return False

    # Create a new product
    product = Product(productName=title,
                      description=description,
                      price=price,
                      lastModifiedDate=last_modified_date,
                      ownerEmail=owner_email
                      )

    # Add it to the current database session
    db.session.add(product)

    # Save the product object
    db.session.commit()

    return True
