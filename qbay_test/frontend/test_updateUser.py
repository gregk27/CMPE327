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
        # Generate uuid, will be reused for user and session
        self.uuid = str(uuid4())
        uuid = self.uuid
        print(uuid)
        s = db.session
        # Clean up database
        s.execute("DELETE FROM user WHERE username='Frontend UpTest'")
        # Set up the database, use SQL queries so no dependency on backend
        # or other pages
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance,\
                              shippingAddress, postalCode)\
            VALUES ('"+uuid+"', 'Frontend UpUser', 'front.upUser@test.com',\
                    '', 500, '560 Kingston Dr', 'K7L2G2')")
        db.session.execute("\
            INSERT INTO session (sessionId, userId, ipAddress)\
            VALUES ('"+uuid+"', '"+uuid+"', '127.0.0.1')")
        db.session.commit()
        print("Session registered")
        yield
        print("TEARDOWN")
        # Clean up database
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
        self.open(base_url + '/user/modify')
        # Update username partition
        self.type("#username", "New Username")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that name was changed (because of redirect this proves db)
        newVal = self.find_element("#username").get_attribute("value")
        assert newVal == "New Username"

        # Update shipping address partition
        self.type("#shippingAddress", "This is an updated shipping address")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that shipping address was changed
        newVal = self.find_element("#shippingAddress").get_attribute("value")
        assert newVal == "This is an updated shipping address"

        # Update postal code partition
        self.type('#postalCode', "L5B0A9")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that postal code was changed
        newVal = self.find_element("#postalCode").get_attribute("value")
        assert newVal == "L5B0A9"

    def test_r3_2(self, *_):
        """
        Test that shipping address can only be an alphanumeric
        value
        From setup code, shipping address is currently empty
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # open modify page
        self.open(base_url + '/user/modify')

        msg = ""

        # Invalid shippingAddress partition (can only be alphanumeric)
        # Get error message to check against
        try:
            updateUser(self.uuid, shippingAddress="560 $horeline_drive")
        except ValueError as e:
            msg = e
        print(msg)

        # Input invalid shipping address
        self.type("#shippingAddress", "560 $horeline_drive")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that error message is correct
        self.assert_text(msg, "#message")

        # Update postal code partition
        self.type('#postalCode', "L5B0A9")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that postal code was changed
        newVal = self.find_element("#postalCode").get_attribute("value")
        assert newVal == "L5B0A9"

    def test_r3_3(self, *_):
        """
        Test that postal code is a valid Canadian postal code
        From setup code, postal code is currently empty
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # open modify page
        self.open(base_url + '/user/modify')

        msg = ""

        # Invalid postalCode partition
        # Get error message to check against
        try:
            updateUser(self.uuid, postalCode="Z1W321")
        except ValueError as e:
            msg = e
        print(msg)

        # Input invalid postal code
        self.type("#postalCode", "Z1W321")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that error message is correct
        self.assert_text(msg, "#message")

    def test_r3_4(self, *_):
        """
        Test that username follows the requirements above
        From setup code, the username is Frontend UpUser
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # open modify page
        self.open(base_url + '/user/modify')

        msg = ""

        # Invalid username partition
        # Get error message to check against
        try:
            updateUser(self.uuid, username="!2")
        except ValueError as e:
            msg = e
        print(msg)

        # Input invalid username
        self.type("#username", "!2")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(0.5)

        # Assert that error message is correct
        self.assert_text(msg, "#message")
