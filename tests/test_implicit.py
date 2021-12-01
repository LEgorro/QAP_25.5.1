import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(autouse=True)
def testing():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--kiosk')
    s = Service(r'C:\Users\Egorro\PycharmProjects\module25\chromedriver.exe')
    pytest.driver = webdriver.Chrome(service=s, options=chrome_options)
    pytest.driver.implicitly_wait(5)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('egorro@inbox.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('Petgorro')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Заходим в список "моих питомцев"
    pytest.driver.find_element_by_xpath("//ul//*[contains(text(), 'Мои питомцы')]").click()

    yield

    pytest.driver.quit()


def test_there_are_all_my_pets():
    # Получаем информацию о пользователе (имя, кол-во питомцев, друзей и сообщений)
    user_info = pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]')
    # Получаем список "Моих питомцев" из таблицы
    my_pets = pytest.driver.find_elements_by_css_selector('tbody tr')

    # Из информации о пользователе извелкаем количество питомцев
    num_of_pets = int((user_info.text).split()[::-1][4])

    # Сравниваем количество питомцев в информации о пользователе и в таблице
    assert num_of_pets == len(my_pets)


def test_half_of_pets_have_photo():
    # Получаем фотографии моих питомцев из таблицы
    images = pytest.driver.find_elements_by_css_selector('tbody tr th img')

    # Подсчитываем количество питомцев с фотографией
    pets_with_photo = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            pets_with_photo += 1

    # Проверяем, что больше половины питомцев имеет фотографию
    assert len(images) / 2 <= pets_with_photo


def test_all_pets_have_name_type_and_age():
    # Получаем список "Моих питомцев" из таблицы
    my_pets = pytest.driver.find_elements_by_css_selector('tbody tr')

    # Подсчитываем количество питомцев, у которых указано имя, тип и возраст
    pets_with_name_type_and_age = 0
    for i in range(len(my_pets)):
        if len(my_pets[i].text.split()) == 4:
            pets_with_name_type_and_age += 1

    # Сравниваем количеством питомцев с именем, типом и возастом с общим количеством питомцев
    assert pets_with_name_type_and_age == len(my_pets)


def test_all_pets_have_different_names():
    # Получаем список имён "Моих питомцев" из таблицы
    name_elements = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')

    # Создаём список имён в текстовом виде
    names = []
    for i in range(len(name_elements)):
        names.append(name_elements[i].text)

    # Проверяем, с помощью преобразования списка(list) в множество(set), все ли имена у питомцев уникальные
    assert len(set(names)) == len(names)


def test_all_pets_are_different():
    # Получаем список "Моих питомцев" из таблицы
    my_pets = pytest.driver.find_elements_by_css_selector('tbody tr')

    # Создаём список с информацией о питомцах в текстовом виде
    pets = []
    for i in range(len(my_pets)):
        pets.append(my_pets[i].text)

    # Проверяем, с помощью преобразования списка(list) в множество(set), нет ли повторяющихся питомцев
    assert (len(pets)) == len(set(pets))