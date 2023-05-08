import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

EXCEL_FILE = "cards.xlsx"
HOST = 'https://dom.ria.com'
URL = f'{HOST}/uk/prodazha-kvartir/lvov/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='wrap_desc p-rel')
    cards = []

    for item in items:
        area_list = item.find_all('a')
        cards.append(
            {
                'price': item.find('b', class_='size18').get_text(),
                'price per m^2': item.find('span', class_='point-before').get_text(),
                'street': item.find('h2', class_='tit').find('a').get_text(),
                'area': area_list[1].get_text() if len(area_list) > 1 else None,
                'rooms': item.find('div', class_='mt-10 chars grey').find_all('span')[0].get_text(),
                'm^2': item.find('div', class_='mt-10 chars grey').find_all('span')[1].get_text(),
                'floor': item.find('div', class_='mt-10 chars grey').find_all('span')[2].get_text()
                if len(item.find('div', class_='mt-10 chars grey').find_all('span')) > 2 else None,
            }
        )
    return cards


def save_doc(items, path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Ціна', 'Ціна за м^2', 'Вулиця', 'Район', 'Клк кімнат', 'В метрах квадратних', 'Поверх'])
    for item in items:
        sheet.append([item['price'], item['price per m^2'], item['street'], item['area'], item['rooms'], item['m^2'],
                      item['floor']])
    workbook.save(filename=path)


page = 1
cards = []

for page in range(1, 253):
    url = f'{HOST}/uk/prodazha-kvartir/lvov/?page={page}'
    html = get_html(url)
    cards += get_content(html.text)
    if not cards:
        break
    print(f'Parsed page {page}')

save_doc(cards, EXCEL_FILE)

print('Done')
