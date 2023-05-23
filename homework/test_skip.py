"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""
import pytest
from selene import command
from selene.support.shared import browser
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (320, 240), (1600, 1200), (240, 320)],
                ids=['desktop', 'mobile', 'desktop', 'mobile'])
def web_browser(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]
    param_id = request.node.callspec.id
    request_name = request.node.name

    if 'mobile' in param_id and 'desktop' in request_name:
        pytest.skip('Мобильное соотношение сторон не подходит для данного теста')
    elif 'desktop' in param_id and 'mobile' in request_name:
        pytest.skip('Десктопное соотношение сторон не подходит для данного теста')

    yield browser

    browser.quit()


@pytest.mark.desktop
def test_github_desktop(web_browser):
    browser.open('https://github.com')
    browser.element('[class*=HeaderMenu-link--sign-in]').click()


@pytest.mark.mobile
def test_github_mobile(web_browser):
    browser.open('https://github.com')
    browser.element('.Button--link').click()
    browser.element('[class*=HeaderMenu-link--sign-in]').perform(command.js.scroll_into_view)
    browser.element('[class*=HeaderMenu-link--sign-in]').click()
