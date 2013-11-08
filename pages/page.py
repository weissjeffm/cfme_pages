#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittestzero import Assert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plugin.pytest_selenium import sel


def is_the_current_page(pg):
    Assert.true(isinstance(pg, Page) and pg.title is not None)
    return sel().title == pg.title
    

class Page(object):
    '''
    Base class for all Pages
    '''
    def __getattr__(self, name):
        return self.locators[name]

    def __init__(self, locators={}, title=None, is_the_current_page=is_the_current_page):
        self.locators = locators
        self.title = title
        self.is_the_current_page = is_the_current_page


def get_url_current_page():
    return sel().current_url


def get_context_current_page():
    url = get_url_current_page()
    stripped = url.lstrip('https://')
    return stripped[stripped.find('/'):stripped.rfind('?')]


def handle_popup(cancel=False):
    wait = WebDriverWait(sel(), 30.0)
    # throws timeout exception if not found
    wait.until(EC.alert_is_present())
    popup = sel().switch_to_alert()
    answer = 'cancel' if cancel else 'ok'
    print popup.text + " ...clicking " + answer
    popup.dismiss() if cancel else popup.accept()
