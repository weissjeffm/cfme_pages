#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from plugin.pytest_selenium import sel
import pages.page as pg
from pages.region import add_locators


def is_the_current_page(page):
    return pg.is_the_current_page() and sel().is_displayed(page.login_submit_button)


title = "CloudForms Management Engine: Dashboard"
locators = {"username_text": (By.CSS_SELECTOR, '#user_name'),
            "password_text": (By.CSS_SELECTOR, '#user_password'),
            "submit_button": (By.ID, 'login')}
for k, v in locators.items():
    globals()[k] = v

add_locators(locators)


def _click_on_login():
    sel().click(login_button)


def _press_enter_on_login_button(self):
    self.login_button.send_keys(Keys.RETURN)


def login(user, password, submit_method=_click_on_login):
    sel().send_keys(username_text, user)
    sel().send_keys(password_text, password)
    submit_method()
