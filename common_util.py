import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import ConfigParser
import os
from Log import *

setting =  ConfigParser.ConfigParser()
setting.read('config.ini')
setting.sections()
log = Logger(object.__module__, DEBUG,"test.log")


class CommonUtil(object):
    """
    This class defines the common workflow method for openweathermap UI automation
    """

    @staticmethod
    def common_setup():
        """
        Test setup for standalone tests
        Performed following task:
        1. Launching Chrome browser
        2. Maximize browser
        3. Open openweathermap website

        :return:

        browser(object): selenium obejct.driver
        """
        dirpath = os.path.dirname(os.path.realpath(__file__))
        chromdriver = dirpath+ "/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromdriver
        driver = selenium.webdriver.Chrome(executable_path=chromdriver)
        driver.implicitly_wait(30)
        driver.maximize_window()
        driver.setting = ConfigParser.ConfigParser()
        driver.setting.read('config.ini')
        driver.setting.sections()
        url = driver.setting.get('url', 'Main_URL')
        driver.get(url)

        return driver


class PageUtil(object):

    def __init__(self, browser):
        self.browser = browser
        self.log = Logger(object.__module__, DEBUG, "test.log")

    def is_title_matches(self):
        """
        Workflow method to check title is matching or not
        :return:
        True if matches
        False
        """
        print self.browser.title
        return "OpenWeatherMap" in self.browser.title

    def click_on_submit_button(self):
        """
        Workflow method to click on submit button
        :param object:
        :return:
        """
        submit_button_locator = self.browser.setting.get('Locators', 'submit_button')
        submit_button = self.browser.find_element_by_xpath(submit_button_locator)
        assert self.is_element_present(By.XPATH,submit_button_locator), "Element is not present"
        submit_button.click()

    def enter_city_value(self, value):
        """
        Workflow method to enter value in text box
        :param object:
            Object
            Value(str) : city name
        :param value:
        :return:
        """
        text_box_locator = self.browser.setting.get('Locators', 'txt_box')
        txt_box = self.browser.find_element_by_xpath(text_box_locator)
        assert self.is_element_present(By.XPATH, text_box_locator), "Element is not present"
        txt_box.send_keys(value)

    def validate_correct_landing_page(self):
        """
        Workflow method to valudate landing page
        :param object:
        :return:
        """
        self.log.info("Validate logo whether landing on correct page")
        locator = self.browser.setting.get('Locators','logo')
        logo = self.browser.find_element_by_xpath(locator)
        assert logo.is_displayed(), "Logo in not enabled"
        self.log.info("Completed logo validation landing on correct page")

    def check_no_found_message_post_entered_invalid_city_name(self):
        """
        Workflow method to validate No message comes when entered Invalid city
        :param object:
        :return:
        """
        not_found_locator = self.browser.setting.get('Locators', 'not_found_msg')
        no_found_msg = self.browser.find_element_by_css_selector(not_found_locator).text
        message = unicode(no_found_msg)
        print message
        output = message.split("\n")[1]
        print output
        assert output == "Not found"," Error message is incorrect"
        close_locator = self.browser.setting.get('Locators', 'close')
        close = self.browser.find_element_by_css_selector(close_locator)
        close.click()
        assert not self.is_element_present(By.XPATH,close_locator), "Element is present "

    def validate_correct_city_temperature_displaying(self, expected_value):
        """
        Workflow method to validate correct city info/ temperature is displaying post entered valid city name
        :param object:
        :return:
        """
        not_found_locator = self.browser.setting.get('Locators', 'expected_city_name')
        actual_value = self.browser.find_element_by_xpath(not_found_locator)
        self.log.debug(actual_value.text)
        assert expected_value in actual_value.text, "Wrong result"

    def is_element_present(self,how,what):
        """
        Workflow method to check element is present or not
        :param object:
        :param how:
        :param what:
        :return:
        """
        try:
            self.browser.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def validate_all_labels(self):
        """
        Workflow method to validate all the label and elements on landing page
            1. Validating "We Deliver 2 Billion Forecasts Per Day" on home page
            2. Validating current location link
            3. Validating Your city text box
            4. Validating C and F temperature Button
            5. Validating Weather Tab link and its landing page
            6. Validating maps Tab link and its landing page
            7. Validating stations Tab link and its landing page
            8. Validating partners Tab link and its landing page
            9. Validating blogs Tab link and its landing page
            10. Validating API Tab link and its landing page
            11. Validating price Tab link and its landing page
            12. Validating Widgets Tab link and its landing page
            13. Validating sign in and sign up links
        :param object:
        :return:
        """
        self.log.debug("Validate Message on the home page")
        home_frame_msg_css = self.browser.setting.get('Locators', 'home_page_frame_msg')
        testing = self.browser.find_element_by_xpath(home_frame_msg_css).text
        assert testing == "We Deliver 2 Billion Forecasts Per Day" , "Home page message is not matching"

        self.log.debug("Validate current location link")
        current_location_link_css = self.browser.setting.get('Locators', 'current_location_link_css')
        location = self.browser.find_element_by_xpath(current_location_link_css)
        assert location.is_enabled(), "Current location link is not enabled"
        assert location.text == "Current location", "Current location has wrong label"

        self.log.debug("validate Your City text box")
        city_txt_box_css = self.browser.setting.get('Locators', 'city_text_box_css')
        txt_box = self.browser.find_element_by_xpath(city_txt_box_css)
        assert self.is_element_present(By.XPATH,city_txt_box_css), "City Text box is not present"
        placeholder = txt_box.get_attribute("placeholder")
        assert placeholder == "Your city name", "Text field label in not correct"

        self.log.debug( "validate C and F button")
        c_css = self.browser.setting.get('Locators', 'c_degree_css')
        f_css = self.browser.setting.get('Locators', 'f_degree_css')
        F = self.browser.find_element_by_xpath(c_css)
        C = self.browser.find_element_by_xpath(f_css)
        assert F.is_displayed(), "F is not displayed"
        assert C.is_displayed()," C is not displayed"

        self.log.debug( "Validate Weather link and its landing page")
        weather_link_css = self.browser.setting.get('Locators', 'weather_link')
        weather_link_expected_value = self.browser.setting.get('Input_Value', 'weather_link_expected_value')
        weather_landing_page_label_css = self.browser.setting.get('Locators', 'weather_landing_page_label')
        weather_landing_page_expected_value = self.browser.setting.get('Input_Value', 'Weather_landing_page_value')

        self.click_on_tabs(weather_link_css,tab_name=weather_link_expected_value)
        self.validate_landing_page_of_tabs(weather_landing_page_label_css,weather_landing_page_expected_value)

        self.log.debug( "Validate API link and its landing page")
        API_link_css = self.browser.setting.get('Locators', 'API_link')
        API_link_expected_value = self.browser.setting.get('Input_Value', 'API_link_expected_value')
        API_landing_page_label_css = self.browser.setting.get('Locators', 'API_landing_page_label')
        API_landing_page_expected_value = self.browser.setting.get('Input_Value', 'API_landing_page_value')

        self.click_on_tabs(API_link_css, API_link_expected_value)
        self.validate_landing_page_of_tabs(API_landing_page_label_css,
                                                  API_landing_page_expected_value)

        self.log.debug( "Validate price link and its  landing page")
        price_link_css = self.browser.setting.get('Locators', 'price_link')
        price_link_expected_value = self.browser.setting.get('Input_Value', 'price_link_expected_value')
        price_landing_page_label_css = self.browser.setting.get('Locators', 'price_landing_page_label')
        price_landing_page_expected_value = self.browser.setting.get('Input_Value', 'price_landing_page_value')

        self.click_on_tabs(price_link_css, price_link_expected_value)
        self.validate_landing_page_of_tabs(price_landing_page_label_css,
                                                  price_landing_page_expected_value)

        self.log.debug( "Validate partner link and its landing page")
        partner_link_css = self.browser.setting.get('Locators', 'partner_link')
        partner_link_expected_value = self.browser.setting.get('Input_Value', 'partner_link_expected_value')
        partner_landing_page_label_css = self.browser.setting.get('Locators', 'partner_landing_page_label')
        partner_landing_page_expected_value = self.browser.setting.get('Input_Value', 'partner_landing_page_value')

        self.click_on_tabs(partner_link_css, partner_link_expected_value)
        self.validate_landing_page_of_tabs(partner_landing_page_label_css,
                                                  partner_landing_page_expected_value)

        self.log.debug( "Validate station link and its landing page")
        station_link_css = self.browser.setting.get('Locators', 'station_link')
        station_link_expected_value = self.browser.setting.get('Input_Value', 'station_link_expected_value')
        station_landing_page_label_css = self.browser.setting.get('Locators', 'station_landing_page_label')
        station_landing_page_expected_value = self.browser.setting.get('Input_Value', 'station_landing_page_value')

        self.click_on_tabs( station_link_css, station_link_expected_value)
        self.validate_landing_page_of_tabs(station_landing_page_label_css,
                                                  station_landing_page_expected_value)

        self.log.debug( "Validate widget link and its landing page")
        widget_link_css = self.browser.setting.get('Locators', 'widget_link')
        widget_link_expected_value = self.browser.setting.get('Input_Value', 'widget_link_expected_value')
        widget_landing_page_label_css = self.browser.setting.get('Locators', 'widget_landing_page_label')
        widget_landing_page_expected_value = self.browser.setting.get('Input_Value', 'widget_landing_page_value')

        self.click_on_tabs( widget_link_css, widget_link_expected_value)
        self.validate_landing_page_of_tabs(widget_landing_page_label_css,
                                                  widget_landing_page_expected_value)

        self.log.debug( "Validate blogs and its landing page")
        blog_link_css = self.browser.setting.get('Locators', 'blog')
        print "Blogs"
        blogs = self.browser.find_element_by_css_selector(blog_link_css)
        blogs.click()
        assert blogs.is_enabled(), "Blog link is not enabled"
        before = self.browser.window_handles[0]
        blogs.click()
        after = self.browser.window_handles[1]
        self.browser.switch_to_window(after)
        blog_landing_page_value = self.browser.find_element_by_css_selector(".breadcrumb-title").text
        assert blog_landing_page_value=="Blogs", "Landing page is wrong"
        self.browser.switch_to_window(before)

        self.log.debug( "validate map dropdown and its landing page")
        All_map_css = self.browser.setting.get('Locators', 'All_maps')
        All_map_values = self.browser.self.driver.find_element_by_xpath(All_map_css)
        All_map_values.click()
        All_map_values = self.browser.setting.get('Locators', 'All_maps_dropdown')
        Map_values = self.driver.find_elements_by_css_selector(All_map_values)
        for value in Map_values:
            actual_text = value.text
            expected_result = ["Weather maps","current satelite maps", "Beautiful places"]
            if actual_text in expected_result:
                self.log.debug("Value is matching")

        self.log.debug( "Validate sign in and sig up buttons ")
        sign_in_css = self.browser.setting.get('Locators', 'sign_in_css')
        sign_up_css = self.browser.setting.get('Locators', 'sign_up_css')
        sign_in = self.browser.find_element_by_css_selector(sign_in_css)
        sign_up = self.browser.find_element_by_css_selector(sign_up_css)
        assert sign_in.is_displayed(), "Sign in is not displayed"
        assert sign_up.is_displayed(), "sign up is not displayed"

    def validate_landing_page_of_tabs(self, css, expected_output):
        """
        Workflow method to validate tabs on landing page
        :param object:
        :param css:
        :param expected_output:
        :return:
        """
        string = self.browser.find_element_by_css_selector(css).text
        self.log.debug( string)
        assert string in expected_output, " Label is not matching"

    def validate_sign_in_window_elements(self):
        """
        workflow method to validate the sign window elements
        :param object:
        :return:
        """
        link = self.browser.find_element_by_partial_link_text("Sign Up")
        link.click()
        self.log.debug("check email id field is present")
        sign_in_email_field = self.browser.setting.get('Locators', 'sign_in_email_field')
        assert self.is_element_present(By.XPATH, sign_in_email_field)," Email Field is not present"
        self.log.debug("check password field is present")
        sign_in_passwrd_field = self.browser.setting.get('Locators', 'sign_in_passwrd_field')
        assert self.is_element_present(By.XPATH, sign_in_passwrd_field), " Password Field is not present"
        self.log.debug("check Submit button field is present")
        sign_in_submit_button = self.browser.setting.get('Locators', 'sign_in_submit_button')
        assert self.is_element_present(By.XPATH, sign_in_submit_button), "Submit button is not present"

    def validate_sign_functionality(self,email, password):
        """
        Workflow method to validate sign functionality
        :param object:
        :return:
        """
        sign_in_email_field = self.browser.setting.get('Locators', 'sign_in_email_field')
        sign_in_passwrd_field = self.browser.setting.get('Locators', 'sign_in_passwrd_field')
        sign_in_submit_button =  self.browser.setting.get('Locators', 'sign_in_submit_button')
        self.browser.validate_sign_in_window_elements(object)
        self.log.debug("Enter value in email id field")
        self.browser.find_element_by_xpath(sign_in_email_field).send_keys(email)
        self.log.debug("Enter value in password field")
        self.browser.find_element_by_xpath(sign_in_passwrd_field).send_keys(password)
        self.log.debug("Click on Submit button")
        assert self.is_element_present(By.XPATH, sign_in_submit_button), " Button is not present"
        self.browser.find_element_by_xpath(sign_in_submit_button).click()

    def validate_alert_message_if_entered_wrong_email_password(self):
        """
        Workflow method to validate alert message upon entering invalid email and password
        :param object:
        """
        alert = self.browser.setting.get('Locators', 'alert')
        self.log.debug("Verify Alert label")
        alert_text = self.browser.find_element_by_xpath(alert).text
        assert alert_text=="Alert", "Alert is not displayed"
        self.log.debug("Verify Invalid Email or password message")
        invalid_email_passwrd_msg = self.browser.setting.get('Locators', 'invalid_email_passwrd_msg')
        invalid_msg = self.browser\
            .find_element_by_xpath(invalid_email_passwrd_msg).text
        assert invalid_msg=="Invalid Email or password.", "Message is wrong"

    def click_on_tabs(self, css, tab_name):
        """
        Workflow method to click on each tab and validate tab labels
        :param object:
        :param css:
        :param tab_name:
        :return:
        """
        tab = self.browser.find_element_by_css_selector(css)
        self.log.debug( tab.text)
        assert tab.text==tab_name
        tab.is_displayed()
        tab.click()

    def click_on_sign_up_link(self):
        """
        Workflow method to click on sign_up link
        :return:
        """
        create_new_acc_txt = self.browser.setting.get('Locators', 'create_new_acc_txt')
        self.log.debug("Click on Sign up link")
        link  = self.browser.find_element_by_partial_link_text("Sign Up")
        link.click()
        self.log.debug("Validate Create New Accont text on sign up page")
        create_acc = self.browser.find_element_by_css_selector(create_new_acc_txt)
        create_acc_text = create_acc.text
        self.log.debug(create_acc_text)
        assert create_acc_text == "Create New Account" , "It is not a sign up window"

    def enter_value_in_txt_field(self, value, placehoder, locator):
        """

        :param value:
        :param kwargs:
        :return:
        """
        field_locator = self.browser.find_element_by_css_selector(locator)
        self._validate_place_holder_txt_field(placehoder, field_locator)
        field_locator.send_keys(value)

    def _validate_place_holder_txt_field(self, placehoder_expected, field_locator):
        placeholder_actual = field_locator.get_attribute("placeholder")
        assert placeholder_actual == placehoder_expected , "Wrong username placeholder"

    def click_on_link(self, link, landing_page):
        """
        Workflow method to click on Link
        :return:
        """
        privacy = self.browser.find_element_by_partial_link_text(link)
        assert  privacy.is_enabled(), "Privacy is enabled"
        before = self.browser.window_handles[0]
        privacy.click()
        after = self.browser.window_handles[1]
        self.browser.switch_to_window(after)
        print self.browser.current_url
        privacy_new_page_title = self.browser.find_element_by_css_selector(landing_page)
        assert privacy_new_page_title.text=="Privacy Policy", " title is mismatch"
        self.browser.close()
        self.browser.switch_to_window(before)

    def select_checkbox(self, locator):
        """
        workflow method to select checkboxes
        :return:
        """
        checkbox = self.browser.find_element_by_css_selector(locator)
        if not checkbox.is_selected():
            checkbox.click()
        else:
            print " check box is already selected"

    def click_create_account_button(self):
        """
        Workflow method to create new account
        :return:
        """
        create_account_button = self.browser.setting.get('Locators', 'create_account_button')
        button = self.browser.find_element_by_css_selector(create_account_button)
        assert button.is_enabled(), "button is enabled"
        if button.is_enabled():
            button.click()