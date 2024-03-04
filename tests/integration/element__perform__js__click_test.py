import time

from selene import command
from tests.integration.helpers.givenpage import GivenPage


def test_command_js_click_does_not_wait_for_no_overlay(session_browser):
    browser = session_browser.with_(timeout=0.5)
    page = GivenPage(browser.driver)
    page.opened_with_body(
        '''
        <div
            id="overlay"
            style='
                display:block;
                position: fixed;
                display: block;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.1);
                z-index: 2;
                cursor: pointer;
            '
        >
        </div>
        <a href="#second">go to Heading 2</a>
        <h2 id="second">Heading 2</h2>
        '''
    )
    before_call = time.time()
    page.execute_script_with_timeout(
        '''
        document.getElementById('overlay').style.display='none'
        ''',
        0.75,
    )

    browser.element('a').perform(command.js.click)

    time_diff = time.time() - before_call
    assert time_diff < 0.25
    assert "second" in browser.driver.current_url
