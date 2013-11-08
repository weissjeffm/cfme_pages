import pytest
import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from contextlib import contextmanager

# Some thread local storage that only gets set up
# once, won't get blown away when reloading module
if not 'thread_locals' in globals():
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


config = None  # for easy access to pytest config


@pytest.yield_fixture
def selenium(request):
    global config
    config = request.config
    with selenium_session(webdriver.Firefox) as sel:
        yield sel


options = [['--highlight', {"action": 'store_true',
                            "dest": 'highlight',
                            "default": False,
                            "help": 'whether to turn on highlighting of elements'}],
           ['--baseurl', {"dest": 'baseurl', "help": 'Base url to load in selenium browser'}]]


def pytest_addoption(parser):
    group = parser.getgroup('cfme', 'cfme')
    for option in options:
        group._addoption(option[0], **option[1])


def highlight(element):
    """Highlights (blinks) a Webdriver element.
        In pure javascript, as suggested by https://github.com/alp82.
    """
    sel().execute_script("""
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

ajax_wait_js = """
var errfn = function(f,n) { try { return f(n) } catch(e) {return 0}};
return errfn(function(n) { return jQuery.active }) +
errfn(function(n) { return Ajax.activeRequestCount });
"""


def wait_for_ajax():
    WebDriverWait(sel(), 120.0).until(lambda s: s.execute_script(ajax_wait_js),
                                      "Ajax wait timed out")


def click(el):
    ActionChains(sel()).move_to_element(sel().find_element(*el)).click().perform()
    wait_for_ajax()


def is_displayed(el):
    try:
        return sel().find_element(*el).is_displayed()
    except NoSuchElementException:
        return False


def move_to_element(el):
    ActionChains(sel()).move_to_element(sel().find_element(*el))


def text(el):
    return sel().find_element(*el).text


def get_attribute(el, attr):
    return sel().find_element(*el).get_attribute(attr)


def send_keys(el, text):
    sel().find_element(*el).send_keys(text)
    wait_for_ajax()
