from qbay.models import db, User, login # NOQA
import pytest
import uuid

# def test_r1_7_user_register():
#     '''
#     Testing R1-7: If the email has been used, the operation failed.
#     '''

#     assert register('u0', 'test0@test.com', '123456') is True
#     assert register('u0', 'test1@test.com', '123456') is True
#     assert register('u1', 'test0@test.com', '123456') is False


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
