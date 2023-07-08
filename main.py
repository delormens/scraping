import csv
import json
import requests
from bs4 import BeautifulSoup

url1 = input('URL: ') # https://vkusnoitochka.ru/
print("~~~~~~~~Site Settings~~~~~~~~") # ПРИМЕРЫ НИЖЕ
divcl = input('div Class: ') # catalog-product
divcl = input('Title: ') # catalog-product-title
divcl = input('Price: ') # catalog-product__price
divcl = input('Imgae: ') # catalog-product__image


def tag_check(product):
    try:
        tag = product.find('div', class_='tag').text.strip()
        return tag
    except AttributeError:
        return ''

with open('save.csv', 'w', newline='', encoding='utf-8') as csvfile, \
        open('save.json', 'w', encoding='utf-8') as jsonfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    table_head = ['Название', 'Цена', 'Фото']
    csv_writer.writerow(table_head)

    url = f'{url1}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_=f'{divcl}')

    for product in products:
        name_product = product.find('div', class_=f'catalog-product-title').text.strip()
        price_product = product.find('p', class_=f'catalog-product__price').text.replace('P', '').replace('от', '').strip()
        photo_product = url + product.find('img', class_=f'catalog-product__image').get('src')

        csv_writer.writerow([name_product, price_product, photo_product])

    product_data = []
    for product in products:
        name_product = product.find('div', class_='catalog-product-title').text.strip()
        price_product = product.find('p', class_='catalog-product__price').text.replace('P', '').replace('от', '').strip()
        photo_product = url + product.find('img', class_='catalog-product__image').get('src')

        product_data.append({
            'Название': name_product,
            'Цена': price_product,
            'Фото': photo_product
                })

    json.dump(product_data, jsonfile, indent=4, ensure_ascii=False)

print("The data has been successfully written to the save.csv and save.json files.")
