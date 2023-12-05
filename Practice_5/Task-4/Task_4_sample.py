import json
import pickle
from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.meteorite_landings


def get_from_pkl(filename):
    with open(filename, 'rb') as f:
        items = pickle.load(f)
    return items


def get_from_json(filename):
    with open(filename, 'r') as f:
        items = json.load(f)
    return items


def insert_many(collection, data):
    collection.insert_many(data)


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


# Вывод первых 33 записей, отсортированных по убыванию по полю mass(g)
def sort_by_mass(collection):
    items = collection.find(limit=33).sort({'mass(g)': -1})
    write_json('res-sample/res_sort_by_mass.json', items)


# Вывод первых 33 записей, отфильтрованных по предикату year < 2000, отсортированных по убыванию по полю mass(g)
def filter_by_year(collection):
    items = collection.find({'year': {'$lt': 2000}}, limit=33).sort({'mass(g)': -1})
    write_json('res-sample/res_filter_by_year.json', items)


# Вывод первых 33 записей, отфильтрованных по предикату:
# 10 000 <= mass(g) <= 50 000 || 100 000 < mass(g) < 200 000
# отсортированных по убыванию по полю year
def filter_by_mass(collection):
    items = collection.find({
        '$or': [
                {'mass(g)': {'$gte': 10_000, '$lte': 50_000}},
                {'mass(g)': {'$gt': 100_000, '$lt': 200_000}}
            ]
    }, limit=33).sort({'year': -1})
    write_json('res-sample/res_filter_by_mass.json', items)


# Вывод первых 33 записей, отфильтрованных по сложному предикату (записи только найденным местом падения метеорита,
# записи только из трех произвольно взятых типов метеоритов), отсортированных по возрастанию поля year
def complex_filter_by_fall_and_recclass(collection):
    items = collection.find({'fall': 'Found',
                             'recclass': {'$in': ['CM2', 'L6', 'H6']}},
                            limit=33).sort({'year': 1})
    write_json('res-sample/res_complex_filter_by_fall_and_recclass.json', items)


# Вывод количества записей, получаемых в результате следующей фильтрации:
# - year в произвольном диапазоне
# - recclas в ['CM2', 'L6', 'H6']
# - 10 000 <= mass(g) <= 50 000 || 100 000 < mass(g) < 200 000
def count_obj(collection):
    result = collection.count_documents({
            'year': {'$gte': 2000, '$lte': 2023},
            'recclass': {'$in': ['CM2', 'L6', 'H6']},
            '$or': [
                {'mass(g)': {'$gte': 10_000, '$lte': 50_000}},
                {'mass(g)': {'$gt': 100_000, '$lt': 200_000}}
            ]
    })
    write_json('res-sample/res_count_obj.json', result)


#data = get_from_pkl('Meteorite_Landings.pkl') + get_from_json('Meteorite_Landings.json')
#insert_many(connect(), data)

sort_by_mass(connect())
filter_by_year(connect())
filter_by_mass(connect())
complex_filter_by_fall_and_recclass(connect())
count_obj(connect())
