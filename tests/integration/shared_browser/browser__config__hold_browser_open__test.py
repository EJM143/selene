import atexit

from selene import have
from selene.support.shared import browser, SharedConfig
from selene.support.webdriver import Help


def setup_function():
    browser.config.hold_browser_open = SharedConfig().hold_browser_open
    """setting to default"""


def teardown_function():
    browser.config.hold_browser_open = SharedConfig().hold_browser_open
    browser.quit()


def test_no_hold_on_default_false():
    browser.open('http://todomvc.com/examples/emberjs/')
    driver = browser.driver
    browser.element('#new-todo').type('a').press_enter()

    atexit._run_exitfuncs()

    assert not Help(driver).has_browser_still_alive()


def test_hold_on_explicit_true():
    browser.config.hold_browser_open = True
    browser.open('http://todomvc.com/examples/emberjs/')
    browser.element('#new-todo').type('a').press_enter()

    atexit._run_exitfuncs()
    browser.element('#new-todo').type('b').press_enter()

    browser.all('#todo-list>li').should(have.texts('a', 'b'))
