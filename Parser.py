from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import codecs, re, csv

# источник данных для выборки по аренде квартир
url = "https://www.avito.ru/magnitogorsk/kvartiry"

# передача управления веб-драйверу для входа на сайт Avito
driver = webdriver.Chrome()
driver.get(url)

# ввод запроса в поле поиска на сайте Avito
elem = driver.find_element_by_class_name("input-input-Zpzc1")
elem.send_keys("Аренда квартиры 1к")
elem.send_keys(Keys.RETURN)

# открытие файла res.csv в режиме записи для сохранения данных
with open('res.csv', 'w', encoding="utf-16", newline='') as output:
    writer = csv.writer(output, delimiter=";")

# передача результата работы веб-драйвера в модуль BeautifulSoup для обработки
    soup = BeautifulSoup(driver.page_source, 'lxml')

# поиск ссылок на объявления о сдаче картир и цен на них
    hrefs = soup.find_all(href=re.compile("magnitogorsk/kvartiry"), class_=re.compile("link-link-MbQDP"))
    prices = soup.find_all(class_=re.compile("price-text-_YGDY"))

# создание строк выходных данных из ссылки, описания и цены съема квартиры
    for i in range(len(hrefs)):
        row = []
        row.append(str('https://www.avito.ru/' + hrefs[i].get('href')))
        row.append(str(hrefs[i].get('title').replace("\xa0", '').strip('Объявление ')))
        row.append(str(prices[i].text.replace('\xa0', '')))
# запись полученной строки в файл
        writer.writerow(row)
driver.close()
