from bs4 import BeautifulSoup
import lxml
import json
import Practice_3.statistic as st


def handle_file(file_name):
    item = dict()
    with open(file_name, encoding='utf-8') as f:
        file = f.read()

        soup = BeautifulSoup(file, 'xml')

        item['name'] = soup.find_all('name')[0].get_text().strip()
        item['constellation'] = soup.find_all('constellation')[0].get_text().strip()
        item['spectral-class'] = soup.find_all('spectral-class')[0].get_text().strip()
        item['radius'] = int(soup.find_all('radius')[0].get_text().strip())
        item['rotation'] = float(soup.find_all('rotation')[0].get_text().replace('days', '').strip())
        item['age'] = float(soup.find_all('age')[0].get_text().replace('billion years', '').strip())
        item['distance'] = float(soup.find_all('distance')[0].get_text().replace('million km', '').strip())
        item['absolute-magnitude'] = float(soup.find_all('absolute-magnitude')[0].get_text().replace('million km', '').strip())
        return item


items = []
for i in range(1, 501):
    items.append(handle_file(f'var_33/{i}.xml'))

with open('raw_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

items = sorted(items, key=lambda x: x['radius'], reverse=True)

with open('result_sorted.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

filtered_items = list(filter(lambda x:  x['age'] > 3, items))

with open('result_filtered.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_items))

selected_items = st.select_data(items, 'rotation', 'constellation')

number_stat = st.num_stat(selected_items[0])

with open('num_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(number_stat))

word_stat = st.word_stat(selected_items[1], selected_items[2])

with open('words_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(word_stat))
