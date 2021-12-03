from qbay.models import db, User, Product, Session
from qbay.backend import purchaseProduct, updateProduct, register, \
    queryUser, createProduct, login, updateUser
import datetime as dt
import hashlib
import pytest
from uuid import uuid4


@pytest.mark.parametrize("username, email, password, expected", [
    # R1-1: Both the email and password cannot be empty
    # Expected False due to empty email
    ['will', '', 'password1235#', False],
    # Expected False due to empty password
    ['nate', 'nate123@gmail.com', '', False],

    # R1-2 and R1-7: A user is uniquely identified by their email
    #     address. If the email has been used, the operation failed.
    # Register user to use email
    ['damien smith', 'dambam07@gmail.com', 'asdjDD123asd/&$', True],
    # Expected False due to duplicate email
    ['jonathon', 'dambam07@gmail.com', 'askdhD123%$#', False],

    # R1-3: The email has to follow addr-spec defined in RFC 5322
    # Expected true baseline test
    ['jon123', 'jon#$^asd@gmail.com', 'asdDi8uh18798asd$', True],
    # Expected False due to email not following addr-spec defined in RFC 5322
    ['damien', 'test@..@test.com', 'password123$', False],

    # R1-4: Password has to meet the required complexity: minimum
    #     length 6, at least one upper case, at least one lower case,
    #     and at least one special character.
    # Expected true baseline test
    ['jacob', 'jacobkie@gmail.com', 'ValidPassword123$$', True],
    # Expected False due to lack of password complexity
    ['daniel fran', 'danfran@gmail.com', 'password', False],

    # R1-5: User name has to be non-empty, alphanumeric-only, and space
    #     allowed only if it is not as the prefix or suffix.
    # Expected False due non-alphanumeric username
    ['name$$', 'hellotesting@gmail.com', 'ValidPassword123&', False],
    # Expected False due to empty username
    ['', 'something@hotmail.com', 'passwrod123&', False],
    # Expected False due to whitespace in prefix of username
    [' jake', 'jake@gmail.com', 'ppassword123&^$', False],
    # Expected False due to whitespace in suffix of username
    ['kaitlyn ', 'katlubsd123@hotmail.com', 'Password123&', False],

    # R1-6: User name has to be longer than 2 characters and less
    #     than 20 characters.
    # Expected False due to username length < 3
    ['u', 'test0129387@test.com', 'asdao8u98u198h$', False],
    # Expected False due to username length > 20
    ['shdmienshtush smithasdoqwieusdh', 'validemailadd@gmail.com',
     'validpswd1%', False]
])
def test_r1_register(username, email, password, expected):
    '''
    Testing R1-X using various parameterized inputs.
    '''
    assert register(username, email, password) is expected


@pytest.mark.parametrize("email, attribute, value", [
    # Testing R1-8: Shipping address is empty at the time of registration.
    ['dambam07@gmail.com', 'shippingAddress', ''],
    # Testing R1-9: Postal code is empty at the time of registration.
    ['dambam07@gmail.com', 'postalCode', ''],
    # Testing R1-10: Balance should be initialized as 100 at the
    #   time of registration.
    ['dambam07@gmail.com', 'balance', '100'],
])
def test_r1_8_10_register(email, attribute, value):
    assert queryUser(email, attribute, value) is True


