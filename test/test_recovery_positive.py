

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Настройки
URL = 'https://b2c.passport.rt.ru/'
VALID_FIRSTNAME = 'Евгений'
VALID_LASTNAME = 'Морозов'
VALID_PHONE = '79966212252'
VALID_EMAIL = 'mac2offee@gmail.com'
VALID_PASSWORD = 'Qwerty7729'


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


def test_password_recovery_by_phone(driver):
    '''Восстановление пароля по номеру телефона'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Забыл пароль'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    ).click()

    # Ждем появления вкладки 'Телефон'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))).click()

    # Вводим номер телефона
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    phone_field.send_keys(VALID_PHONE)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset').click()

    # Ждем появления формы выбора способа восстановления пароля
    sms_reset = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'sms-reset-type')))

    # Выбрать радиокнопку 'По номеру телефона'
    sms_reset.click()

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset-form-submit').click()

    # Ждем появления формы ввода кода из SMS
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rt-code-input')))

    # Задержка для возможности ввести кода из SMS вручную
    time.sleep(30)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.XPATH, '//*[@id="otp"]/div[2]/button').click()

    # Дождаться появления формы ввода нового пароля
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password-new"]')))

    # Ввести новый пароль
    driver.find_element(By.XPATH, '//*[@id="password-new"]').send_keys('Qazwsx7890')

    # Подтвердить новый пароль
    driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('Qazwsx7890')

    # Нажимаем кнопку 'Сохранить'
    driver.find_element(By.XPATH, '//*[@id="t-btn-reset-pass"]').click()

    # Проверяем, что перенаправление на страницу авторизации прошло успешно
    title = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'card-title'))
    )
    assert 'Авторизация' in title.text, 'Что-то пошло не так при восстановлении пароля по номеру телефона'


def test_password_recovery_by_email(driver):
    '''Восстановление пароля по email'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Забыл пароль'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    ).click()

    # Ждем появления вкладки 'Почта'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-mail'))).click()

    # Вводим email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys(VALID_EMAIL)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset').click()

    # Ждем появления формы выбора способа восстановления пароля
    email_reset = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'email-reset-type')))

    # Выбрать радиокнопку 'По e-mail'
    email_reset.click()

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.ID, 'reset-form-submit').click()

    # Ждем появления формы ввода кода из email
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rt-code-input')))

    # Задержка для возможности ввести кода из email вручную
    time.sleep(30)

    # Нажимаем кнопку 'Продолжить'
    driver.find_element(By.XPATH, '//*[@id="otp"]/div[2]/button').click()

    # Ждем появления формы ввода нового пароля
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password-new"')))

    # Ввести новый пароль
    driver.find_element(By.XPATH, '//*[@id="password-new"]').send_keys('Rtyuio8090')

    # Подтвердить новый пароль
    driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('Rtyuio8090')

    # Нажимаем кнопку 'Сохранить'
    driver.find_element(By.XPATH, '//*[@id="t-btn-reset-pass"]').click()

    # Проверяем, что перенаправление на страницу авторизации прошло успешно
    title = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'card-title'))
    )
    assert 'Авторизация' in title.text, 'Что-то пошло не так при восстановлении пароля по номеру телефона'



