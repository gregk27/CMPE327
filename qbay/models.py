from datetime import datetime
# from operator import and_ not used in program
from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment
from validate_email import validate_email
from uuid import uuid4
import hashlib
import json

db = SQLAlchemy(app)

'''
This file defines data models and related business logics
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
    productName = db.Column(db.String(80), nullable=False, unique=True)
    userId = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    ownerEmail = db.Column(db.String(120), nullable=False)
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
    content = db.Column(db.String(65535), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    product = relationship('Product', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
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


def login(email, password, ip):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        A session for the user on the current machine, None if login fails
    '''
    # Validate inputs before proceeding
    if len(email) == 0 \
       or not validate_email(email) \
       or not validatePswd(password):
        return None

    matches = User.query.filter_by(email=email).all()
    user = None
    # Check results for a password match
    for m in matches:
        # Extract salt from string
        salt = m.password.split(":")[0]
        # Hash input with salt and compare to target
        if(m.password == salt + ":"
           + hashlib.sha512((password + salt).encode('utf-8')).hexdigest()):
            user = m
            break
    if user is None:
        return None

    time = datetime.now()
    s = Session(user=user, userId=user.id, ipAddress=ip,
                sessionId=str(uuid4()),
                # Session expires after a year
                expiry=datetime(time.year+1, time.month, time.day))
    return s


def validatePswd(password):
    '''
    Validatation of password
      Parameters:
        password (string): user password
      Returns:
        True if input password matches all required critera, otherwise False
    '''
    specialChars = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                    '(', ')', '_', '-', '+', '=', '{', '[', '}', ']',
                    '|', '\\', ':', ';', '"', '\'', '<', ',', '>', '.',
                    '?', '/']

    if len(password) < 6:
        print("Password must be at least 6 characters")
        return False

    if not any(char.isupper() for char in password):
        print('Password must contain at least one uppercase letter')
        return False

    if not any(char.islower() for char in password):
        print('Password must contain at least one lowercase letter')
        return False

    if not any(char in specialChars for char in password):
        print('Password must contain at least one special character')
        return False

    return True


def validateUser(username):
    '''
    Validatation of username
      Parameters:
        username (string): user name
      Returns:
        True if input username matches all required critera, otherwise False
    '''
    if len(username) < 3:
        print("Username must be at least 3 character")
        return False

    if len(username) > 20:
        print("Username exceeded characters. Maximum allowed is 20.")
        return False

    # Username must be alphamerical, whitepsace in prefix or suffix not allowed
    if (not username.replace(" ", "").isalnum() or username[0] == " "
            or username[-1] == " "):
        return False

    return True


def validateEmail(email):
    '''
    Validatation of email
      Parameters:
        email (string): user email
      Returns:
        True if input email follows addr-spec defined in RFC 5322 and if email
        is unique, otherwise False
    '''
    if len(email) == 0:
        return False

    if not validate_email(email):
        return False

    # check email exists in database
    exists = User.query.filter_by(email=email).all()
    if len(exists) > 0:
        return False

    return True


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
    if validateEmail(email) and validateUser(name) and validatePswd(password):
        # create a new user
        salt = uuid4()
        # Generate string from salt and hashed password
        hashed = str(salt) + ":" + hashlib.sha512((password + str(salt))
                                                  .encode('utf-8')).hexdigest()
        user = User(id=str(uuid4()), username=name, email=email,
                    password=hashed, balance=100, shippingAddress="",
                    postalCode="")
        # add it to the current database session
        db.session.add(user)
        # actually save the user object
        db.session.commit()
        return True

    return False


def queryUser(email, attribute, value):
    '''
    Check if specified user attribute matches expected value
      Parameters:
        email (string):     user email
        attribute (string)  user dbColumn
        value (string)      user attribute value
      Return: True if query matches value
    '''
    user = User.query.filter_by(email=email).all()
    # stringify user object
    temp = str(user[0])
    # create JSON object
    access = json.loads(temp)
    if access[attribute] == value:
        return True

    return False
