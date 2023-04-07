import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def chrome_options(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # открыть браузер в полноэкранном режиме
    options.add_argument("--disable-gpu")  # отключить использование GPU
    options.add_argument("--disable-extensions")  # отключить расширения браузера
    options.add_argument("--no-sandbox")  # запустить Chrome в безопасном режиме

    driver_name = request.config.getoption("--driver")
    if driver_name == "firefox":
        browser = webdriver.Firefox(options=options)
    else:
        browser = webdriver.Chrome(options=options)

    yield browser
    # закрытие браузера после окончания тестов
    browser.quit()

    return options


@pytest.fixture(scope="session", autouse=True)
def web_browser(chrome_options):
    # инициализация Chrome WebDriver
    browser = webdriver.Chrome(options=chrome_options)
    yield browser
    # закрытие браузера после окончания тестов
    browser.quit()


@pytest.fixture(scope="function", autouse=True)
def pytest_runtest_makereport(item, call, __multicall__):
    # сохранение информации об ошибках в отчете
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep