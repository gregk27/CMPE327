from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from qbay.backend import register

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):

    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        This is a functional test as it validates that th user can be logged in
        """
        # Ensure the user is in the database, ignore errors from preexistance
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

        # after clicking on the browser (the line above)
        # the front-end code is activated
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value.

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test User!", "#welcome-header")
        # other available APIs

    def test_login(self, *_):
        """
        Test that the login fails on bad credentials
        It contains both input and output testing methods
        """
        # Ensure the user is in the database, ignore errors from preexistance
        try:
            register("Test User", "user@test.com", "ValidPass1!")
        except ValueError:
            pass

        """
        Input partitioning:
         - Bad email, bad password
         - Good email, bad password
         - Bad email, good password
         - Good email, good password
        """

        # Bad email, bad password partition
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user2@test.com")
        self.type("#password", "BadPassword1!")
        # click enter button
        self.click('input[type="submit"]')

        # test that it's still on the login page
        self.assert_text("Log In", "h1")

        # Bad email, bad password partition
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "BadPassword1!")
        # click enter button
        self.click('input[type="submit"]')

        # test that it's still on the login page
        self.assert_text("Log In", "h1")

        # Bad email, bad password partition
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user2@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # test that it's still on the login page
        self.assert_text("Log In", "h1")

        # Bad email, bad password partition
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test User!", "#welcome-header")

        """
        Output partitioning
         - displays error
         - redirects to homepage
        """
        # displays error
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user2@test.com")
        self.type("#password", "BadPassword1!")
        # click enter button
        self.click('input[type="submit"]')

        # test that the login error is displayed
        self.assert_text("Incorrect email or password", "#message")

        # redirects to homepage
        # open login page
        self.open(base_url + '/user/login')
        # fill email and password
        self.type("#email", "user@test.com")
        self.type("#password", "ValidPass1!")
        # click enter button
        self.click('input[type="submit"]')

        # test if it's on the homepage
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test User!", "#welcome-header")
