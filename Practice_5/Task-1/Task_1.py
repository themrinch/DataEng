from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.person


def get_from_text(filename):
    items = list()
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == '=====\n':
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split('::')
                if splitted[0] in ['id', 'year', 'age']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'salary':
                    item[splitted[0]] = float(splitted[1])
                else:
                    item[splitted[0]] = splitted[1]
    return items


def insert_many(collection, data):
    collection.insert_many(data)


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


def sort_by_salary(collection):
    items = collection.find(limit=10).sort({'salary': -1})
    write_json('res/res_sort_by_salary.json', items)


def filter_by_age(collection):
    items = collection.find({'age': {'$lt': 30}}, limit=15).sort({'salary': -1})
    write_json('res/res_filter_by_age.json', items)


def complex_filter_by_city_and_job(collection):
    items = collection.find({'city': 'Москва',
                            'job': {'$in': ['Повар', 'Учитель', 'Менеджер']}},
                            limit=10).sort({'age': 1})
    write_json('res/res_complex_filter_by_city_and_job.json', items)


def count_obj(collection):
    result = collection.count_documents({
            'age': {'$gt': 20, '$lt': 30},
            'year': {'$gte': 2019, '$lte': 2022},
            '$or': [
                {'salary': {'$gt': 50000, '$lte': 75000}},
                {'salary': {'$gt': 125000, '$lt': 150000}}
            ]
    })
    write_json('res/res_count_obj.json', result)


#data = get_from_text('task_1_item.text')
#insert_many(connect(), data)

sort_by_salary(connect())
filter_by_age(connect())
complex_filter_by_city_and_job(connect())
count_obj(connect())

