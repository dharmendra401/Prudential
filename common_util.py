import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import ConfigParser
import os
from Log import *


setting =  ConfigParser.ConfigParser()
setting.read('config.ini')
setting.sections()
object.log = Logger(object.__module__, DEBUG,"test.log")


class Common_util(object):
    """
    This class defines the common workflow method for openweathermap UI automation
    """

    @staticmethod
    def common_setup(object):
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
        object.driver = selenium.webdriver.Chrome(executable_path=chromdriver)
        object.driver.implicitly_wait(30)
        object.driver.maximize_window()
        object.driver.setting = ConfigParser.ConfigParser()
        object.driver.setting.read('setting.ini')
        object.driver.setting.sections()
        url = object.driver.setting.get('url', 'Main_URL')
        object.driver.get(url)

        return object.driver

    @staticmethod
    def is_title_matches(object):
        """
        Workflow method to check title is matching or not
        :return:
        True if matches
        False
        """
        print object.driver.title
        return "OpenWeatherMap" in object.driver.title

    @staticmethod
    def click_on_submit_button(object):
        """
        Workflow method to click on submit button
        :param object:
        :return:
        """
        submit_button_locator = object.driver.setting.get('Locators', 'submit_button')
        submit_button = object.driver.find_element_by_xpath(submit_button_locator)
        WebDriverWait(object.driver, 10).until(EC.presence_of_element_located(By.XPATH, submit_button))
        object.driver.submit_button.click()

    @staticmethod
    def enter_city_value(object, value):
        """
        Workflow method to enter value in text box
        :param object:
            Object
            Value(str) : city name
        :param value:
        :return:
        """
        text_box_locator = object.driver.setting.get('Locators', 'txt_box')
        txt_box = object.driver.find_element_by_xpath(text_box_locator)
        WebDriverWait(object.driver, 10).until(EC.presence_of_element_located(By.XPATH, txt_box))
        txt_box.send_keys(value)

    @staticmethod
    def validate_correct_landing_page(object):
        """
        Workflow method to valudate landing page
        :param object:
        :return:
        """
        object.log.info("Validate logo whether landing on correct page")
        locator = object.driver.setting.get('Locators','logo')
        logo = object.driver.find_element_by_xpath(locator)
        assert logo.is_displayed(), "Logo in not enabled"
        object.log.info("Completed logo validation landing on correct page")


    @staticmethod
    def check_no_found_message_post_entered_invalid_city_name(object):
        """
        Workflow method to validate No message comes when entered Invalid city
        :param object:
        :return:
        """
        not_found_locator = object.driver.setting.get('Locators', 'not_found_msg')
        no_found_msg = object.driver.find_element_by_css_selector(not_found_locator).text
        message = unicode(no_found_msg)
        object.log.debug(message)
        output = message.split("\n")[1]
        assert output == "Not found"," Error message is incorrect"
        close_locator = object.driver.setting.get('Locators', 'close')
        close = object.driver.find_element_by_css_selector(close_locator)
        close.click()
        WebDriverWait(object.driver, 10).until(EC.invisibility_of_element(By.CSS_SELECTOR, close))

    @staticmethod
    def validate_correct_city_temperature_displaying(object):
        """
        Workflow method to validate correct city info/ temperature is displaying post entered valid city name
        :param object:
        :return:
        """
        not_found_locator = object.driver.setting.get('Locators', 'expected_city_name')
        actual_value = object.driver.find_element_by_xpath(not_found_locator)
        object.log.debug(actual_value.text)
        assert object.valid_input in actual_value.text, "Wrong result"


    @staticmethod
    def is_element_present(object,how,what):
        """
        Workflow method to check element is present or not
        :param object:
        :param how:
        :param what:
        :return:
        """
        try:
            object.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True


    @staticmethod
    def validate_all_labels(object):
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
        object.log.debug("Validate Message on the home page")
        home_frame_msg_css = object.driver.setting.get('Locators', 'home_page_frame_msg')
        testing = object.driver.find_element_by_xpath(home_frame_msg_css).text
        assert testing == "We Deliver 2 Billion Forecasts Per Day" , "Home page message is not matching"

        object.log.debug("Validate current location link")
        current_location_link_css = object.driver.setting.get('Locators', 'current_location_link_css')
        location = object.driver.find_element_by_xpath(current_location_link_css)
        assert location.is_enabled(), "Current location link is not enabled"
        assert location.text == "Current location", "Current location has wrong label"

        object.log.debug("validate Your City text box")
        city_txt_box_css = object.driver.setting.get('Locators', 'city_text_box_css')
        txt_box = object.driver.find_element_by_xpath(city_txt_box_css)
        assert txt_box.is_enabled(), " Text box is enabled"
        placeholder = txt_box.get_attribute("placeholder")
        assert placeholder == "Your city name", "Text field label in not correct"

        object.log.debug( "validate C and F button")
        c_css = object.driver.setting.get('Locators', 'c_degree_css')
        f_css = object.driver.setting.get('Locators', 'f_degree_css')
        F = object.driver.find_element_by_xpath(c_css)
        C = object.driver.find_element_by_xpath(f_css)
        assert F.is_displayed(), "F is not displayed"
        assert C.is_displayed()," C is not displayed"

        object.log.debug( "Validate Weather link and its landing page")
        weather_link_css = object.driver.setting.get('Locators', 'weather_link')
        weather_link_expected_value = object.driver.setting.get('Input_Value', 'weather_link_expected_value')
        weather_landing_page_label_css = object.driver.setting.get('Locators', 'weather_landing_page_label')
        weather_landing_page_expected_value = object.driver.setting.get('Input_Value', 'Weather_landing_page_value')

        Common_util.click_on_tabs(object.driver,weather_link_css,weather_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver, weather_landing_page_label_css,weather_landing_page_expected_value)

        object.log.debug( "Validate API link and its landing page")
        API_link_css = object.driver.setting.get('Locators', 'API_link')
        API_link_expected_value = object.driver.setting.get('Input_Value', 'API_link_expected_value')
        API_landing_page_label_css = object.driver.setting.get('Locators', 'API_landing_page_label')
        API_landing_page_expected_value = object.driver.setting.get('Input_Value', 'API_landing_page_value')

        Common_util.click_on_tabs(object.driver, API_link_css, API_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver, API_landing_page_label_css,
                                                  API_landing_page_expected_value)

        object.log.debug( "Validate price link and its  landing page")
        price_link_css = object.driver.setting.get('Locators', 'price_link')
        price_link_expected_value = object.driver.setting.get('Input_Value', 'price_link_expected_value')
        price_landing_page_label_css = object.driver.setting.get('Locators', 'price_landing_page_label')
        price_landing_page_expected_value = object.driver.setting.get('Input_Value', 'price_landing_page_value')

        Common_util.click_on_tabs(object.driver, price_link_css, price_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver, price_landing_page_label_css,
                                                  price_landing_page_expected_value)

        object.log.debug( "Validate partner link and its landing page")
        partner_link_css = object.driver.setting.get('Locators', 'partner_link')
        partner_link_expected_value = object.driver.setting.get('Input_Value', 'partner_link_expected_value')
        partner_landing_page_label_css = object.driver.setting.get('Locators', 'partner_landing_page_label')
        partner_landing_page_expected_value = object.driver.setting.get('Input_Value', 'partner_landing_page_value')

        Common_util.click_on_tabs(object.driver, partner_link_css, partner_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver, partner_landing_page_label_css,
                                                  partner_landing_page_expected_value)

        object.log.debug( "Validate station link and its landing page")
        station_link_css = object.driver.setting.get('Locators', 'station_link')
        station_link_expected_value = object.driver.setting.get('Input_Value', 'station_link_expected_value')
        station_landing_page_label_css = object.driver.setting.get('Locators', 'station_landing_page_label')
        station_landing_page_expected_value = object.driver.setting.get('Input_Value', 'station_landing_page_value')

        Common_util.click_on_tabs(object.driver, station_link_css, station_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver,station_landing_page_label_css,
                                                  station_landing_page_expected_value)

        object.log.debug( "Validate widget link and its landing page")
        widget_link_css = object.driver.setting.get('Locators', 'widget_link')
        widget_link_expected_value = object.driver.setting.get('Input_Value', 'widget_link_expected_value')
        widget_landing_page_label_css = object.driver.setting.get('Locators', 'widget_landing_page_label')
        widget_landing_page_expected_value = object.driver.setting.get('Input_Value', 'widget_landing_page_value')

        Common_util.click_on_tabs(object.driver, widget_link_css, widget_link_expected_value)
        Common_util.validate_landing_page_of_tabs(object.driver,widget_landing_page_label_css,
                                                  widget_landing_page_expected_value)

        object.log.debug( "Validate blogs and its landing page")
        blog_link_css = object.driver.setting.get('Locators', 'blog')
        print "Blogs"
        blogs = object.driver.find_element_by_css_selector(blog_link_css)
        blogs.click()
        assert blogs.is_enabled(), "Blog link is not enabled"
        before = object.driver.window_handles[0]
        blogs.click()
        after = object.driver.window_handles[1]
        object.driver.switch_to_window(after)
        blog_landing_page_value = object.driver.find_element_by_css_selector(".breadcrumb-title").text
        assert blog_landing_page_value=="Blogs", "Landing page is wrong"
        object.driver.switch_to_window(before)

        object.log.debug( "validate map dropdown and its landing page")
        All_map_css = object.driver.setting.get('Locators', 'All_maps')
        All_map_values = object.driver.find_element_by_css_selector(All_map_css)
        All_map_values.click()
        select = object.Select(All_map_values)
        object.log.debug( [oo.text for oo in select.options])
        expected_result = ["Weather maps","current satelite maps", "Beautiful places"]
        if oo.text in expected_result:
            object.log.debug( "All values are matched")

        object.log.debug( "Validate sign in and sig up buttons ")
        sign_in_css = object.driver.setting.get('Locators', 'sign_in_css')
        sign_up_css = object.driver.setting.get('Locators', 'sign_up_css')
        sign_in = object.driver.find_element_by_css_selector(sign_in_css)
        sign_up = object.driver.find_element_by_css_selector(sign_up_css)
        assert sign_in.is_displayed(), "Sign in is not displayed"
        assert sign_up.is_displayed(), "sign up is not displayed"

    @staticmethod
    def validate_landing_page_of_tabs(object, css,expected_output):
        """
        Workflow method to validate tabs on landing page
        :param object:
        :param css:
        :param expected_output:
        :return:
        """
        string = object.find_element_by_css_selector(css).text
        object.log.debug( string)
        assert string in expected_output, " Label is not matching"


    @staticmethod
    def validate_sign_in_window_elements(object):
        """
        workflow method to validate the sign window elements
        :param object:
        :return:
        """
        sign_in = object.driver.setting.get('Locators', 'sign_in_css')
        object.driver.find_element_by_css_selector(sign_in).click
        object.log.debug("check email id field is present")
        object.driver.sign_in_email_field = object.driver.setting.get('Locators', 'sign_in_email_field')
        Common_util.is_element_present(By.XPATH, object.driver.sign_in_email_field)
        object.log.debug("check password field is present")
        object.driver.sign_in_passwrd_field = object.driver.setting.get('Locators', 'sign_in_passwrd_field')
        Common_util.is_element_present(By.XPATH, object.driver.sign_in_passwrd_field)
        object.log.debug("check Submit button field is present")
        object.driver.sign_in_submit_button = object.driver.setting.get('Locators', 'sign_in_submit_button')
        Common_util.is_element_present(By.XPATH, object.driver.sign_in_submit_button)


    @staticmethod
    def validate_sign_functionality(object,email, password):
        """
        Workflow method to validate sign functionality
        :param object:
        :return:
        """
        Common_util.validate_sign_in_window_elements(object)
        object.log.debug("Enter value in email id field")
        object.driver.find_element_by_xpath(object.driver.sign_in_email_field).send_keys(email)
        object.log.debug("Enter value in password field")
        object.driver.find_element_by_xpath(object.driver.sign_in_passwrd_field).send_keys(password)
        WebDriverWait(object.driver, 10).until(EC.presence_of_element_located(By.XPATH, object.driver.sign_in_submit_button))
        object.log.debug("Click on Submit button")
        WebDriverWait(object.driver, 10).until(
            EC.element_to_be_clickable(By.XPATH, object.driver.sign_in_submit_button))
        object.driver.find_element_by_xpath(object.driver.sign_in_submit_button).click()



    @staticmethod
    def validate_invalid_alert_if_entered_wrong_email_password(object):
        """
        Workflow method to validate alert message upon entering invalid email and password
        :param object:
        """
        alert = object.driver.setting.get('Locators', 'alert')
        object.log.debug("Verify Alert label")
        alert_text = object.driver.find_element_by_xpath(alert).text
        assert alert_text=="Alert", "Alert is not displayed"
        object.log.debug("Verify Invalid Email or password message")
        invalid_email_passwrd_msg = object.driver.setting.get('Locators', 'invalid_email_passwrd_msg')
        invalid_msg = object.driver.find_element_by_xpath(invalid_email_passwrd_msg).text
        assert invalid_msg=="Invalid Email or password.", "Message is wrong"


    @staticmethod
    def click_on_tabs(object,css,tab_name):
        """
        Workflow method to click on each tab and validate tab labels
        :param object:
        :param css:
        :param tab_name:
        :return:
        """
        tab = object.find_element_by_css_selector(css)
        object.log.debug( tab.text)
        assert tab.text==tab_name
        tab.is_displayed()
        tab.click()