@pytest.mark.parametrize('email, password, ip, resultA, resultB', [
    # Test User A login
    ['R2.1A@test.com', 'P&ssw0rd', '123.456.789.123', True, False],
    # Test User A invalid password
    ['R2.1A@test.com', 'wr0ngp&ss', '123.456.789.123', False, False],
    # Test User B login
    ['R2.1B@test.com', 'Password2.0!', '123.456.789.123', False, True],
    # Test User A with B's password
    ['R2.1A@test.com', 'Password2.0!', '123.456.789.123', False, False]
])
def test_r2_1_login(email, password, ip, resultA, resultB):
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    '''

    testUserA = {"name": "R2 1 Test A", "email": "R2.1A@test.com",
                 "password": "P&ssw0rd"}
    testUserB = {"name": "R2 1 Test B", "email": "R2.1B@test.com",
                 "password": "Password2.0!"}

    # Register test users if they don't exist
    register(**testUserA)
    register(**testUserB)

    session = login(email, password, ip)

    # If its expected that one of the users is logged in, check for correctness
    if(resultA or resultB):
        # Check that session was returned
        assert session is not None
        # Check whether it is/should be user A
        assert (session.user.username == testUserA['name']) is resultA
        assert (session.user.email == testUserA['email']) is resultA
        # Check whether it is/should be user B
        assert (session.user.username == testUserB['name']) is resultB
        assert (session.user.email == testUserB['email']) is resultB
        # Check that ip set correctly
        assert session.ipAddress == ip
    else:
        # Otherwise, make sure no session was created incorrectly
        assert session is None


@pytest.mark.parametrize("email, password, result", [
    # Baseline with valid credentials
    ['R2.2@test.com', 'P&ssw0rd', True],
    # R1-1 Empty email
    ['R2.2@test.com', '', False],
    # R1-3 Invalid email
    ['test@..@test.com', 'P&ssw0rd', False],
    # R1-4a Passowrd too short
    ['R2.2@test.com', 'P&s5', False],
    # R1-4b Passowrd missing caps
    ['R2.2@test.com', 'p&ssw0rd', False],
    # R1-4c Passowrd missing special/num
    ['R2.2@test.com', 'Password', False],
])
def test_r2_2_login(email, password, result):
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    '''

    # Create a new user from parameters
    # Can't use register since this user breaks database restrictions
    salt = uuid4()
    hashed = str(salt) + ":" + hashlib.sha512((password + str(salt))
                                              .encode('utf-8')).hexdigest()
    user = User(id=str(uuid4()), username="R2 2 test", email=email,
                password=hashed, balance=100, shippingAddress="",
                postalCode="")
    db.session.add(user)
    db.session.commit()

    # Attempt to log in and validate result
    session = login(email, password, '123.456.789.123')

    if(session is not None):
        db.session.delete(Session.query.filter_by(sessionId=session.sessionId)
                          .one_or_none())
    # Delete user when done
    db.session.delete(user)
    db.session.commit()

    assert (session is not None) is result


