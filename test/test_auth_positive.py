

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


def test_login_valid_phone(driver):
    '''Авторизация по номеру телефона с корректными данными'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Ждем появления вкладки 'Телефон'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-phone'))).click()

    # Вводим номер телефона и пароль, нажимаем на кнопку входа
    driver.find_element(By.ID, 'username').send_keys(VALID_PHONE)
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Ожидаем появления элемента с именем пользователя
    user_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.user-name.user-info__name'))
    )

    # Проверяем, что мы успешно вошли в систему
    assert 'Морозов Евгений' in user_name.text, 'Имя пользователя не отображается, возможно, авторизация не удалась'


def test_login_valid_email(driver):
    '''Авторизация по электронной почте с корректными данными'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Ждем появления вкладки 'Почта'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-mail'))).click()

    # Вводим почту и пароль, нажимаем на кнопку входа
    driver.find_element(By.ID, 'username').send_keys(VALID_EMAIL)
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Ожидаем появления элемента с именем пользователя
    user_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.user-name.user-info__name'))
    )

    # Проверяем, что мы успешно вошли в систему
    assert 'Морозов Евгений' in user_name.text, 'Имя пользователя не отображается, возможно, авторизация не удалась'


def test_login_valid_login(driver):
    '''Авторизация по логину с корректными данными'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Ждем появления вкладки 'Логин'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 't-btn-tab-login'))).click()

    # Вводим логин и пароль, нажимаем на кнопку входа
    driver.find_element(By.ID, 'username').send_keys(VALID_LOGIN)
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)

    # Нажимаем кнопку 'Войти'
    driver.find_element(By.ID, 'kc-login').click()

    # Ожидаем появления элемента с именем пользователя
    user_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.user-name.user-info__name'))
    )

    # Проверяем, что мы успешно вошли в систему
    assert 'Морозов Евгений' in user_name.text, 'Имя пользователя не отображается, возможно, авторизация не удалась'


def test_switch_tabs(driver):
    '''Переключение между вкладками авторизации'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Список вкладок для переключения: Телефон, Почта, Логин, Лицевой счёт
    tabs = ['t-btn-tab-phone', 't-btn-tab-mail', 't-btn-tab-login', 't-btn-tab-ls']

    # Проходим по всем вкладкам по очереди
    for tab_id in tabs:
        # Ожидаем, пока вкладка станет кликабельной, и кликаем по ней
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, tab_id))
        ).click()

        # Добавляем небольшую паузу, чтобы визуально успеть отследить переключение
        time.sleep(0.5)

    # Проверяем, что активная вкладка визуально подсвечена
    active_tab = driver.find_element(By.CSS_SELECTOR, '.rt-tab--active')
    assert active_tab.is_displayed(), 'Активная вкладка не выделяется визуально'


def test_redirect_to_password_recovery(driver):
    '''Проверка перехода по ссылке "Забыл пароль"'''

    # Переходим на страницу авторизации
    driver.get(URL)

    # Находим и нажимаем на ссылку 'Забыл пароль'
    forgot_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'forgot_password'))
    )
    forgot_link.click()

    # Ждём, пока откроется страница восстановления пароля
    WebDriverWait(driver, 10).until(EC.url_contains('reset-credentials'))

    # Проверяем, что произошёл переход по правильному адресу
    assert 'reset-credentials' in driver.current_url, 'Не открылось окно восстановления пароля'


def test_redirect_to_register(driver):
    '''Проверка перехода по ссылке "Зарегистрироваться"'''

    # Открываем страницу авторизации
    driver.get(URL)

    # Находим ссылку 'Зарегистрироваться' и кликаем по ней
    reg_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'kc-register'))
    )
    reg_link.click()

    # Ждем, пока URL изменится на страницу регистрации
    WebDriverWait(driver, 10).until(EC.url_contains('registration'))

    # Проверяем, что переход действительно выполнен
    assert 'registration' in driver.current_url, 'Не открылось окно регистрации'



