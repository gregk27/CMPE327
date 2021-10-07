from qbay.models import db, User, login, register, queryUser
import pytest
import uuid


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


@pytest.mark.parametrize('email, password, ip, resultA, resultB', [
    # Test User A login
    ['testA.R2.1@test.com', 'password', '123.456.789.123', True, False],
    # Test User A invalid password
    ['testA.R2.1@test.com', 'wrongpass', '123.456.789.123', False, False],
    # Test User B login
    ['testB.R2.1@test.com', 'Password2.0', '123.456.789.123', False, True],
    # Test User A with B's password
    ['testA.R2.1@test.com', 'Password2.0', '123.456.789.123', False, False]
])
def test_r2_1_login(email, password, ip, resultA, resultB):
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    '''

    # Define data for test users
    # Use dict instead of instance so it's not changed
    testUserA = {
        "id": str(uuid.uuid4()),
        "username": "Test A R2-1",
        "email": "testA.R2.1@test.com",
        # Salted hash for "password"
        "password": "b55ba5a4-e531-4343-ae73-31dfe5f3c8af:\
8e30d08b613f3813a117ad02e19b6e547fb45d11004e800\
de7e1099363b8bbf8fa11c6430cca26941c5241c73191ee\
02747841fe23a76f8ddbf14dbf2a41ddff",
        "balance": 0
    }

    testUserB = {
        "id": str(uuid.uuid4()),
        "username": "Test B R2-1",
        "email": "testB.R2.1@test.com",
        # Salted hash for "Password2.0"
        "password": "3fd20e2b-95ac-420e-83b2-e3b0100f7d80:\
f4935e405a07f5985d4fd8fbc0a19485dc2879247942d8a\
90914d8d052476606ec88cb5360b4ec5718ea61790b8870\
5d44fe82797b419479713d4462e4807eae",
        "balance": 0
    }

    # Create test users, delete and recreate if exist
    db.session.execute("DELETE FROM user WHERE email LIKE '%R2.1@test.com'")
    db.session.add(User(**testUserA))
    db.session.add(User(**testUserB))
    db.session.commit()

    session = login(email, password, ip)

    if(resultA or resultB):
        assert session is not None
        assert (session.user.id == testUserA['id']) is resultA
        assert (session.user.id == testUserB['id']) is resultB
        assert session.ipAddress == ip
    else:
        assert session is None
