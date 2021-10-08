from qbay.models import Product, updateProduct, register, \
    queryUser, createProduct
import datetime as dt
import pytest


def test_r1_1_register():
    '''
    Testing R1-1: Both the email and password cannot be empty.
    '''
    # Expected False due to empty email
    assert register('will', '', 'password1235#') is False
    # Expected False due to empty password
    assert register('nate', 'nate123@gmail.com', '') is False


def test_r1_2_r1_7_register():
    '''
    Testing R1-2 and R1-7: A user is uniquely identified by their email
    address. If the email has been used, the operation failed.
    '''
    assert register('damien smith', 'dambam07@gmail.com',
                    'asdjDD123asd/&$') is True
    # Expected False due to duplicate email
    assert register('jonathon', 'dambam07@gmail.com', 'askdhD123%$#') is False


def test_r1_3_register():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322
    '''
    assert register('jon123', 'jon#$^asd@gmail.com',
                    'asdDi8uh18798asd$') is True
    # Expected False due to email not following addr-spec defined in RFC 5322
    assert register('damien smith', 'test@..@test.com',
                    'password123$') is False


def test_r1_4_register():
    '''
    Testing R1-4: Password has to meet the required complexity: minimum
    length 6, at least one upper case, at least one lower case, and at least
    one special character.
    '''
    assert register('jacob', 'jacobkie@gmail.com',
                    'ValidPassword123$$') is True
    # Expected False due to lack of password complexity
    assert register('daniel fran', 'danfran@gmail.com', 'password') is False


def test_r1_5_register():
    '''
    Testing R1-5: User name has to be non-empty, alphanumeric-only, and space
    allowed only if it is not as the prefix or suffix.
    '''
    # Expected False due non-alphanumeric username
    assert register('name$$', 'hellotesting@gmail.com',
                    'ValidPassword123&') is False
    # Expected False due to empty username
    assert register('', 'something@hotmail.com', 'passwrod123&') is False
    # Expected False due to whitespace in prefix of username
    assert register(' jake', 'jake@gmail.com', 'ppassword123&^$') is False
    # Expected False due to whitespace in suffix of username
    assert register('kaitlyn ', 'katlubsd123@hotmail.com',
                    'Password123&') is False


def test_r1_6_register():
    '''
    Testing R1-6: User name has to be longer than 2 characters and less
    than 20 characters.
    '''
    # Expected False due to username length < 3
    assert register('u', 'test0129387@test.com', 'asdao8u98u198h$') is False
    # Expected False due to username length > 20
    assert register('shdmienshtush smithasdoqwieusdh',
                    'validemailadd@gmail.com', 'validpswd1%') is False


def test_r1_8_register():
    '''
    Testing R1-8: Shipping address is empty at the time of registration.
    '''
    assert queryUser('dambam07@gmail.com', 'shippingAddress', '') is True


def test_r1_9_register():
    '''
    Testing R1-9: Postal code is empty at the time of registration.
    '''
    assert queryUser('dambam07@gmail.com', 'postalCode', '') is True


def test_r1_10_register():
    '''
    Testing R1-10: Balance should be initialized as 100 at the
    time of registration.
    '''
    assert queryUser('dambam07@gmail.com', 'balance', '100') is True


def test_r4_1_create_product():
    """
    Testing R4-1: Title of the product has to be alphanumeric-only,
      and space allowed only if it is not as prefix and suffix.
    """
    # Register a test user, if exists will just return false
    register('Test0', 'test0@test.com', 'Password1!')

    # Space as prefix
    assert createProduct(title=' p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Space as suffix
    assert createProduct(title='p0 ',
                         description='This is a test description ',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Check Alphanum only
    assert createProduct(title='p@',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Alphanum and spaces not as prefix or suffix (Passing case)
    assert createProduct(title='p1',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_2_create_product():
    """
    Testing R4-2: The title of the product is no longer than 80 characters.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # Title > 81 chars
    assert createProduct(title='a'*81,
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Title == 80 chars (Passing case)
    assert createProduct(title='a'*80,
                         description='Test'*21,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_3_create_product():
    """
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # Description < 20 chars
    assert createProduct(title='p0',
                         description='a'*19,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Description > 2000 chars
    assert createProduct(title='p0',
                         description='a'*2001,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Description is made of arbitrary chars, length [20, 2000] (Passing case)
    assert createProduct(title='p2',
                         description='abcdefghijklmnopqrstuvwxyz0123456789' +
                         ' !@#$%^&*()./?<>[]|{}\\',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_4_create_product():
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # Description length shorter than title
    assert createProduct(title='a'*25,
                         description='a'*20,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Description length equal to title
    assert createProduct(title='a'*20,
                         description='a'*20,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Description length longer than title (Passing case)
    assert createProduct(title='a'*21,
                         description='a'*22,
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_5_create_product():
    """
    Testing R4-5: Price has to be of range [10,10000].
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # Price < 10.0
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=9.99,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Price > 10000.0
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10000.01,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Price in between [10, 10000] (Passing case)
    assert createProduct(title='p3',
                         description='This is a test description',
                         price=100.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_6_create_product():
    """
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # Date == 2021-01-02
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 1, 2),
                         owner_email='test0@test.com') is False

    # Date == 2025-01-02
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2025, 1, 2),
                         owner_email='test0@test.com') is False

    # Date in between (2021-01-02, 2025-01-02) (Passing case)
    assert createProduct(title='p4',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_7_create_product():
    """
    Testing R4-7: owner_email cannot be empty. The owner of the corresponding
      product must exist in the database.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')

    # owner_email == ""
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='') is False

    # owner_email == None
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email=None) is False

    # owner_email == stevending@test.com (email DNE in database)
    assert createProduct(title='p0',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='stevending@test.com') is False

    # owner_email == test0@test.com (Existing email) (Passing case)
    assert createProduct(title='p5',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_8_create_product():
    """
    Testing R4-8: A user cannot create products that have the same title.
    """
    # Register a test user, if exists will just reurn false
    register('Test0', 'test0@test.com', 'Password1!')
    register('Test1', 'test1@test.com', 'Password1!')

    # Already created p1
    assert createProduct(title='p1',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Different user creating product with p1 (Passing case)
    assert createProduct(title='p1',
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test1@test.com') is True


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
        "title": f"Test Product {target.replace('.', ' ')}",
        "owner_email": email,
        "price": 500,
        "description": "Lorem Ipsum Dolar Set Amet",
        "last_modified_date": dt.datetime.now(),
    }

    assert createProduct(**orgVals)
    prod = Product.query.filter_by(productName=orgVals["title"],
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
    ["R4.1A", {"title": "inv&|id"}, False],
    # Title shorter than 80 characters
    ["R4.2",  {"title": "Lorem ipsum dolor sit amet, consectetur adipiscing \
elit. Vivamus nec neque tincidunt."}, False],
    # Description minimum 20 characters
    ["R4.3",  {"description": "Short Desc"}, False],
    # Description maximum 2000 characters
    ["R4.3B",  {"description": "Long Desc"+"."*2000}, False],
    # Description maximum 2000 characters
    ["R4.4",  {"title": "Longer than description title",
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
        "title": f"Test Product {target.replace('.', ' ')}",
        "owner_email": email,
        "price": 500,
        "description": "Lorem Ipsum Dolar Set Amet",
        "last_modified_date": dt.datetime.now(),
    }

    assert createProduct(**orgVals)
    prod = Product.query.filter_by(productName=orgVals["title"],
                                   ownerEmail=orgVals["owner_email"]).first()

    # Generate new values to use by making desired changes
    newVals = orgVals.copy()
    for key, val in changedVals.items():
        newVals[key] = val

    assert updateProduct(prod.id, **newVals) is expected
