import pytest
import threading
from selenium import webdriver
from contextlib import contextmanager

thread_locals = threading.local()

@contextmanager
def selenium_session(cls, *args, **kwargs):
    thread_locals.selenium = cls(*args, **kwargs)
    yield thread_locals.selenium
    thread_locals.selenium.quit()

@pytest.yield_fixture
def selenium():
    with selenium_session(webdriver.Firefox) as sel:
        yield sel



