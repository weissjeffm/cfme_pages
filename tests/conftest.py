import pytest
import threading
from selenium import webdriver

thread_locals = threading.local()

@pytest.yield_fixture
def selenium(request):
    thread_locals.selenium = webdriver.Firefox()
    try:
        yield thread_locals.selenium
    finally:
        thread_locals.selenium.quit()



