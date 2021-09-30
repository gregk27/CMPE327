from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment

db = SQLAlchemy(app)

# Declare a base
Base = declarative_base()

'''
This file defines data models and related business logics
'''


class User(db.Model):
    """User model."""
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    __tablename__ = "user"

    def __repr__(self):
        return '<User %r>' % self.username


# Source:
#   https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html
# Used for including product image
class Product(Base):
    """Product model."""
    id = db.Column(db.String, primary_key=True)
    productName = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    size = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    colour = db.Column(db.String)
    currentPrice = db.Column(db.Float, nullable=False)
    startingBid = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    shipCost = db.Column(db.Float, nullable=False)
    category = db.Column(db.String)
    bidder = db.Column(db.String)
    image = image_attachment('ProductPicture')
    __tablename__ = "product"


class ProductPicture(Base, Image):
    """Product picture model."""

    productId = db.Column(db.String, ForeignKey('product.id'),
                          primary_key=True)
    product = relationship('Product')
    __tablename__ = 'product_picture'


class Sessions(db.Model):
    """Session model."""
    userId = db.Column(db.String)
    sessionId = db.Column(db.String, primary_key=True)
    expiry = db.Column(db.String)
    ipAddress = db.Column(db.String)
    csrfToken = db.Column(db.String)
    __tablename__ = "session"


# Used to process transactions
class Transaction(db.Model):
    """Transaction model."""
    paymentId = db.Column(db.String, primary_key=True)
    customerId = db.Column(db.String, nullable=False)
    netAmount = db.Column(db.Float, nullable=False)
    merchant = db.Column(db.String, nullable=False)
    cardId = db.Column(db.BigInteger, nullable=False, unique=True)
    cvv = db.Column(db.Integer, nullable=False)
    expiryDate = db.Column(db.Date(), nullable=False)
    billAddress = db.Column(db.String, nullable=False)
    __tablename__ = "transaction"


class Review(db.Model):
    """Product Review model."""
    id = db.Column(db.String, primary_key=True, unique=True)
    productId = db.Column(db.String, ForeignKey('product.id'), nullable=False)
    userId = db.Column(db.String, ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    __tablename__ = "review"

# create all tables
# db.create_all()


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]