@pytest.mark.parametrize("target, newVals, shouldChange", [
    [
        "R3.1",  # One can only update username, shippingAddress,
                 # and postalCode.
        {
            "id": "1234",
            "username": "New username",
            "email": "invalid@test.ca",
            "password": "Ppassword1!",
            "balance": 1000,
            "shippingAddress": "123 Kingston Road",
            "postalCode": "K7L2G2"
        },
        {
            "username": True,
            "shippingAddress": True,
            "postalCode": True,
        }
    ],
    [
        "R3.2A",  # shippingAddress has to be non-empty
                  # and contain no special characters
        {
            "id": "1234",
            "username": "New username",
            "email": "invalid@test.ca",
            "password": "Ppassword1!",
            "balance": 1000,
            "shippingAddress": "123 K!ngston Road",
            "postalCode": "K7L2G2"
        },
        {
            "username": True,
            "shippingAddress": False,
            "postalCode": True,
        }
    ],
    [
        "R3.2B",  # shippingAddress has to be non-empty
                  # and contain no special characters
        {
            "id": "1234",
            "username": "New username",
            "email": "invalid@test.ca",
            "password": "Ppassword1!",
            "balance": 1000,
            "shippingAddress": "  ",
            "postalCode": "K7L2G2"
        },
        {
            "username": True,
            "shippingAddress": False,
            "postalCode": True,
        }
    ],
    [
        "R3.3",  # postalCode has to be valid Canadian postal code
        {
            "id": "1234",
            "username": "New username",
            "email": "invalid@test.ca",
            "password": "Ppassword1!",
            "balance": 1000,
            "shippingAddress": "123 Kingston Road",
            "postalCode": "KK12w2"
        },
        {
            "username": True,
            "shippingAddress": True,
            "postalCode": False,
        }
    ],
])
def test_r3_updateUser(target, newVals, shouldChange):
    '''
    Testing all R3-x requirements using parameterization
    '''
    email = f"test{target}@example.com"
    register(f"Test User {target.replace('.', ' ')}", email, "Password1!")

    orgVals = {
        "id": "1234",
        "name": "Test User",
        "email": email,
        "password": "Password1!",
        "balance": 1000,
        "shippingAddress": "123 Kingston Road",
        "postalCode": "K7L2G2"
    }

    user = User.query.filter_by(email=orgVals["email"]).first()

    user.balance = orgVals['balance']
    user.shippingAddress = orgVals['shippingAddress']
    user.postalCode = orgVals['postalCode']

    orgVals['id'] = user.id
    try:
        assert updateUser(user.id, **newVals) is True
    except ValueError:
        assert not (shouldChange['username']
                    and shouldChange['shippingAddress']
                    and shouldChange['postalCode'])

    modUser = User.query.filter_by(id=orgVals["id"]).first()

    # Check that values are correct
    assert modUser is not None
    assert modUser.id == orgVals["id"]
    assert (modUser.username == newVals['username']) \
        is shouldChange['username']
    assert modUser.email == orgVals["email"]
    assert (modUser.shippingAddress == newVals['shippingAddress']) \
        is shouldChange['shippingAddress']
    assert (modUser.postalCode == newVals['postalCode']) \
        is shouldChange['postalCode']

    db.session.delete(user)
    db.session.commit()


