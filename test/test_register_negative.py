

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
VALID_PHONE = '79063391405'
VALID_EMAIL = 'q1f2d5@gmail.com'
VALID_LOGIN = 'rtkid_1761625584986'
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


def test_register_using_existing_email(driver):
    '''Регистрация аккаунта используя уже существующий email'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Зарегистрироваться'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    ).click()

    # Находим поле 'Регион'
    region_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='new-password']"))
    )

    # Нажимаем по полю, чтобы активировать
    region_input.click()

    # Вводим нужный регион
    region_input.send_keys('Самарская обл')

    # Ждём появления списка регионов и выбираем нужный
    region_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-select__list-item'))
    )
    region_list.click()

    # Вводим имя
    driver.find_element(By.NAME, 'firstName').send_keys(VALID_FIRSTNAME)

    # Вводим фамилию
    driver.find_element(By.NAME, 'lastName').send_keys(VALID_LASTNAME)

    # Вводим почту
    driver.find_element(By.ID, 'address').send_keys(VALID_EMAIL)

    # Вводим пароль
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)

    # Подтверждаем пароль
    driver.find_element(By.ID, 'password-confirm').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Зарегистрироваться'
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Ожидаем появления окна с предупреждением
    msg_title = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.card-modal__title'))
    )

    # Проверяем, что окно с предупреждением существует
    assert 'Учётная запись уже существует' in msg_title.text, 'Окно с предупреждением о существовании аккаунта - не появилось'


def test_register_short_password(driver):
    '''Ошибка при вводе слишком короткого пароля'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Зарегистрироваться'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    ).click()

    # Вводим нужный регион
    region_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='new-password']")))
    region_input.click()
    region_input.send_keys('Самарская обл')
    region_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-select__list-item')))
    region_list.click()

    # Вводим корректные имя и фамилию
    driver.find_element(By.NAME, 'firstName').send_keys(VALID_FIRSTNAME)
    driver.find_element(By.NAME, 'lastName').send_keys(VALID_LASTNAME)

    # Вводим почту
    driver.find_element(By.ID, 'address').send_keys(VALID_EMAIL)

    # Вводим короткий пароль
    driver.find_element(By.ID, 'password').send_keys('ABC')
    driver.find_element(By.ID, 'password-confirm').send_keys('ABC')

    # Нажимаем кнопку 'Зарегистрироваться'
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что появилось сообщение об ошибке
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.new-password-container .rt-input-container__meta'))
    ).text

    assert 'Длина пароля должна быть не менее' in error_msg, 'Нет сообщения о некорректной длине пароля'


def test_register_password_mismatch(driver):
    '''Ошибка при несовпадении пароля и подтверждения'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Зарегистрироваться'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    ).click()

    # Вводим нужный регион
    region_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='new-password']")))
    region_input.click()
    region_input.send_keys('Самарская обл')
    region_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-select__list-item')))
    region_list.click()

    # Вводим корректные имя и фамилию
    driver.find_element(By.NAME, 'firstName').send_keys(VALID_FIRSTNAME)
    driver.find_element(By.NAME, 'lastName').send_keys(VALID_LASTNAME)

    # Вводим почту
    driver.find_element(By.ID, 'address').send_keys(VALID_EMAIL)

    # Вводим два разных пароля
    driver.find_element(By.ID, 'password').send_keys('Qwerty1234')
    driver.find_element(By.ID, 'password-confirm').send_keys('Qwerty5678')

    # Нажимаем кнопку 'Зарегистрироваться'
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что появилось сообщение о несовпадении паролей
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.new-password-container .rt-input-container__meta'))
    ).text

    assert 'Пароли не совпадают' in error_msg, 'Нет предупреждения о несовпадении паролей'


def test_register_invalid_email(driver):
    '''Ошибка при вводе некорректного email'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Зарегистрироваться'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    ).click()

    # Вводим нужный регион
    region_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='new-password']")))
    region_input.click()
    region_input.send_keys('Самарская обл')
    region_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-select__list-item')))
    region_list.click()

    # Вводим корректные имя и фамилию
    driver.find_element(By.NAME, 'firstName').send_keys(VALID_FIRSTNAME)
    driver.find_element(By.NAME, 'lastName').send_keys(VALID_LASTNAME)

    # Вводим неправильный адрес (без @)
    driver.find_element(By.ID, 'address').send_keys('qwerty.gmail.com')

    # Вводим пароль
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)
    driver.find_element(By.ID, 'password-confirm').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Зарегистрироваться'
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что появилось сообщение о неверном формате email
    assert 'Введите корректный адрес' in driver.page_source or '@' in driver.page_source, \
        'Нет сообщения об ошибке при неверном формате email'

    # Проверяем, что появилось сообщение о неправильной почте
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.email-phone-con .rt-input-container__meta'))
    ).text

    assert 'Введите телефон в формате' in error_msg and 'или email в формате' in error_msg, 'Нет сообщения об ошибке при неверном формате email'


def test_register_empty_fields(driver):
    '''Ошибка при пустых полях регистрации'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Нажимаем ссылку 'Зарегистрироваться'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    ).click()

    # Не заполняем ни одно поле и сразу нажимаем 'Зарегистрироваться'
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что появилось сообщение об обязательных полях
    assert 'Укажите' in driver.page_source or 'заполнить' in driver.page_source, 'Не отображается ошибка при пустых полях'



