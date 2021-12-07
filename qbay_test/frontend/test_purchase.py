import pytest
from seleniumbase import BaseCase
from uuid import uuid4

from qbay_test.conftest import base_url
from qbay.models import Product, db
from qbay.backend import purchaseProduct


class FrontEndProductPurchaseTest(BaseCase):

    @pytest.fixture(autouse=True)
    def login(self, *_):
        print("Setup")
        # Generate uuid, will be reused for user and session
        self.uuid = str(uuid4())
        uuid = self.uuid
        print(uuid)
        s = db.session
        # Clean up databases
        s.execute("DELETE FROM product WHERE productName='Frontend upTest'")
        s.execute("DELETE FROM user WHERE email='front.buyProd@test.com'")
        # Set up the database, use SQL queries so no dependency on backend
        # or other pages
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance,\
                              shippingAddress, postalCode)\
            VALUES ('"+uuid+"', 'Frontend UpUser', 'front.upUser@test.com',\
                    '', 500, '560 Kingston Dr', 'K7L2G2')")
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance,\
                              shippingAddress, postalCode)\
            VALUES ('user1', 'Frontend UpUser Two', 'front.upUser2@test.com',\
                    '', 500, '560 Kingston Dr', 'K7L2G2')")
        db.session.execute("\
            INSERT INTO product (id, productName, userId, ownerEmail,\
                 price, description, lastModifiedDate, sold)\
            VALUES ('1234', 'Frontend ProdUp Test', '1234',\
                'front.upProd@test.com', 1000, 'Product to test frontend',\
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
            INSERT INTO product (id, productName, userId, ownerEmail,\
                 price, description, lastModifiedDate, sold)\
            VALUES ('"+uuid+"', 'Frontend ProdUp Test 2', '"+uuid+"',\
                'front.upProd@test.com', 300, 'Product to test frontend',\
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
            INSERT INTO product (id, productName, userId, ownerEmail,\
                 price, description, lastModifiedDate, sold)\
            VALUES ('4567', 'Frontend ProdUp Test 3', '4567',\
                'front.upProd@test.com', 1000, 'Product to test frontend',\
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
            INSERT INTO session (sessionId, userId, ipAddress)\
            VALUES ('"+uuid+"', '"+uuid+"', '127.0.0.1')")
        db.session.commit()
        print("Session registered")
        yield
        print("TEARDOWN")
        db.session.execute(f"DELETE FROM product WHERE id='{uuid}'")
        db.session.execute(f"DELETE FROM session WHERE sessionId='{uuid}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid}'")
        db.session.commit()

    def test_purchase_1(self, *_):
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        msg = ""

        # Click buy button
        self.click('input[type="submit"]')
        self.wait(0.5)

        purchaseProduct(self.uuid, '1234')

        newVal = self.find_element('#prod.sold').get_attribute("value")
        assert newVal is True

        try:
            purchaseProduct('user1', '1234')
        except ValueError as e:
            msg = e
        print(msg)

    def test_purchase_2(self, *_):
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        msg = ""

        try:
            purchaseProduct(self.uuid, self.uuid)
        except ValueError as e:
            msg = e
        print(msg)

        self.assert_text(msg, "#message")

    def test_purchase_3(self, *_):
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        msg = ""

        try:
            purchaseProduct(self.uuid, "4567")
        except ValueError as e:
            msg = e
        print(msg)

        self.assert_text(msg, "#message")
