# Центр помощи кошкам "Муркоша"
# https://murkosha.ru/

from bs4 import BeautifulSoup
import json
import Practice_3.statistic as st


def handle_file_objects(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        soup = site.find_all('li', attrs={'class': 'pet-full__item'})
        keys = ['name', 'age', 'sex', 'color', 'fur', 'claw', 'tray', 'have_parasites',
                'vaccinated', 'chipped', 'strilized', 'passport', 'free', 'img', 'vid']
        values = ['Приучен к когтеточке', 'Знает лоточек', 'Обработан от паразитов', 'Вакцинирован',
                  'Чипирован', 'Стерилизован', 'Есть ветпаспорт', 'Бесплатно']
        item = dict()
        image = site.find_all('a', attrs={'class': 'colorbox'})
        for i in range(len(keys)):
            if i == 0:
                item[keys[i]] = site.find('span', attrs={'class': 'field field--name-title field--type-string field--label-hidden'}).get_text().strip()
            elif i == 1:
                item[keys[i]] = int(soup[i - 1].span.get_text().split(' ')[0].strip())
            elif i in [5, 6, 8, 9, 10, 11, 12]:
                item[keys[i]] = soup[i - 1].get_text().strip() in values
            elif i == 7:
                item[keys[i]] = not (soup[i - 1].get_text().strip() in values)
            elif i == 13:
                item[keys[i]] = list()
                for j in range(len(image)):
                    item['img'].append(image[j]['href'])
            elif i == 14:
                try:
                    item[keys[i]] = site.iframe['src']
                except TypeError:
                    item[keys[i]] = 'No video'
            else:
                item[keys[i]] = soup[i - 1].span.get_text().strip()
        return item


def handle_file_cat(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        soup = site.find_all('div', attrs={'class': 'pets__cell'})
        items = list()
        for elem in soup:
            item = dict()
            title = list(elem.h3.strings)
            item['preview_name'] = title[0].strip()
            if title[1].split()[1] in ['месяц', 'месяца', 'месяцев']:
                item['preview_age'] = round((int(title[1].split()[0]) / 12), 1)
            else:
                item['preview_age'] = int(title[1].split()[0])
            item['url'] = elem.a['href']
            item['preview_img'] = elem.img['data-savepage-src']
            items.append(item)
        return items


items_obj = []
items_cat = []
for i in range(1, 13):
    items_obj.append(handle_file_objects(f'objects/{i}.html'))
    items_cat += handle_file_cat(f'catalogue/{i}.html')

with open('raw_data_obj.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items_obj))

with open('raw_data_cat.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items_cat))

items_obj = sorted(items_obj, key=lambda x: x['age'], reverse=True)

with open('result_sorted_obj.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items_obj))

filtered_items = list(filter(lambda x:  x['sex'] != 'Кот', items_obj))

with open('result_filtered_obj.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_items))

selected_items = st.select_data(items_obj, 'age', 'color')

number_stat = st.num_stat(selected_items[0])

with open('num_stat_result_obj.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(number_stat))

word_stat = st.word_stat(selected_items[1], selected_items[2])

with open('words_stat_result_obj.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(word_stat))
