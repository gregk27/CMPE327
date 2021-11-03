from seleniumbase import BaseCase
from uuid import uuid4
import pytest

from qbay_test.conftest import base_url
from qbay.models import db
from qbay.backend import updateUser


class FrontEndUserUpdatePageTest(BaseCase):

    @pytest.fixture(autouse=True)
    def login(self, *_):
        print("Setup")
        self.uuid = str(uuid4())
        uuid = self.uuid
        print(uuid)
        s = db.session

        s.execute("DELETE FROM user WHERE username='Frontend UpTest'")
        s.execute("DELETE FROM user WHERE email='front.upUser@test.com")

        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance)\
            VALUES ('"+uuid+"', 'Frontend UpUser', 'front.upUser@test.com',\
                    '', 500)")

        db.session.execute("\
            INSERT INTO session (sessionId, userId, ipAddress)\
            VALUES ('"+uuid+"', '"+uuid+"', '127.0.0.1')")
        db.session.commit()
        print("Session registered")
        yield
        print("TEARDOWN")

        db.session.execute(f"DELETE FROM session WHERE sessionId='{uuid}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid}'")
        db.session.commit()

    def test_r3_1(self, *_):
        """

        Test that all available parameters can be set
        This is a test using functional partitioning, partitioned as follows
        - user can update username
        - user can update shippingAddress
        - user can update postalCode
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # open modify pagep
        self.open(base_url + '/user/update/Frontend UserUp Test')

        self.type("#username", "New Username")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        newVal = self.find_element("#username").get_attribute("value")
        assert newVal == "New Username"

        self.type("#shippingAddress", "This is an updated shipping address")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        newVal = self.find_element("#shippingAddress").get_attribute("value")
        assert newVal == "This is an updated shipping address"

        self.type('#postalCode', "L5B0A9")
        self.click('input[type="submit"]')
        self.wait(0.5)

        newVal = self.find_element("#postalCode").get_attribute("value")
        assert newVal == "L5B0A9"

    def test_r5_2(self, *_):
        self.open(base_url + f'/_test/{self.uuid}')
        self.open(base_url + '/user/update/Frontend UserUp Test')

        msg = ""

        try:
            updateUser(self.uuid, shippingAddress="560 $horeline_drive")
        except ValueError as e:
            msg = e
        print(msg)
