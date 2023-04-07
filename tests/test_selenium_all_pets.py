from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_petfriends():

    errors = []

    # Создание экземпляра веб-драйвера
    selenium = webdriver.Chrome()

    # Открыть страницу:
    selenium.get("https://petfriends.skillfactory.ru/")

    # Создание объекта WebDriverWait и Настройка неявных ожиданий
    wait = WebDriverWait(selenium, 10)
    selenium.implicitly_wait(10)

    # Нажать на кнопку "Зарегистрироваться"
    btn_newuser = selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # Нажать на ссылку "У меня уже есть аккаунт"
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # Ввести почту
    field_email = selenium.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("iish@kut.ut")

    # Ввести пароль
    field_pass = selenium.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("12345")

    # Кликнуть на кнопку "Войти"
    btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Ждем, пока страница загрузится после авторизации
    time.sleep(5)

    # Проверяем наличие элементов с именем класса card (карточка питомца)
    card_elements = selenium.find_elements(By.CSS_SELECTOR, "div.card")
    if len(card_elements) > 0:
        print("Карточки питомцев найдены на странице")
    else:
        print("Карточки питомцев не найдены на странице")

    # Проверяем, что у каждого питомца есть фото, имя и возраст
    for card in card_elements:
        photo_element = card.find_element(By.CSS_SELECTOR, "img.card-img-top")
        name_element = card.find_element(By.CSS_SELECTOR, "h5.card-title")
        age_element = card.find_element(By.CSS_SELECTOR, "p.card-text")

        if not photo_element.is_displayed():
            errors.append("Фото питомца не отображается на карточке")
        if not name_element.text:
            errors.append("Имя питомца не отображается на карточке")
        if not age_element.text:
            errors.append("Возраст питомца не отображается на карточке")

    # Выводим ошибки, если они есть
    if errors:
        print("Ошибки:")
        for error in errors:
            print("- " + error)
    else:
        print("Ошибок не найдено")

    # Перейти на главную страницу
    #selenium.get("https://petfriends.skillfactory.ru/all_pets")

    # Кликнуть на гамбургер
    menu_button = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/nav/button/span')))
    menu_button.click()

    # Ждем некоторое время, чтобы меню успело открыться
    time.sleep(5)

    # Кликнуть на ссылку "Мои питомцы"
    my_pets_link = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    my_pets_link.click()

    # Проверяем, что мы находимся на странице "Мои питомцы"
    assert "my_pets" in selenium.current_url, "Переход на страницу 'Мои питомцы' не выполнен"
    print("Карточки питомцев не найдены на странице")

    # Ждем некоторое время
    time.sleep(5)

    # Ожидание появления таблицы с питомцами
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table-hover")))

    # Проверяем наличие таблицы с питомцами
    assert selenium.find_element(By.CSS_SELECTOR, "table.table-hover"), "Таблица с питомцами не найдена на странице"
    # получаем все строки таблицы
    rows = selenium.find_elements(By.CSS_SELECTOR, "table.table-hover tbody tr")

    # проверяем, что количество строк больше 0
    assert len(rows) > 0, "Нет строк в таблице с питомцами"

    # проверяем, что хотя бы у половины питомцев есть фото
    photos_count = 0
    for row in rows:
        if row.find_elements(By.XPATH, "td[4]//img"):
            photos_count += 1
    try:
        assert photos_count >= len(rows) / 2, "У менее чем половины питомцев есть фото"
    except AssertionError as e:
        errors.append(str(e))
    print("Продолжаем выполнение теста")

    # проверяем, что у всех питомцев есть имя, возраст и порода
    for row in rows:
        assert row.find_element(By.XPATH, "td[1]").text != "", "У питомца нет имени"
        assert row.find_element(By.XPATH, "td[2]").text != "", "У питомца нет породы"
        assert row.find_element(By.XPATH, "td[3]").text != "", "У питомца нет возраста"

    # проверяем, что у всех питомцев разные имена
    names = set()
    for row in rows:
        pet_name = row.find_element(By.XPATH, "td[1]").text
    try:
        assert pet_name not in names, "Имя питомца повторяется в таблице"
    except AssertionError as e:
        errors.append(str(e))
    print("Продолжаем проверку имен")
    names.add(pet_name)

    # проверяем, что в списке нет повторяющихся питомцев
    breeds = set()
    for row in rows:
        pet_breed = row.find_element(By.XPATH, "td[2]").text
    try:
        assert pet_breed not in breeds, "Порода питомца повторяется в таблице"
    except AssertionError as e:
        errors.append(str(e))
    print("Продолжаем проверку пород")
    breeds.add(pet_breed)

    # Запись ошибок в файл
    if errors:
        with open("errors.txt", "w") as f:
            for error in errors:
                f.write(f"{error}\n")
        print("Ошибки теста записаны в файл errors.txt")
    else:
        print("Тест выполнен успешно, ошибок не обнаружено")

    # закрываем браузер
    selenium.quit()