from bs4 import BeautifulSoup
import json
import Practice_3.statistic as st


def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all('div', attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
            item['bonus'] = int(product.strong.get_text().replace('+ начислим', '').replace(' бонусов', '').strip())

            props = product.ul.find_all('li')
            for prop in props:
                item[prop['type']] = prop.get_text().strip()
            items.append(item)
    return items


items = []
for i in range(1, 58):
    items += handle_file(f'var_33/{i}.html')

with open('raw_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open('result_sorted.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

filtered_items = list(filter(lambda x:  x['bonus'] > 3000, items))

with open('result_filtered.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_items))

selected_items = st.select_data(items, 'price', 'title')

number_stat = st.num_stat(selected_items[0])

with open('num_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(number_stat))

word_stat = st.word_stat(selected_items[1], selected_items[2])

with open('words_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(word_stat))
