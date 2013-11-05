#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from base import Base
from page import Page

class LoginPage(Base):
    # TODO: This obviously should change. File bug
    title = "CloudForms Management Engine: Dashboard"
    locators = {"login_username_field": (By.CSS_SELECTOR, '#user_name'),
                "login_password_field": (By.CSS_SELECTOR, '#user_password'),
                "login_submit_button": (By.ID, 'login')}

    # Demo locators
    #title = u"Mozilla \u2014 Home of the Mozilla Project \u2014 mozilla.org"
    #_header_locator = (By.CSS_SELECTOR, 'h1')

    @property
    def is_the_current_page(self):
        '''Override the base implementation to make sure that we are actually on the login screen
        and not the actual dashboard
        '''
        return Base.is_the_current_page and self.is_element_visible(*self._login_submit_button_locator)

    def _click_on_login_and_send_window_size(self):
        self.login_button.click()
        driver = self.login_button.parent
        driver.execute_script("""miqResetSizeTimer();""")

    def login(self, user='default'):
        return self.login_with_mouse_click(user)

    def login_with_enter_key(self, user='default'):
        return self.__do_login(self._press_enter_on_login_button, user)

    def login_with_mouse_click(self, user='default'):
        return self.__do_login(self._click_on_login_button, user)

    def login_and_send_window_size(self, user='default'):
        return self.__do_login(self._click_on_login_and_send_window_size, user)

    def __do_login(self, continue_function, user='default'):
        self.__set_login_fields(user)
        # TODO: Remove once bug is fixed
        time.sleep(1.25)
        continue_function()
        try:
            self._wait_for_results_refresh()
        except:
            self._wait_for_results_refresh()
        from pages.dashboard import DashboardPage
        return DashboardPage(self.testsetup)

    def __set_login_fields(self, user='default'):
        credentials = self.testsetup.credentials[user]
        self.username.send_keys(credentials['username'])
        self.password.send_keys(credentials['password'])

    def _press_enter_on_login_button(self):
        self.login_button.send_keys(Keys.RETURN)

    def login(self, user, password, method=lambda self=self: sel().click(self,"login_submit_button")):
        pass
