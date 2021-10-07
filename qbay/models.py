from qbay import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment
from validate_email import validate_email
from uuid import uuid4
import datetime as dt
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
    productName = db.Column(db.String(80), nullable=False)
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
    print(1)
    print(title)
    if (not title.replace(" ", "").isalnum() or
            title[0] == " " or
            title[-1] == " " or
            len(title) > 80):
        return False

    # If description is less than 20 or greater than 20
    # or length of description is less than or equal to length of title,
    # return False
    print(2)
    if ((len(description) < 20 or len(description) > 2000) or
            len(description) <= len(title)):
        return False

    # Check acceptable price range [10, 10000]
    print(3)
    if (price < 10.0 or price > 10000.0):
        return False

    # Check acceptable last_modified_date range
    print(4)
    if (last_modified_date <= dt.datetime(2021, 1, 2) or
            last_modified_date >= dt.datetime(2025, 1, 2)):
        return False

    # Check if owner email is null
    print(5)
    if (owner_email == "" or owner_email is None):
        return False

    # Check if owner of the corresponding product exists
    print(6)
    owner = User.query.filter_by(email=owner_email).all()
    if (len(owner) == 0):
        return False

    # Check if user has already used this title
    userProducts = Product.query.filter_by(ownerEmail=owner_email,
                                           productName=title).all()
    print(7)
    if (len(userProducts) == 1):
        return False

    # Create a new product
    product = Product(id=str(uuid4()),
                      productName=title,
                      description=description,
                      price=price,
                      lastModifiedDate=last_modified_date,
                      userId=owner[0].id,
                      ownerEmail=owner_email
                      )

    # Add it to the current database session
    db.session.add(product)

    # Save the product object
    db.session.commit()

    return True


def updateProduct(productId, **kwargs):
    print(productId)
    product = Product.query.filter_by(id=productId).first()
    if product is None:
        return False

    # Update price if it's higher
    if 'price' in kwargs:
        if(kwargs['price'] > product.price):
            product.price = kwargs['price']
        kwargs.pop('price')

    # Update name if it's alphanumeric and under 80 chars
    if 'name' in kwargs:
        # TODO: Take name validation from creation function
        product.name = kwargs['name']
        kwargs.pop('name')

    # Update description if it's within size limits
    if 'description' in kwargs:
        desc = kwargs['description']
        if(len(desc) >= 20 and len(desc) <= 2000
           and len(desc) > len(product.productName)):
            product.description = desc
        kwargs.pop('description')

    # Check price is in range
    if 'price' in kwargs:
        price = kwargs['price']
        if(price >= 10 and price <= 10000):
            product.price = price
        kwargs.pop('price')

    # Assign remaining properties directly
    for key, val in kwargs.items():
        # Some properties cannot be chagned
        if key == 'userId' or key == 'ownerEmail' \
          or key == 'lastModifiedDate' or key == "id":
            continue
        # If there's no special condition, just update directly
        elif key in kwargs:
            setattr(product, key, val)

    product.lastModifiedDate = dt.datetime.now()
    db.session.commit()
    return True
