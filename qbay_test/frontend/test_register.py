from seleniumbase import BaseCase
from qbay_test.conftest import base_url


class register_test(BaseCase):

    # Blackbox method - Functional Requirements
    def test_functional(self, *_):
        # Open the register page
        self.open(base_url + '/user/register')
        # Input a correct set of registration information
        self.type("#email", "validemail@gmail.com")
        self.type("#name", "Damien Smith")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        # Submit the information
        self.click('input[type="submit"]')

        # Open the login page
        self.open(base_url + "/user/login")
        # Input the correct email and password
        self.type("#email", "validemail@gmail.com")
        self.type("#password", "ValidPassword123!")
        # Submit the information
        self.click('input[type="submit"]')

        # If the home page is able to load - this means that the login
        # was successful and therefore the functional requirements of
        # the registration page pass
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Damien Smith!", "#welcome-header")
        shipping = self.find_element('#shipping').text
        # Check to see if "Invalid" is in message
        assert("Shipping address:" in shipping)
        postal = self.find_element('#postal').text
        # Check to see if "Invalid" is in message
        assert("Postal Code:" in postal)
        balance = self.find_element('#balance').text
        # Check to see if "Invalid" is in message
        assert("Balance = 100" in balance)
        #  self.assert_text("Shipping address: 2313", "#shipping")
        # self.assert_text("Postal Code: dasd1", "#postal")
        # self.assert_text("Balance = 99", "#balance")

    # Blackbox method - input partioning
    def test_username(self, *_):
        # Testing invalid username - no special characters allowed
        self.open(base_url + '/user/register')
        self.type("#email", "valid@gmail.com")
        self.type("#name", "Damien!@#")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid username." in msg)

        # Testing invalid username - whitespace in prefix
        self.open(base_url + '/user/register')
        self.type("#email", "valid1@gmail.com")
        self.type("#name", " bob")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid username." in msg)

        # Testing invalid username - whitespace in suffix
        self.open(base_url + '/user/register')
        self.type("#email", "valid2@gmail.com")
        self.type("#name", "bob ")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid username." in msg)

        # Testing invalid username - insufficient number of characters
        self.open(base_url + '/user/register')
        self.type("#email", "valid3@gmail.com")
        self.type("#name", "TI")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid username." in msg)

        # Testing invalid username - username too long (characters)
        self.open(base_url + '/user/register')
        self.type("#email", "valid4@gmail.com")
        self.type("#name", "asdkjlsdksjdkajskjdaksjdksjskskdj")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid username." in msg)

        # Testing invalid username - empty username
        self.open(base_url + '/user/register')
        self.type("#email", "valid5@gmail.com")
        self.type("#name", "")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        # Check if still on the same page
        self.wait(0.5)
        self.assert_element("#email")
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")

    def test_email(self, *_):
        # Testing valid email - no double @ allowed
        self.open(base_url + '/user/register')
        self.type("#email", "invalid@email@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid email or already in use." in msg)

        # Testing valid email - no duplicate emails allowed
        self.open(base_url + '/user/register')
        self.type("#email", "test123@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')
        self.open(base_url + '/user/register')
        self.type("#email", "test123@gmail.com")
        self.type("#name", "DamienS")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid email or already in use." in msg)

        # Testing invalid email - empty email input
        self.open(base_url + '/user/register')
        self.type("#email", "")
        self.type("#name", "random")
        self.type("#password", "ValidPassword123!")
        self.type("#password2", "ValidPassword123!")
        self.click('input[type="submit"]')

        # Check if still on the same page
        self.wait(0.5)
        self.assert_element("#email")
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")

    def test_password(self, *_):
        # Testing valid password - requires at least 1 special character
        self.open(base_url + '/user/register')
        self.type("#email", "validemail1@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "Invalidpassword")
        self.type("#password2", "Invalidpassword")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid password." in msg)

        # Testing valid password - requires at least 1 uppercase
        self.open(base_url + '/user/register')
        self.type("#email", "validemail1@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "invalidpassword1!")
        self.type("#password2", "invalidpassword1!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid password." in msg)

        # Testing valid password - requires at least 1 lowercase
        self.open(base_url + '/user/register')
        self.type("#email", "validemail2@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "INVALIDPASSWORD1!")
        self.type("#password2", "INVALIDPASSWORD1!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid password." in msg)

        # Testing valid password - not enough characters
        self.open(base_url + '/user/register')
        self.type("#email", "validemail2@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "Tet1!")
        self.type("#password2", "Tet1!")
        self.click('input[type="submit"]')

        msg = self.find_element('#message').text
        assert("Registration Failed. Invalid password." in msg)

        # Testing valid password - empty password
        self.open(base_url + '/user/register')
        self.type("#email", "validemail3@gmail.com")
        self.type("#name", "Damien")
        self.type("#password", "")
        self.type("#password2", "")
        self.click('input[type="submit"]')

        # Check if still on the same page
        self.wait(0.5)
        self.assert_element("#email")
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")

    # Blackbox method - output partioning
    def test_registration(self, *_):

        # Test registration FAIL
        self.open(base_url + "/user/register")
        self.type("#email", "randomEmail@gmail.com")
        self.type("#name", "John")
        self.type("#password", "InvalidPassword")
        self.type("#password2", "InvalidPassword")
        self.click('input[type="submit"]')

        # Check if still on the same page
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

        # Check if on the login page
        self.wait(0.5)
        self.assert_text("Please login", "#message")
