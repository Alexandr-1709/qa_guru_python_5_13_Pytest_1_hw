"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import browser, command
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1600, 1200), (320, 240), (240, 320)])
def web_browser(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]

    yield browser

    browser.quit()


@pytest.mark.parametrize('web_browser', [(1920, 1080), (1600, 1200)], indirect=True)
def test_github_desktop(web_browser):
    browser.open('https://github.com')
    browser.element('[class*=HeaderMenu-link--sign-in]').click()


# Другой вариант через переменную-декоратор
mobile_only = pytest.mark.parametrize('web_browser', [(320, 240), (240, 320)], indirect=True)


@mobile_only
def test_github_mobile(web_browser):
    browser.open('https://github.com')
    browser.element('.Button--link').click()
    browser.element('[class*=HeaderMenu-link--sign-in]').perform(command.js.scroll_into_view)
    browser.element('[class*=HeaderMenu-link--sign-in]').click()
