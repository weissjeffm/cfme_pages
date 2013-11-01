import pytest
import threading
from selenium import webdriver
from contextlib import contextmanager

thread_locals = threading.local()

def sel():
    return thread_locals.selenium


@contextmanager
def selenium_session(cls, *args, **kwargs):
    sel = cls(*args, **kwargs)
    thread_locals.selenium = sel
    sel.maximize_window()
    yield sel
    sel.quit()

@pytest.yield_fixture
def selenium():
    with selenium_session(webdriver.Firefox) as sel:
        yield sel

options = [['--highlight', {"action":'store_true', 
                            "dest":'highlight',
                            "default":False,
                            "help":'whether to turn on highlighting of elements'}],
           ['--baseurl', {"dest":'baseurl', "help":'Base url to load in selenium browser'}]]

def pytest_addoption(parser):
    group = parser.getgroup('cfme', 'cfme')
    for option in options:
        group._addoption(option[0], **option[1] )

def highlight(element):
    """Highlights (blinks) a Webdriver element.
        In pure javascript, as suggested by https://github.com/alp82.
    """
    driver = element._parent
    driver.execute_script("""
            element = arguments[0];
            original_style = element.getAttribute('style');
            element.setAttribute('style', original_style + "; background: yellow;");
            setTimeout(function(){
                element.setAttribute('style', original_style);
            }, 30);
            """, element)

def pytest_configure(config):
    from selenium.webdriver.remote.webelement import WebElement
    def _execute(self, command, params=None):
        highlight(self)
        return self._old_execute(command, params)

    # Let's add highlight as a method to WebDriver so we can call it arbitrarily
    WebElement.highlight = highlight

    if (config.option.highlight):
        WebElement._old_execute = WebElement._execute
        WebElement._execute = _execute


def find(cls, locator_name):
    return sel().find_element(*cls.locators[locator_name])


def click(cls, el):
    find(cls, el).click()