@pytest.mark.parametrize("title, expected", [
    # Space as prefix
    [' p0', False],
    # Space as suffix
    ['p0 ', False],
    # Check Alphanum only
    ['p@', False],
    # Alphanum and spaces not as prefix or suffix (Passing case)
    ['p1', True]
])
def test_r4_1_create_product(title, expected):
    """
    Testing R4-1: Title of the product has to be alphanumeric-only,
      and space allowed only if it is not as prefix and suffix.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')
    try:
        assert createProduct(title,
                             description='This is a test description',
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('title, description, expected', [
    # Title > 81 chars
    ['a'*81, 'This is a test description', False],
    # Title == 80 chars (Passing case)
    ['a'*80, 'Test'*21, True],
])
def test_r4_2_create_product(title, description, expected):
    """
    Testing R4-2: The title of the product is no longer than 80 characters.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    try:
        assert createProduct(title,
                             description,
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('description, expected', [
    # Description < 20 chars
    ['a'*19, False],
    # Description > 2000 chars
    ['a'*2001, False],
    # Description is made of arbitrary chars, length [20, 2000] (Passing case)
    ['abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()./?<>[]|{}\\', True]
])
def test_r4_3_create_product(description, expected):
    """
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')
    try:
        assert createProduct(productName='p0',
                             description=description,
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('title, description, expected', [
    # Description length shorter than title
    ['a'*25, 'a'*20, False],
    # Description length equal to title
    ['a'*20, 'a'*20, False],
    # Description length longer than title (Passing case)
    ['a'*21, 'a'*22, True]
])
def test_r4_4_create_product(title, description, expected):
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    try:
        # Description length shorter than title
        assert createProduct(title,
                             description=description,
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('price, expected', [
    # Price < 10.0
    [9.99, False],
    # Price > 10000.0
    [10000.01, False],
    # Price in between [10, 10000] (Passing case)
    [100.0, True]
])
def test_r4_5_create_product(price, expected):
    """
    Testing R4-5: Price has to be of range [10,10000].
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    try:
        assert createProduct(productName='p2',
                             description='This is a test description',
                             price=price,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('date, expected', [
    # Date == 2021-01-02
    [dt.datetime(2021, 1, 2), False],
    # Date == 2025-01-02
    [dt.datetime(2025, 1, 2), False],
    # Date in between (2021-01-02, 2025-01-02) (Passing case)
    [dt.datetime(2021, 10, 8), True]
])
def test_r4_6_create_product(date, expected):
    """
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    try:
        assert createProduct(productName='p3',
                             description='This is a test description',
                             price=10.0,
                             last_modified_date=date,
                             owner_email='test0@test.com') is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('email, expected', [
    # owner_email == ""
    ['', False],
    # owner_email == None
    [None, False],
    # owner_email == stevending@test.com (email DNE in database)
    ['stevending@test.com', False],
    # owner_email == test0@test.com (Existing email) (Passing case)
    ['test0@test.com', True],
])
def test_r4_7_create_product(email, expected):
    """
    Testing R4-7: owner_email cannot be empty. The owner of the corresponding
      product must exist in the database.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    try:
        assert createProduct(productName='p4',
                             description='This is a test description',
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email=email) is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize('email, expected', [
    # Test0 has already created p1
    ['test0@test.com', False],
    # Different user creating product with p1 (Passing case)
    ['test1@test.com', True]
])
def test_r4_8_create_product(email, expected):
    """
    Testing R4-8: A user cannot create products that have the same title.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')
    register('Test1', 'test1@test.com', 'Password1!')

    # Register a test product, if exists pass error
    try:
        createProduct(productName='p5',
                      description='This is a test description',
                      price=10.0,
                      last_modified_date=dt.datetime(2021, 10, 8),
                      owner_email='test0@test.com') is expected
    except ValueError:
        pass

    try:
        assert createProduct(productName='p5',
                             description='This is a test description',
                             price=10.0,
                             last_modified_date=dt.datetime(2021, 10, 8),
                             owner_email=email) is expected
    except ValueError:
        assert not expected


@pytest.mark.parametrize("target, newVals, shouldChange", [
    [
        "R5.1",  # One can update all attributes of the product,
                 # except owner_email and last_modified_date.
        {
            "id": "1234",
            "productName": "New Name R5 1",
            "userId": "1234",
            "ownerEmail": "invalid@test.ca",
            "price": 1000,
            "description": "The quick brown fox jumps over the lazy dog",
        },
        {
            "productName": True,
            "price": True,
            "description": True,
        }
    ],
    [
        "R5.2",  # Price can be only increased but cannot be decreased
        {
            "id": "1234",
            "productName": "New Name R5 2",
            "userId": "1234",
            "ownerEmail": "invalid@test.ca",
            "price": 100,
            "description": "The quick brown fox jumps over the lazy dog",
        },
        {
            "productName": True,
            "price": False,
            "description": True,
        }
    ],
])
def test_r5_updateProduct(target, newVals, shouldChange):
    '''
    Testing all R5-x requirements using parameterization
    '''
    email = f"test{target}@example.com"
    register(f"Test User {target.replace('.', ' ')}", email, "Password1!")

    orgVals = {
        "productName": f"Test Product {target.replace('.', ' ')}",
        "owner_email": email,
        "price": 500,
        "description": "Lorem Ipsum Dolar Set Amet",
        "last_modified_date": dt.datetime.now(),
    }

    assert createProduct(**orgVals)
    prod = Product.query.filter_by(productName=orgVals["productName"],
                                   ownerEmail=orgVals["owner_email"]).first()
    orgVals['id'] = prod.id
    assert updateProduct(prod.id, **newVals) is True

    modProd = Product.query.filter_by(id=orgVals["id"]).first()

    # Check that values are correct
    assert modProd is not None
    assert modProd.id == orgVals["id"]
    assert (modProd.productName == newVals['productName']) \
        is shouldChange['productName']
    assert modProd.ownerEmail == orgVals["owner_email"]
    assert (modProd.price == newVals['price']) is shouldChange['price']
    assert (modProd.description == newVals['description']) \
        is shouldChange['description']
    # Verify R5-3
    assert modProd.lastModifiedDate != orgVals["last_modified_date"]


@pytest.mark.parametrize("target, changedVals, expected", [
    # Unchanged base test
    ["R4.0", {}, True],
    # Title must be alphanumeric
    ["R4.1A", {"productName": "inv&|id"}, False],
    # Title shorter than 80 characters
    ["R4.2",  {"productName": "Lorem ipsum dolor sit amet, consectetur adipiscing \
elit. Vivamus nec neque tincidunt."}, False],
    # Description minimum 20 characters
    ["R4.3",  {"description": "Short Desc"}, False],
    # Description maximum 2000 characters
    ["R4.3B",  {"description": "Long Desc"+"."*2000}, False],
    # Description maximum 2000 characters
    ["R4.4",  {"productName": "Longer than description title",
               "description": "Shorter that title desc"}, False],
    # Price above 10
    ["R4.5A",  {"price": 5}, False],
    # Price below 10000
    ["R4.5B",  {"price": 10001}, False],
    # Date too small
    ["R4.6A",  {"lastModifiedDate": dt.datetime(2021, 1, 1)}, False],
    # Date too big
    ["R4.6B",  {"lastModifiedDate": dt.datetime(2025, 1, 3)}, False],
    # R4-7 not tested as email cannot be changed
])
def test_r5_4_updateProduct(target, changedVals, expected):
    '''
    Testing all R5-4 subrequirements using parameterization
    '''
    email = f"test{target}@example.com"
    register(f"Test User {target.replace('.', ' ')}", email, "Password1!")

    orgVals = {
        "productName": f"Test Product {target.replace('.', ' ')}",
        "owner_email": email,
        "price": 500,
        "description": "Lorem Ipsum Dolar Set Amet",
        "last_modified_date": dt.datetime.now(),
    }

    assert createProduct(**orgVals)
    prod = Product.query.filter_by(productName=orgVals["productName"],
                                   ownerEmail=orgVals["owner_email"]).first()

    # Generate new values to use by making desired changes
    newVals = orgVals.copy()
    for key, val in changedVals.items():
        newVals[key] = val

    # Update product, if error raised and failure expected then test is passed
    try:
        assert updateProduct(prod.id, **newVals) is expected
    except ValueError:
        assert not expected


def test_placing_order():
    '''
    Test that a user can place an order so long that the order is not for their
    own product or costs more than their current balance.
    '''
    # Register test users, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')
    register('Test1', 'test1@test.com', 'Password1!')

    # Create test products, if exists will just return false
    createProduct(productName='tp',
                  description='This is a test description',
                  price=10.0,
                  last_modified_date=dt.datetime(2021, 10, 8),
                  owner_email='test0@test.com')
    createProduct(productName='p1',
                  description='This is a test description',
                  price=1000.0,
                  last_modified_date=dt.datetime(2021, 10, 8),
                  owner_email='test1@test.com')
    createProduct(productName='tpPass',
                  description='This is a test description',
                  price=10.0,
                  last_modified_date=dt.datetime(2021, 10, 8),
                  owner_email='test1@test.com')

    # Get userID and prodID (updates per case)
    user = User.query.filter_by(username='Test0').first()
    prod = Product.query.filter_by(productName='tp').first()

    with pytest.raises(ValueError):
        # User buying their own product
        purchaseProduct(user.id, prod.id)

    user = User.query.filter_by(username='Test0').first()
    prod = Product.query.filter_by(productName='p1').first()

    with pytest.raises(ValueError):
        # User buying a product greater than their balance
        purchaseProduct(user.id, prod.id)

    # User buys a product that is not their own and is less than
    # their balance (Passing case)
    user = User.query.filter_by(username='Test0').first()
    prod = Product.query.filter_by(productName='tpPass').first()
    assert purchaseProduct(user.id, prod.id) is True
