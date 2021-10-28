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
            VALUES ('"+uuid+"', 'Frontend UpTest', '"+uuid+"',\
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

