import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.dialects.postgresql import UUID
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Declare a base
Base = declarative_base()


class User(db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# Source: https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html
# Used for including product image
class Product(Base):
    """Product model."""
    id = db.Column(db.Integer, primary_key=True)
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

    productId = db.Column(db.Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
    __tablename__ = 'product_picture'


# Using postgresql for UUID
class Sessions(db.Model):
    """Session model."""
    userId = db.Column(db.String)
    sessionId = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expiry = db.Column(db.String)
    ipAddress = db.Column(db.String)
    csrfToken = db.Column(db.String)
    __tablename__ = "session"
