import pytest
from seleniumbase import BaseCase
from uuid import uuid4

from qbay_test.conftest import base_url
from qbay.models import Product, db


class FrontEndProductPurchaseTest(BaseCase):

    @pytest.fixture(autouse=True)
    def login(self, *_):
        print("Setup")
        # Generate uuid, will be reused for user and session
        self.uuid = str(uuid4())
        self.uuid2 = str(uuid4())
        self.uuid3 = str(uuid4())
        uuid = self.uuid
        uuid2 = self.uuid2
        uuid3 = self.uuid3
        print(uuid)
        print(uuid2)
        print(uuid3)
        s = db.session
        # Clean up databases
        s.execute("DELETE FROM product WHERE productName='Frontend buyTest'")
        s.execute("DELETE FROM user WHERE username='Test0'")
        s.execute("DELETE FROM user WHERE username='Test1'")
        s.execute("DELETE FROM user WHERE username='Test2'")
        # Set up the database, use SQL queries so no dependency on backend
        # or other pages
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance)\
            VALUES ('"+uuid+"', 'Test0', 'test0@test.com',\
                    '', 1000)")
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance)\
            VALUES ('"+uuid2+"', 'Test1', 'testSeller1@test.com',\
                    '', 500)")
        db.session.execute("\
            INSERT INTO user (id, username, email, password, balance)\
            VALUES ('"+uuid3+"', 'Test3', 'testSeller2@test.com',\
                    '', 500)")
        db.session.execute("\
            INSERT INTO product (id, productName, userId, ownerEmail,\
                 price, description, lastModifiedDate, sold)\
            VALUES('"+uuid+"', 'P1', '"+uuid+"',\
                'front.buyProd@test.com', 300, 'Product to test frontend',\
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
                    INSERT INTO product (id, productName, userId, ownerEmail,\
                         price, description, lastModifiedDate, sold)\
                    VALUES ('"+uuid2+"', 'P2', '"+uuid2+"',\
                'front.buyProd2@test.com', 300, 'Product to test frontend',\
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
                    INSERT INTO product (id, productName, userId, ownerEmail,\
                                 price, description, lastModifiedDate, sold)\
                    VALUES('"+uuid3+"', 'P3', '"+uuid3+"', \
                'front.buyProd3@test.com', 1100, 'Product to test frontend', \
                CURRENT_TIMESTAMP, false)")
        db.session.execute("\
            INSERT INTO session (sessionId, userId, ipAddress)\
            VALUES ('"+uuid+"', '"+uuid+"', '127.0.0.1')")
        db.session.commit()
        print("Session registered")
        print(uuid)
        print(uuid4())
        yield
        print("TEARDOWN")
        db.session.execute(f"DELETE FROM product WHERE id='{uuid}'")
        db.session.execute(f"DELETE FROM product WHERE id='{uuid2}'")
        db.session.execute(f"DELETE FROM product WHERE id='{uuid3}'")
        db.session.execute(f"DELETE FROM session WHERE sessionId='{uuid}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid2}'")
        db.session.execute(f"DELETE FROM user WHERE id='{uuid3}'")
        db.session.commit()

    def test_purchase_1(self, *_):
        """
        Test that user can purchase a product
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        self.wait(5)

        # Click buy button
        self.click("#prod-"+self.uuid2+" input[type=submit]")
        self.wait(0.5)

        # Check if the product has been sold
        Prod = Product.query.filter_by(id=self.uuid2).first()

        assert Prod.sold is True

        # Refresh home page
        self.open(base_url + '/')

        # Test that product listed in purchase history (and not available)
        self.wait(5)
        self.assert_element("#purchases #prod-"+self.uuid2)
        self.assert_element_absent("#available #prod-"+self.uuid2)

    def test_purchase_2(self, *_):
        """
        Test that user cannot buy their own products
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        # Assert the product does not have a buy buttton
        self.assert_element_absent("#prod-"+self.uuid+" input[type=submit]")

    def test_purchase_3(self, *_):
        """
        Test that user cannot place an order
        that costs more than available balance
        """
        # Set session token
        self.open(base_url + f'/_test/{self.uuid}')
        # Open home page
        self.open(base_url + '/')

        self.wait(5)

        # Assert that the buy button is disabled for the expensive product
        self.assert_attribute('#prod-'+self.uuid3+' input[type="submit"]',
                              "disabled", 'true')
