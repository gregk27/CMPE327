from seleniumbase import BaseCase
from uuid import uuid4
import pytest

from qbay_test.conftest import base_url
from qbay.models import db

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndProductUpdatePageTest(BaseCase):

    @pytest.fixture(autouse=True)
    def login(self, *_):
        print("SETUP")
        # Generate uuid, will be reused for user, product and session
        self.uuid = str(uuid4())
        uuid = self.uuid
        print(uuid)
        s = db.session
        # Clean up database
        s.execute("DELETE FROM product WHERE productName='Frontend UpTest'")
        s.execute("DELETE FROM user WHERE email='front.upProd@test.com'")
        # Set up the database, use SQL queries so no dependency on backend
        # or other pages
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance)\
            VALUES ('"+uuid+"', 'Frontend UpProd', 'front.upProd@test.com',\
                    '', 500)")
        db.session.execute("\
            INSERT INTO product (id, productName, userId, ownerEmail,\
                 price, description, lastModifiedDate)\
            VALUES ('"+uuid+"', 'Frontend ProdUp Test', '"+uuid+"',\
                'front.upProd@test.com', 1000, 'Product to test frontend',\
                CURRENT_TIMESTAMP)")
        db.session.execute("\
            INSERT INTO session (sessionId, userId, ipAddress)\
            VALUES ('"+uuid+"', '"+uuid+"', '127.0.0.1')")
        db.session.commit()
        print("Session registered")
        yield
        print("TEARDOWN")
        # Clean up database
        db.session.execute(f"DELETE FROM product WHERE id='{uuid}'")
        db.session.execute(f"DELETE FROM session WHERE sessionId='{uuid}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid}'")
        db.session.commit()

    def test_r5_1(self, *_):
        """
        Test that all available parameters can be set
        This is a test using functional paritioning, paritioned as follows
         - user can update name
         - user can update description
         - user can update price
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # open modify page
        self.open(base_url + '/product/update/Frontend ProdUp Test')

        # Update name partition
        self.type("#name", "New product name")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(2)

        # Assert that name was changed (because of redirect this proves db)
        newVal = self.find_element("#name").get_attribute("value")
        assert newVal == "New product name"

        # Update description partition
        self.type("#desc", "This is an updated description")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(2)

        # Assert that description was changed
        newVal = self.find_element("#desc").get_attribute("value")
        assert newVal == "This is an updated description"

        # Update description partition
        self.type("#price", "2500")
        # click enter button
        self.click('input[type="submit"]')
        self.wait(2)

        # Assert that description was changed
        newVal = self.find_element("#price").get_attribute("value")
        assert float(newVal) == 2500
