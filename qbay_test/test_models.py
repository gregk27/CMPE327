from qbay.models import register
from qbay.models import queryUser
from qbay.models import * # NOQA
from qbay.models import createProduct
import datetime as dt


# def test_r1_7_user_register():
#     '''
#     Testing R1-7: If the email has been used,the operation failed.
#     '''

#     assert register('u0',owner_email='test0@test.com','123456') is True
#     assert register('u0','test1@test.com','123456') is True
#     assert register('u1',owner_email='test0@test.com','123456') is False


# def test_r2_1_login():
#     '''
#     Testing R2-1: A user can log in using her/his email address
#       and the password.
#     (will be tested after the previous test,so we already have u0,
#       u1 in database)
#     '''

#     user=login(owner_email='test0@test.com',123456)
#     assert user is not None
#     assert user.username == 'u0'

#     user=login(owner_email='test0@test.com',1234567)
#     assert user is None


def test_r4_1_create_product():
    """
    Testing R4-1: Title of the product has to be alphanumeric-only,
      and space allowed only if it is not as prefix and suffix.
    """
    # Space as prefix
    assert createProduct(title='p0',
                         description=' This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Space as suffix
    assert createProduct(title='p0',
                         description='This is a test description ',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Check Alphanum only
    assert createProduct(title='p0',
                         description='This is @ test description',
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
    # Title > 81 chars
    assert createProduct(title='a'*81,
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is False

    # Title == 80 chars (Passing case)
    assert createProduct(title='a'*80,
                         description='This is a test description',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_3_create_product():
    """
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    """
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
                         ' !@#$%^&*()./?<>[]{}|\\',
                         price=10.0,
                         last_modified_date=dt.datetime(2021, 10, 8),
                         owner_email='test0@test.com') is True


def test_r4_4_create_product():
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
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
                         owner_email='test1@test.com') is False


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
