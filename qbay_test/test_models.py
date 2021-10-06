from qbay.models import * # NOQA
import datetime as dt


# def test_r1_7_user_register():
#     '''
#     Testing R1-7: If the email has been used,the operation failed.
#     '''

#     assert register('u0',ownerEmail='test0@test.com','123456') is True
#     assert register('u0','test1@test.com','123456') is True
#     assert register('u1',ownerEmail='test0@test.com','123456') is False


# def test_r2_1_login():
#     '''
#     Testing R2-1: A user can log in using her/his email address
#       and the password.
#     (will be tested after the previous test,so we already have u0,
#       u1 in database)
#     '''

#     user=login(ownerEmail='test0@test.com',123456)
#     assert user is not None
#     assert user.username == 'u0'

#     user=login(ownerEmail='test0@test.com',1234567)
#     assert user is None


def test_r4_1_create_product():
    """
    Testing R4-1: Title of the product has to be alphanumeric-only,
      and space allowed only if it is not as prefix and suffix.
    """
    # Space as prefix
    assert createProduct(productName='p0',
      description=' This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Space as suffix
    assert createProduct(productName='p0',
      description='This is a test description ',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Check Alphanum only
    assert createProduct(productName='p0',
      description='This is @ test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Alphanum and spaces not as prefix or suffix (Passing case)
    assert createProduct(productName='p1',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True

def test_r4_2_create_product():
    """
    Testing R4-2: The title of the product is no longer than 80 characters.
    """
    # Title > 81 chars
    assert createProduct(productName='a'*81,
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Title == 80 chars (Passing case)
    assert createProduct(productName='a'*80,
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_3_create_product():
    """
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    """
    # Description < 20 chars
    assert createProduct(productName='p0',
      description='a'*19,
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Description > 2000 chars
    assert createProduct(productName='p0',
      description='a'*2001,
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Description is made of arbitrary chars, length [20, 2000] (Passing case)
    assert createProduct(productName='p2',
      description='abcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()./?<>[]{}\|',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_4_create_product():
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
    # Description length shorter than title
    assert createProduct(productName='a'*25,
      description='a'*20,
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Description length equal to title
    assert createProduct(productName='a'*20,
      description='a'*20,
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Description length longer than title (Passing case)
    assert createProduct(productName='a'*21,
      description='a'*22,
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_5_create_product():
    """
    Testing R4-5: Price has to be of range [10,10000].
    """
    # Price < 10.0
    assert createProduct(productName='p0',
      description='This is a test description',
      price=9.99,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Price > 10000.0
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10000.01,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False

    # Price in between [10, 10000] (Passing case)
    assert createProduct(productName='p3',
      description='This is a test description',
      price=100.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_6_create_product():
    """
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    """
    # Date == 2021-01-02
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,1,2),
      ownerEmail='test0@test.com') is False

    # Date == 2025-01-02
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2025,1,2),
      ownerEmail='test0@test.com') is False

    # Date in between (2021-01-02, 2025-01-02) (Passing case)
    assert createProduct(productName='p4',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_7_create_product():
    """
    Testing R4-7: owner_email cannot be empty. The owner of the corresponding
      product must exist in the database.
    """
    # ownerEmail == ""
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='') is False

    # ownerEmail == None
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail=None) is False

    # ownerEmail == stevending@test.com (email DNE in database)
    assert createProduct(productName='p0',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='stevending@test.com') is False
    
    # ownerEmail == test0@test.com (Existing email) (Passing case)
    assert createProduct(productName='p5',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is True


def test_r4_8_create_product():
    """
    Testing R4-8: A user cannot create products that have the same title.
    """
    
    # Already created p1
    assert createProduct(productName='p1',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test0@test.com') is False
    
    # Different user creating product with p1 (Passing case)
    assert createProduct(productName='p1',
      description='This is a test description',
      price=10.0,
      lastModifiedDate=dt.datetime(2021,10,8),
      ownerEmail='test1@test.com') is False


