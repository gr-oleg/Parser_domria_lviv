import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

EXCEL_FILE = "cards.xlsx"
HOST = 'https://dom.ria.com'
URL = f'{HOST}/uk/prodazha-kvartir/lvov/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/111.0.0.0 Mobile Safari/537.36'
}

START_PAGE = 1  # 1. Replace Magic Number with Symbolic Constant
END_PAGE = 11  # 1. Replace Magic Number with Symbolic Constant

class Card:  # 2. Replace Data Value with Object
    def __init__(self, price, price_per_m2, street, rooms, m2, floor):
        self.price = price
        self.price_per_m2 = price_per_m2
        self.street = street
        self.rooms = rooms
        self.m2 = m2
        self.floor = floor

class Cards:  # 3. Encapsulate Collection
    def __init__(self):
        self._cards = []

    def add(self, card):
        self._cards.append(card)

    def get_all(self):
        return self._cards

def _get_html(url, params=''):  # 4. Hide Method
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text

def has_floor_info(item):  # 5. Decompose Conditional
    return len(item.find('div', class_='mt-10 chars').find_all('span')) > 2

def create_card(item):  # 6. Extract Method
    price = item.find('b', class_='size22').get_text()
    price_per_m2 = item.find('span', class_='point-before').get_text()
    street = item.find('div', class_='tit').find('a').get_text()
    rooms = item.find('div', class_='mt-10 chars').find_all('span')[0].get_text()
    m2 = item.find('div', class_='mt-10 chars').find_all('span')[1].get_text()
    floor = item.find('div', class_='mt-10 chars').find_all('span')[2].get_text() \
        if has_floor_info(item) else None
    return Card(price, price_per_m2, street, rooms, m2, floor)

def get_content(html):  # 7. Replace Method with Method Object
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='wrap_desc p-rel')
    cards = Cards()

    for item in items:
        card = create_card(item)
        cards.add(card)

    return cards.get_all()

def save_doc(items, path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Ціна', 'Ціна за м^2', 'Вулиця', 'Клк кімнат', 'В метрах квадратних', 'Поверх'])
    for item in items:
        sheet.append([item.price, item.price_per_m2, item.street, item.rooms, item.m2, item.floor])
    workbook.save(filename=path)

cards = []

for page in range(START_PAGE, END_PAGE):  # 1. Replace Magic Number with Symbolic Constant
    url = f'{HOST}/uk/prodazha-kvartir/lvov/?page={page}'
    new_cards = get_content(_get_html(url)) # 8. Inline Temp
    if not new_cards:  # 9. Remove Control Flag
        break
    cards += new_cards
    print(f'Parsed page {page}')

save_doc(cards, EXCEL_FILE)

print('Done')