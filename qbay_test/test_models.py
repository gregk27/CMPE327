from datetime import datetime

from qbay.models import db, Product, User, updateProduct # NOQA
import uuid
import pytest
import os

# def test_r1_7_user_register():
#     '''
#     Testing R1-7: If the email has been used, the operation failed.
#     '''

#     assert register('u0', 'test0@test.com', '123456') is True
#     assert register('u0', 'test1@test.com', '123456') is True
#     assert register('u1', 'test0@test.com', '123456') is False


# def test_r2_1_login():
#     '''
#     Testing R2-1: A user can log in using her/his email address
#       and the password.
#     (will be tested after the previous test, so we already have u0,
#       u1 in database)
#     '''

#     user = login('test0@test.com', 123456)
#     assert user is not None
#     assert user.username == 'u0'

#     user = login('test0@test.com', 1234567)
#     assert user is None

def test_r5_1_updateProduct():
    '''
    Testing R5-1: One can update all attributes of the product,
        except owner_email and last_modified_date.
    '''
    u = User(
        id=str(uuid.uuid4()),
        username="Test User",
        email="testR5.1@example.com",
        password="",
        balance=0,
        sessions=[],
        products=[],
        reviews=[],
        buyTransactions=[],
        sellTransactions=[]
    )
    orgProd = Product(
        id=str(uuid.uuid4()),
        productName="Test Product",
        userId=u.id,
        ownerEmail=u.email,
        price=500,
        description="Lorem Ipsum Dolar Set Amet",
        lastModifiedDate=datetime.now(),
        user=u
    )

    db.session.add(u)
    db.session.add(orgProd)
    db.session.commit()

    newVals = {
        "id": "1234",
        "productName": "New Name",
        "userId": "1234",
        "ownerEmail": "invalid@test.ca",
        "price": 1000,
        "description": "The quick brown fox jumps over the lazy dog",
    }

    assert updateProduct(orgProd.id, **newVals) is True

    modProd = Product.query.filter_by(id=orgProd.id).first()

    #TODO: Test that changes are proprely comitted to the database file

    # Check that values are correct
    assert modProd is not None
    assert modProd.id == orgProd.id
    assert modProd.userId == orgProd.userId
    assert modProd.ownerEmail == orgProd.ownerEmail
    assert modProd.price == newVals['price']
    assert modProd.description == newVals['description']
