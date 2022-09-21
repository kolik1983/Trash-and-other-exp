import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# получает значения из консоли
def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help="Choose language: 'ru' or 'en'")
    parser.addoption('--headless', action='store', default='None',
                     help="Open a browser invisible, without GUI is used by default")
    # parser.addoption('--window_size', action='store', default='1920,1080',
    #                  help='Choose the any windows size')



@pytest.fixture(scope="function")
def browser(request):
    # Значения переменных user_language / browser_name / headless принимаются из консоли.
    user_language = request.config.getoption("language")
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption('headless')
    #size = request.config.getoption('window_size')


    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        # Чтобы указать язык браузера, использую класс Options и метод add_experimental_option
        # Без браузерный режим для 'Chrome'
        options = Options()
        if headless == 'true':
            options.add_argument('headless')


        # // Отключение сообщений в консоли типа: USB: usb_device_handle...
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # // Выбор языка страницы
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        #options.add_experimental_option('size')
        browser = webdriver.Chrome(options=options)
        browser.set_window_size(1920, 1080)
        browser.implicitly_wait(10) # Не явное ожидание элементов 10 сек.

    elif browser_name == "firefox":

        print("\nstart firefox browser for test..")
        # Без браузерный режим для 'Firefox', через импорт библиотеки 'os'
        if headless == 'true':
            os.environ['MOZ_HEADLESS'] = '1'

        # Чтобы указать язык браузера, использую класс Options и метод add_experimental_option
        # Для Firefox  браузера
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(firefox_profile=fp)
        browser.set_window_size(1920, 1080)
        browser.implicitly_wait(10)  # Не явное ожидание элементов 10 сек.

    elif browser_name == "yandex":

        options = Options()
        if headless == 'true':
            options.add_argument('headless')

        service = Service("102_chromedriver.exe")
        options.binary_location = "C:/Users/erigo/AppData/Local/Yandex/YandexBrowser/Application/browser.exe"

        # // Отключение сообщений в консоли типа: USB: usb_device_handle...
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(options=options, service=service)
        browser.set_window_size(1920, 1080)
        browser.implicitly_wait(10)


    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox or yandex")
    yield browser
    print("\nquit browser..")
    browser.quit()


# Supports console options (pytest):
# --browser_name= (firefox or chrome or yandex)
# --language=ru (default='en')
# --headless=true (default='None')

# pytest -v -s  --tb=line --reruns 1  --browser_name=chrome --language=ru --headless=None   test_1_page.py
# for launch yandex - pytest -v -s  --tb=line --reruns 1  --browser_name=yandex --language=ru --headless=true   test_1_page.py
# для корректной работы Яндекс браузера необходимо скачать хромдрайвер 102 версии, той же на которой работает Яндекс. 
