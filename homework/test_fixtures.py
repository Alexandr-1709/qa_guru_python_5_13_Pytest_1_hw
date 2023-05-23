"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""
import pytest
from selene import browser, command
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1600, 1200)])
def web_browser_for_desktop_window(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]

    yield browser

    browser.quit()


@pytest.fixture(params=[(320, 240), (240, 320)])
def web_browser_for_mobile_window(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]

    yield browser

    browser.quit()


def test_github_desktop(web_browser_for_desktop_window):
    browser.open('https://github.com')
    browser.element('[class*=HeaderMenu-link--sign-in]').click()


def test_github_mobile(web_browser_for_mobile_window):
    browser.open('https://github.com')
    browser.element('.Button--link').click()
    browser.element('[class*=HeaderMenu-link--sign-in]').perform(command.js.scroll_into_view)
    browser.element('[class*=HeaderMenu-link--sign-in]').click()
