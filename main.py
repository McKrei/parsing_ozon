import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


class Parsing:
    '''Класс для сохранения состояния драйвера и получения html страницы'''
    def __init__(self, path_driver):
        service = Service(executable_path=path_driver)
        # Добавьте любые необходимые опции для вашего кода
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-features=PrivacySandbox')
        # chrome_options.add_argument('--disable-features=InterestCohort')
        # chrome_options.add_argument('--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure,InterestCohortFeaturePolicy')
        # chrome_options.add_argument("--disable-features=EnableExperimentalWebPlatformFeatures")
        # Запуск драйвера Chrome
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_page(self, url):
        '''Получаем html страницы'''
        # Открываем динамическую веб-страницу
        self.driver.get(url)
        # Дайте некоторое время для загрузки динамического контента
        self.driver.implicitly_wait(4)
        # Получаем исходный код страницы
        time.sleep(7)
        page_source = self.driver.page_source
        return page_source


def get_all_data_page(page_source: str) -> list:
    soup = BeautifulSoup(page_source, "lxml")
    all_data = []
    # print(page_source)
    blocks = soup.find_all('div', {'class': 'pk1 p1k'})
    # print(blocks)
    print(len(blocks))
    for block in blocks:
        if not block:
            continue
        url = block.find('a', {'class': 'tile-hover-target mk k0m'})
        # info = block.find('span', {'class': 'em4 me4 em8 tsBodyM mk'}).find_all('font', {'color': '#001a34'})
        # info = [el.text for el in info]
        # price = block.find('div', {'class': 'pk2'}).text
        # price = re.findall(r'\d+.+?₽', price)
        # price = price[0][:-1] if price else None
        all_data.append((
            block.find('span', {'class': 'em4 me4 em5 em7 tsBodyL mk k0m'}).text,
            # *info,
            # price,
            url.get('href') if url else None,
        ))
    return all_data


def save_data_to_csv(data) -> list[list]:
    with open("data.csv", "a", encoding="utf-8") as file:
        for item in data:
            file.write('|'.join(map(str, item)) + '\n')


columns = [
    "Название",
    # "тип",
    # "Диагональ экрана, дюйм",
    # "Емкость аккумулятора, мАч:",
    # "Процессор:",
    # "Основной материал корпуса:"
    # "цена",
    "ссылка на товар",
]


def main():
    save_data_to_csv([columns])
    url = "https://www.ozon.ru/category/smartfony-15502/xiaomi-32686750/?page="

    for i in range(1, 280):
        parsing = Parsing('chromedriver.exe')
        print(i)
        page = parsing.get_page(f'{url}{i}')
        data = get_all_data_page(page)
        save_data_to_csv(data)
        parsing.driver.quit()
        time.sleep(1)

if __name__ == '__main__':
    main()
