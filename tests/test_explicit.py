import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


@pytest.fixture(autouse=True)
def testing():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--kiosk')
    # chrome_options.add_argument('headless')
    s = Service(r'C:\Users\Egorro\PycharmProjects\module25\chromedriver.exe')
    pytest.driver = webdriver.Chrome(service=s, options=chrome_options)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email:
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))).send_keys('egorro@inbox.ru')
    # Вводим пароль:
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))).send_keys('Petgorro')
    # Нажимаем на кнопку входа в аккаунт:
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.task3.fill>div.text-center'))).text == "Все питомцы наших пользователей"

    images = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 3