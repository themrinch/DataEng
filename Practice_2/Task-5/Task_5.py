import csv
import json
import msgpack
import pickle
import os
import numpy as np

items = list()
dataset = list()

filename = 'PS_2023.11.05_08.34.37.csv'
with open(filename, newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    fields = next(reader)
    for row in reader:
        item = {
            'PlanetName': row[0],
            'NumberOfStars': int(row[3]),
            'NumberOfPlanets': int(row[4]),
            'DiscoveryMethod': row[5],
            'DiscoveryYear': int(row[6]),
            'DiscoveryFacility': row[7],
            'SolutionType': row[8]
        }
        items.append(item)
        dataset.append(row)

length = len(items)

numbers_stat = dict()
for elem in ['NumberOfStars', 'NumberOfPlanets', 'DiscoveryYear']:
    numbers_stat[elem] = list()

word_stat = dict()
for elem in ['DiscoveryMethod', 'DiscoveryFacility', 'SolutionType']:
    word_stat[elem] = dict()

for elem in items:
    for item in numbers_stat:
        numbers_stat[item].append(elem[item])
    for item in word_stat:
        if elem[item] in word_stat[item].keys():
            word_stat[item][elem[item]] += 1
        else:
            word_stat[item][elem[item]] = 1

result = list()

for elem in numbers_stat:
    numbers_stat[elem] = {
        'max': float(np.max(numbers_stat[elem])),
        'min': float(np.min(numbers_stat[elem])),
        'avg': float(np.mean(numbers_stat[elem])),
        'sum': float(np.sum(numbers_stat[elem])),
        'std': float(np.std(numbers_stat[elem]))
    }
result.append(numbers_stat)

for elem in word_stat:
    word_stat[elem] = dict(sorted(word_stat[elem].items(), reverse=True, key=lambda item: item[1]))
    for item in word_stat[elem]:
        word_stat[elem][item] = str(round(((word_stat[elem][item] / length) * 100), 2)) + '%'

result.append(word_stat)

with open('result.json', 'w') as stat_json:
    stat_json.write(json.dumps(result))


with open('json_task_5_data.json', 'w') as d_json:
    d_json.write(json.dumps(dataset))

with open('msgpack_task_5_data.msgpack', 'wb') as d_msgpack:
    d_msgpack.write(msgpack.dumps(dataset))

with open('pkl_task_5_data.pkl', 'wb') as d_pkl:
    d_pkl.write(pickle.dumps(dataset))

print(f"csv_data_size         = {os.path.getsize(filename)}")
print(f"msgpack_data_size     = {os.path.getsize('msgpack_task_5_data.msgpack')}")
print(f"pkl_data_size         = {os.path.getsize('pkl_task_5_data.pkl')}")
print(f"json_data_size        = {os.path.getsize('json_task_5_data.json')}")

