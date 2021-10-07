from qbay.models import db, User, login, register, queryUser
from uuid import uuid4
import hashlib
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

    # Delete user when done
    db.session.delete(user)
    db.session.commit()

    assert (session is not None) is result
