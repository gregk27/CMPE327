from seleniumbase import BaseCase

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

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test space in prefix in product name
        self.type(" p0", "#name")
        self.type("This is a test description", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test space in suffix in product name
        self.type("p0 ", "#name")
        self.type("This is a test description", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test special character in product name
        self.type("p@", "#name")
        self.type("This is a test description", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test length of product name (Cannot be >80)
        self.type("a"*81, "#name")
        self.type("This is a test description", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test correct product name input
        # Valid product name, length 80 chars
        # Description longer than title
        # Success will redirect to home page
        self.type("p1"*40, "#name")
        self.type("This is a test description"*4, "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("p1"*40, "#products")

    def test_description(self, *_):
        """
        Test various inputs for product description.
        """

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test description length < 20
        self.type("p0", "#name")
        self.type("a"*19, "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test description length > 2000
        self.type("p0", "#name")
        self.type("a"*2001, "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test description length <= title length
        self.type("p0", "#name")
        self.type("aa", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test correct production description input
        # Success will redirect to home page
        self.type("p1", "#name")
        self.type("abcdefghijklmnopqrstuvwxyz" +
                  "0123456789!@#$%^&*()./?<>[]|{}\\", "#desc")
        self.type("10", "#price")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("abcdefghijklmnopqrstuvwxyz" +
                         "0123456789!@#$%^&*()./?<>[]|{}\\", "#products")

    def test_price(self, *_):
        """
        Test various inputs for product price.
        """

        # Open product creation page
        self.open(base_url + '/product/create')

        # Test price < 10
        self.type("p0", "#name")
        self.type("This is a test description", "#desc")
        self.type("9.99", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test price > 10000
        self.type("p0", "#name")
        self.type("This is a test description", "#desc")
        self.type("10000.01", "#price")
        self.click('input[type="submit"]')
        self.assert_text("Unknown error occurred", '#message')

        # Test correct price input
        # Success will redirect to home page
        self.type("p2", "#name")
        self.type("This is a test description", "#desc")
        self.type("100", "#price")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("100.0", "#products")

    # Blackbox method - Output Partitioning
    def test_message(self, *_):
        """
        Test all outputs by checking resulting message.
        """

        # Open product creation page
        self.open(base_url + '/product/create')
