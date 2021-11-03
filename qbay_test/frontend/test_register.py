from seleniumbase import BaseCase
from qbay_test.conftest import base_url


class register_test(BaseCase):

    # Blackbox method - Functional Requirements
    def test_func(self, *_):
        self.open(base_url + '/user/register')
        self.type("#email", "validemail@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        self.open(base_url + "/user/login")
        self.type("#email", "validemail@gmail.com")
        self.type("#password", "ValidPassword123!")
        self.click('input[type="submit"]')

        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Damien!", "#welcome-header")

    '''
    # Blackbox method - input partioning
    def test_username(self, *_):
        self.open(base_url + 'user/register')
        self.type()
        self.type()
        self.type()

    def test_email(self, *_):
        self.open(base_url, 'user/register')
        self.type()
        self.type()
        self.type()
        self.type()

    def test_password(self, *_):
        self.open(base_url, 'user/register')
        self.type()
        self.type()
        self.type()

    '''

    # Blackbox method - output partioning
    def test_registration(self, *_):

        # Test registration FAIL
        self.open(base_url + "/user/register")
        self.type("#email", "randomEmail@gmail.com")
        self.type("#name", "John")
        self.type("#password", "InvalidPassword")
        self.type("#password2", "InvalidPassword")
        self.click('input[type="submit"]')
        self.wait(0.5)

        self.assert_element("#email")
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")

        # Test registration SUCCESS
        self.open(base_url + "/user/register")
        self.type("#email", "testing123@gmail.com")
        self.type("#name", "Bruce")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')
        self.wait(0.5)

        self.assert_element("#email")
        self.assert_element("#password")
