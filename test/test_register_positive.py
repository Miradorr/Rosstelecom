

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
VALID_EMAIL = 'd1s2f1q2@gmail.com'
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


# Полный сценарий регистрации требует подтверждения кода из email, что невозможно автоматизировать без тестового API.
# Поэтому реализован один демонстрационный тест, проверяющий корректность заполнения формы и переход к окну подтверждения.
def test_register_valid_data_email(driver):
    '''Регистрация с корректными данными по email'''

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

    # Задержка для возможности ввести кода вручную
    # Код может прийти не сразу, поэтому ставим время с запасом
    time.sleep(120)

    # Ожидаем появления элемента с именем пользователя
    user_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.user-name.user-info__name'))
    )

    # Проверяем, что мы успешно вошли в систему
    assert f'{VALID_LASTNAME} {VALID_FIRSTNAME}' in user_name.text, 'Имя пользователя не отображается, возможно, авторизация не удалась'



