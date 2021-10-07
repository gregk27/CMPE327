from qbay.models import register
from qbay.models import queryUser
from qbay.models import * # NOQA


def test1():
    assert True

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
