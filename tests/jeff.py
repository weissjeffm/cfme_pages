import pytest

@pytest.mark.nondestructive
@pytest.mark.usefixtures("selenium")
class Foo:
    def test_mytest(self, selenium):
        selenium.get("http://google.com")
