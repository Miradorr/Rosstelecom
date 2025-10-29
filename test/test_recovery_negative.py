

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Настройки
URL = 'https://b2c.passport.rt.ru/'
INVALID_PHONE = '12345'
INVALID_LOGIN = 'abc0000'
NOT_EXIST_PHONE = '375999999999'


@pytest.fixture()
def driver():
    '''Фикстура для инициализации веб-драйвера Chrome'''

    # Создаем экземпляр браузера Google Chrome и открываем его в полноэкранном режиме
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    # Устанавливаем неявное ожидание в 10 секунд
    browser.implicitly_wait(10)

    # Передаем управление тесту
    yield browser

    # Закрываем браузер после выполнения теста
    browser.quit()


def test_recovery_with_invalid_phone(driver):
    '''Ошибка при вводе некорректного номера телефона'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переходим по ссылке 'Забыл пароль'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    ).click()

    # Ждем появления вкладки 'Телефон'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))).click()

    # Вводим неправильный номер телефона
    driver.find_element(By.ID, 'username').send_keys(INVALID_PHONE)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.rt-input-container .rt-input-container__meta'))
    )

    assert 'Неверный формат телефона' in error_msg.text, 'Нет сообщения об ошибке при вводе некорректного телефона'


def test_recovery_with_invalid_login(driver):
    '''Ошибка при вводе некорректного логина'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переходим по ссылке 'Забыл пароль'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    ).click()

    # Ждем появления вкладки 'Логин'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-login'))).click()

    # Вводим некорректный логин
    driver.find_element(By.ID, 'username').send_keys(INVALID_LOGIN)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'form-error-message'))
    )

    assert 'Неверный логин' in error_msg.text, 'Нет сообщения об ошибке при вводе несуществующего логина'


def test_recovery_with_not_exist_account(driver):
    '''Ошибка при вводе несуществующего номера телефона'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переходим по ссылке 'Забыл пароль'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    ).click()

    # Ждем появления вкладки 'Телефон'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))).click()

    # Вводим несуществующий номер
    driver.find_element(By.ID, 'username').send_keys(NOT_EXIST_PHONE)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'form-error-message'))
    )

    assert 'Неверный логин' in error_msg.text, 'Нет сообщения о несуществующем пользователе'



