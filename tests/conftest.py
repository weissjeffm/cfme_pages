import pytest
import threading
from selenium import webdriver
from contextlib import contextmanager

thread_locals = threading.local()

@contextmanager
def selenium_session(cls):
    thread_locals.selenium = object.__new__(cls)
    thread_locals.selenium.__init__()
    yield thread_locals.selenium
    thread_locals.selenium.quit()

@pytest.yield_fixture
def selenium():
    with selenium_session(webdriver.Firefox) as sel:
        yield sel



