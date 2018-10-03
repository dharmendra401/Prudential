#Author: dharmendra Pandey [dharmendra401@yahoo.in]

import  unittest

from selenium.webdriver.common.by import By

from common_util import CommonUtil, PageUtil
from Log import *
import ConfigParser

setting =  ConfigParser.ConfigParser()
setting.read('config.ini')
setting.sections()

class SearchTest(unittest.TestCase):

    """
    Tests for the openweathermap UI
    """

    @classmethod
    def setUp(self):
        # """
        # setup for home page
        # :return: None
        # """
        self.log = Logger(self.__module__, DEBUG,"test.log")
        self.log.debug("-------Starting test Setup------")
        self.driver = CommonUtil.common_setup()
        self.page = PageUtil(self.driver)
        self.page.is_title_matches()
        self.log.debug("------Completed Test setup-------")

    def test_invalid_city_weather(self):
        """
        Verify if enter invalid city in text box field
        Step:
            1. Validate landing page is correct
            2. Enter invalid city in the text box
            3. Click on submit button
            4. Check No found message appears and validate the same
            5. Click on X icon on the No found message frame
        """
        self.log.debug("Started test_invalid_city_weather Test ")
        self.page.validate_correct_landing_page()

        self.log.info("Enter Invalid value in text field")
        invalid_input = setting.get('Input_Value', 'Invalid_value')
        self.page.enter_city_value(invalid_input)

        self.log.info("Click on Submit button")
        self.page.click_on_submit_button()

        self.log.info("Check No found message appears and click on Close icon")
        self.page.check_no_found_message_post_entered_invalid_city_name()
        self.log.debug("Completed test_invalid_city_weather test")

    def test_valid_city_verify_weather_details(self):
        """
        Verify if enter valid city namein text box field
        Step:
            1. Validate landing page is correct
            2. Enter valid city name in the text box
            3. Click on submit button
            4. Check correct city temperature is displaying or not
               Here validating "City name" link. city_name_link should be equal
               to city name which we have entered

        """
        self.log.debug("Started test_invalid_city_weather Test ")
        self.page.validate_correct_landing_page()

        self.log.info("Enter valid value in text field")
        valid_input = setting.get('Input_Value', 'Valid_value')
        self.page.enter_city_value(valid_input)

        self.log.info("Click on Submit button")
        self.page.click_on_submit_button()

        self.log.info("Check correct city temperature is displaying")
        self.page.validate_correct_city_temperature_displaying(valid_input)

    def test_validate_landing_page(self):
        """
        Verify elements of openweather landing page
        Step:
            1. Validating all the tabs:
                weather
                maps
                API
                price
                partners
                stations
                widget
                blogs
            2. validating Current location link
            3. validating sign in and sign up links
            4. Validating C and F temperature buttons
            5. Validating Your city name text box
            6. Validating Search button
            7. Validating "We Deliver 2 Billion Forecasts Per Day" message on the home page
        """
        self.log.debug("Started test_valid_city_weather Test ")
        self.page.validate_correct_landing_page()

        self.log.debug("Checking all elements of home page")
        self.page.validate_all_labels()


    def test_sign_in_functionality_invalid_email_password(self):
        """
        This test will validate sign in functionality
        1.Validate email and password field is present
        2.enter invalid email  in email id field
        3.enter invalid password in password field
        4.Click on submit button
        5.Verify "Invalid Email or password" message
        :return:
        """
        self.log.debug("Validate email and password fields are present")
        self.page.validate_sign_in_window_elements()
        email = "abc@gmail.com" #Invalid email id
        password = "123456" #Invalid password
        self.log.debug("enter invalid email and password")
        self.page.validate_sign_functionality(email, password)
        self.log.debug("Verify alert 'Invalid Email or password.' messsage ")
        self.page.validate_alert_message_if_entered_wrong_email_password()


    @classmethod
    def tearDown(self):
        """
        Teardown to close chrome browser
        :return:
        """
        self.log.debug("Started TearDown")
        self.driver.quit()
        self.log.debug("Completed TearDown")



