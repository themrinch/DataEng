from bs4 import BeautifulSoup
import json
import Practice_3.statistic as st


def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as f:
        file = f.read()

        soup = BeautifulSoup(file, 'xml')
        clothes = soup.find_all('clothing')
        for cloth in clothes:
            item = dict()
            for elem in cloth:
                if elem.name is None:
                    continue
                elif elem.name == 'price' or elem.name == 'reviews':
                    item[elem.name] = int(elem.get_text().strip())
                elif elem.name == 'rating':
                    item[elem.name] = float(elem.get_text().strip())
                elif elem.name == 'new':
                    item[elem.name] = elem.get_text().strip() == '+'
                elif elem.name == 'exclusive' or elem.name == 'sporty':
                    item[elem.name] = elem.get_text().strip() == 'yes'
                else:
                    item[elem.name] = elem.get_text().strip()
            items.append(item)
    return items


items = []
for i in range(1, 101):
    items += handle_file(f'var_33/{i}.xml')


with open('raw_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open('result_sorted.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

filtered_items = list(filter(lambda x:  x['material'] != 'Хлопок', items))

with open('result_filtered.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_items))

selected_items = st.select_data(items, 'rating', 'category')

number_stat = st.num_stat(selected_items[0])

with open('num_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(number_stat))

word_stat = st.word_stat(selected_items[1], selected_items[2])

with open('words_stat_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(word_stat))
