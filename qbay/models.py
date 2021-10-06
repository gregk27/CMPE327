# from operator import and_ not used in program
from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment
from validate_email import validate_email

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
    shippingAddress = db.Column(db.String(64))
    postalCode = db.Column(db.String(36))

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
#     '''
#     Register a new user
#       Parameters:
#         name (string):     user name
#         email (string):    user email
#         password (string): user password
#       Returns:
#         True if registration succeeded otherwise False
#     '''
#     # check if the email has been used:
#     existed = User.query.filter_by(email=email).all()
#     if len(existed) > 0:
#         return False

#     # create a new user
#     user = User(username=name, email=email, password=password)
#     # add it to the current database session
#     db.session.add(user)
#     # actually save the user object
#     db.session.commit()

#     return True


# def login(email, password):
#     '''
#     Check login information
#       Parameters:
#         email (string):    user email
#         password (string): user password
#       Returns:
#         The user object if login succeeded otherwise None
#     '''
#     valids = User.query.filter_by(email=email, password=password).all()
#     if len(valids) != 1:
#         return None
#     return valids[0]


def validatePswd(password):
    '''
    Validatation of password
      Parameters:
        password (string): user password
      Returns:
        True if input password matches all required critera, otherwise False
    '''
    valid = True
    specialChars = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                    '(', ')', '_', '-', '+', '=', '{', '[', '}', ']',
                    '|', '\\', ':', ';', '"', '\'', '<', ',', '>', '.',
                    '?', '/']

    if len(password) < 6:
        print("Password must be at least 6 characters")
        valid = False

    if not any(char.isupper() for char in password):
        print('Password must contain at least one uppercase letter')
        valid = False

    if not any(char.islower() for char in password):
        print('Password must contain at least one lowercase letter')
        valid = False

    if not any(char in specialChars for char in password):
        print('Password must contain at least one special character')
        valid = False

    if valid:
        return valid


def validateUser(username):
    '''
    Validatation of username
      Parameters:
        username (string): user name
      Returns:
        True if input username matches all required critera, otherwise False
    '''
    valid = True

    if len(username) < 3:
        print("Username must be at least 3 character")
        valid = False

    if len(username) > 20:
        print("Username exceeded characters. Maximum allowed is 20.")
        valid = False

    alnum = list("abcdefghijklmnopqrstuvwxyz" +
                 "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
    for x in username:
        if x not in alnum:
            valid = False

    if username[0] == " " or username[len(username)-1] == " ":
        valid = False

    for i in range(len(username)):
        if username[i] == " " and username[i+1] == " ":
            valid = False

    return valid


def validateEmail(email):
    '''
    Validatation of email
      Parameters:
        email (string): user email
      Returns:
        True if input email follows addr-spec defined in RFC 5322 and if email is unique, otherwise False
    '''
    valid = True

    if len(email) == 0:
        valid = False

    if validate_email(email):
        valid = False

    #check email exists in database
    exists = User.query.filter_by(email=email).all()
    if len(exists) > 0:
        valid = False

    return valid


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
    registered = False
    if validateEmail(email) and validateUser(name) and validatePswd(password):
        # create a new user
        user = User(username=name, email=email, password=password,
                    shippingAddress="", postalCode="", balance=100)
        # add it to the current database session
        db.session.add(user)
        # actually save the user object
        db.session.commit()
    registered = True
    return registered
