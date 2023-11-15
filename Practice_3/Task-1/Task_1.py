from bs4 import BeautifulSoup
import re
import json
import Practice_3.statistic as st


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        pads = site.find_all('div')

        item = dict()

        genre_raw = site.html.body.div.div.span.get_text()
        item['genre'] = genre_raw.strip().split(':')[1].strip()
        item['title'] = site.find_all('h1')[0].get_text().strip()
        item['author'] = site.find_all('p')[0].get_text().strip()
        item['pages'] = int(site.find_all('span', attrs={'class': 'pages'})[0].get_text().split(':')[1].replace(' страниц', '').strip())
        item['year'] = int(site.find_all('span', attrs={'class': 'year'})[0].get_text().replace('Издано в', '').strip())
        item['isbn'] = site.find_all('span', string=re.compile('ISBN:'))[0].get_text().split(':')[1].strip()
        item['description'] = site.find_all('p')[1].get_text().replace('Описание', '').strip()
        item['img_url'] = site.find_all('img')[0]['src']
        item['rating'] = float(site.find_all('span', string=re.compile('Рейтинг:'))[0].get_text().split(':')[1].strip())
        item['views'] = int(site.find_all('span', string=re.compile('Просмотры:'))[0].get_text().split(':')[1].strip())

        return item


items = []
for i in range(1, 1000):
    items.append(handle_file(f'var_33/{i}.html'))

with open('raw_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

items = sorted(items, key=lambda x: x['views'], reverse=True)

with open('result_sorted.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

filtered_items = list(filter(lambda x:  x['genre'] != 'любовный роман', items))

with open('result_filtered.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_items))

selected_items = st.select_data(items, 'rating', 'genre')

number_stat = st.num_stat(selected_items[0])

with open('num_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(number_stat))

word_stat = st.word_stat(selected_items[1], selected_items[2])

with open('words_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(word_stat))
