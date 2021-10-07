
from qbay.models import * 
#NOQA

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

validateEmail('dambam07@gmail.com')

def test_user_register():
    '''
    Testing R2-1: A user can register with their email address, username and password
      (will be tested after the previous test, so we already have u0,
        u1 in database)
     '''
    assert validateEmail('dambam07@gmail.com') is True
    assert validateUser('damien') is True
    assert validatePswd('asdjDD123asd/&$') is True
    assert register('damien smith', 'dambam07@gmail.com', 'asdjDD123asd/&$') is True
    assert register('jon123', 'jon#$^asd@gmail.com', 'asdDi8uh18798asd$') is True
    #Expected False due to duplicate email
    assert register('jonathon', 'dambam07@gmail.com', 'askdhD123%$#') is False
    #Expected False due to username length < 3
    assert register('u', 'test0129387@test.com', 'asdao8u98u198h$') is False
    #Expected False due to username length > 20
    assert register('shdmienshtush smithasdoqwieusdh', 'validemailadd@gmail.com', 'validpswd1%') is False
    #Expected False due to email not following addr-spec defined in RFC 5322
    assert register('damien smith', 'test@..@test.com', 'password123$') is False
    #Expected False due to whitespace in prefix of username
    assert register(' jake', 'jake@gmail.com', 'ppassword123&^$') is False
    #Expected False due to lack of password complexity
    assert register('daniel fran', 'danfran@gmail.com', 'password') is False
    #Expected False due to empty username
    assert register('', 'something@hotmail.com', 'passwrod123&') is False
    #Expected False due to empty email
    assert register('will', '', 'password1235#') is False
    #Expected False due to empty password
    assert register('nate', 'nate123@gmail.com', '') is False


test_user_register()
'''
R1-1: Both the email and password cannot be empty.
 R1-2: A user is uniquely identified by his/her email address.
 R1-3: The email has to follow addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation). You can use external libraries/imports.
 R1-4: Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character.
 R1-5: User name has to be non-empty, alphanumeric-only, and space allowed only if it is not as the prefix or suffix.
 R1-6: User name has to be longer than 2 characters and less than 20 characters.
 R1-7: If the email has been used, the operation failed.
 R1-8: Shipping address is empty at the time of registration.
 R1-9: Postal code is empty at the time of registration.
 R1-10: Balance should be initialized as 100 at the time of registration. (free $100 dollar signup bonus).
'''