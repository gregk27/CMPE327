from seleniumbase import BaseCase
from qbay.backend import createProduct
from qbay.backend import register
import datetime as dt

from qbay_test.conftest import base_url

"""
This file defines all integration tests for the frontend product creation
functions and page.
"""


class ProductCreationTest(BaseCase):

    # Blackbox method - Functional Requirements
    def test_product_create_page(self, *_):
        """
        This is a test for the product creation page to
        verify if it has all the necessary fields.
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Open product creation page
        self.open(base_url + '/product/create')

        # Verify elements exist
        self.assert_element("#name")
        self.assert_element("#desc")
        self.assert_element("#price")
        self.assert_element("#btn-submit")

    # Blackbox method - Input Partitioning
    def test_name(self, *_):
        """
        Test various inputs for product name.
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test space in prefix in product name
        self.type("#name", " p0")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid name" in msg)

        # Test space in suffix in product name
        self.type("#name", "p0 ")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid name" in msg)

        # Test special character in product name
        self.type("#name", "p@")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid name" in msg)

        # Test length of product name (Cannot be >80)
        self.type("#name", "a"*81)
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid name" in msg)

        # Test correct product name input
        # Valid product name, length 80 chars
        # Description longer than title
        # Success will redirect to home page
        self.type("#name", "p1"*40)
        self.type("#desc", "This is a test description"*4)
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Go to home page
        self.open(base_url)
        # Confirm at home page
        self.assert_element("#welcome-header")
        # Check if product was created
        self.assert_text("p1"*40, "#products")

    def test_description(self, *_):
        """
        Test various inputs for product description.
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test description length < 20
        self.type("#name", "p0")
        self.type("#desc", "a"*19)
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid description" in msg)

        # Test description length > 2000
        self.type("#name", "p0")
        self.type("#desc", "a"*2001)
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid description" in msg)

        # Test description length <= title length
        self.type("#name", "p0")
        self.type("#desc", "aa")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid description" in msg)

        # Test correct production description input
        # Success will redirect to home page
        self.type("#name", "p1")
        self.type("#desc", "abcdefghijklmnopqrstuvwxyz" +
                  "0123456789!@#$%^&*()./?<>[]|{}\\")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Go to home page
        self.open(base_url)
        # Confirm at home page
        self.assert_element("#welcome-header")
        # Check if product was created
        self.assert_text("p1", "#products")

    def test_price(self, *_):
        """
        Test various inputs for product price.
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test price < 10
        self.type("#name", "p0")
        self.type("#desc", "This is a test description")
        self.type("#price", "9.99")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid price" in msg)

        # Test price > 10000
        self.type("#name", "p0")
        self.type("#desc", "This is a test description")
        self.type("#price", "10000.01")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid price" in msg)

        # Test price cannot be converted to float
        self.type("#name", "p0")
        self.type("#desc", "This is a test description")
        self.type("#price", "a")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("Invalid price" in msg)

        # Test correct price input
        # Success will redirect to home page
        self.type("#name", "p2")
        self.type("#desc", "This is a test description")
        self.type("#price", "100")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("100.0", "#products")

    def test_new_product(self, *_):
        """
        Test that a new product does not have the same
        name as an existing product. The other test cases
        already have different product names (pass case).
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Ensure the product is in the database,
        # ignore errors from pre-existance
        try:
            createProduct(productName="Product",
                          description="Product description",
                          price="10",
                          last_modified_date=dt.datetime(2021, 10, 8),
                          owner_email='user0@test.com')
        except ValueError:
            pass

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test creating a product with same name
        self.type("#name", "Product")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)
        # Get updated message
        msg = self.find_element('#message').text
        # Check to see if "Invalid" is in message
        assert("User already has product" in msg)

    # Blackbox method - Output Partitioning
    def test_product_creation(self, *_):
        """
        Test outputs from product creation. If product creation fails, user
        should be on the same page. Otherwise, if product creation is a
        success, user should be redirected to home page.
        """

        # Ensure the user is in the database, ignore errors from pre-existance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test product creation FAIL
        self.type("#name", " p0")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Wait for render to complete
        self.wait(0.5)

        # Verify elements exist (Still on same page)
        self.assert_element("#name")
        self.assert_element("#desc")
        self.assert_element("#price")
        self.assert_element("#btn-submit")

        # Test product creation PASS
        self.type("#name", "Product Pass")
        self.type("#desc", "This is a test description")
        self.type("#price", "10")
        self.click('input[type="submit"]')
        # Go to home page
        self.open(base_url)
        # Confirm at home page
        self.assert_element("#welcome-header")
        # Check if product was created
        self.assert_text("Product Pass", "#products")
