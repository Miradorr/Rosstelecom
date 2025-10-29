

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Настройки
URL = 'https://b2c.passport.rt.ru/'
VALID_PHONE = '79063391405'
VALID_EMAIL = 'q1f2d5@gmail.com'
VALID_LOGIN = 'rtkid_1761625584986'
VALID_PASSWORD = 'Qwerty7729'
INVALID_PASSWORD = '123456Qwerty'


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


def test_login_wrong_password(driver):
    '''Проверка отображения ошибки при авторизации с неверным паролем'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переключаемся на вкладку 'Телефон'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))
    ).click()

    # Вводим существующий номер телефона
    driver.find_element(By.ID, 'username').send_keys(VALID_PHONE)

    # Вводим неверный пароль
    driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'form-error-message'))
    ).text

    assert 'Неверный логин или пароль' in error_msg, 'Ожидалось сообщение об ошибке при неверном пароле, но его нет'


def test_login_unregistered_phone(driver):
    '''Проверка входа с несуществующим номером телефона'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переключаемся на вкладку 'Телефон'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))
    ).click()

    # Вводим несуществующий номер телефона
    driver.find_element(By.ID, 'username').send_keys('79969399495')

    # Вводим любой валидный по формату пароль
    driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'form-error-message'))
    ).text

    assert 'Неверный логин или пароль' in error_msg, 'Сообщение об ошибке не отображается при несуществующем номере телефона'


def test_login_empty_fields(driver):
    '''Проверка поведения при пустых полях логина и пароля'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем кнопку 'Войти' сразу, не заполняя поля
    driver.find_element(By.ID, 'kc-login').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username-meta'))
    ).text

    assert 'Введите номер телефона' in error_msg, 'Сообщение об ошибке отсутствует при попытке входа с пустыми полями'


def test_login_with_special_symbols(driver):
    '''Проверка входа при вводе недопустимых символов в поле логина'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переключаемся на вкладку 'Логин'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 't-btn-tab-login'))
    ).click()

    # Вводим в поле логина набор спецсимволов
    driver.find_element(By.ID, 'username').send_keys('!@#$%^&*()')

    # Вводим любой валидный по формату пароль
    driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Проверяем, что появилось сообщение об ошибке
    error_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'form-error-message'))
    ).text

    assert 'Неверный логин или пароль' in error_text, 'Не отображается сообщение об ошибке при вводе недопустимых символов'


def test_login_short_phone_number(driver):
    '''Проверка поведения при вводе слишком короткого номера телефона'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Переключаемся на вкладку 'Телефон'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))
    ).click()

    # Вводим короткий номер (меньше 11 цифр)
    driver.find_element(By.ID, 'username').send_keys('79630')

    # Вводим пароль
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username-meta'))
    ).text

    assert 'Неверный формат телефона' in error_msg, 'Ошибка при коротком номере телефона не отображается'



