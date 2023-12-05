from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.meteorite_landings


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


# Удаление из коллекции документов по предикату: year < 1900 || year > 2020
def delete_by_year(collection):
    result = collection.delete_many({
        '$or': [
            {'year': {'$lt': 1900}},
            {'year': {'$gt': 2020}},
        ]
    })
    write_json('res-update-delete/res_delete_by_year.json', {'deleted_count': result.deleted_count})


# Увеличить год (year) во всех документах на 1
def update_year(collection):
    result = collection.update_many({}, {
        '$inc': {'year': 1}
    })
    write_json('res-update-delete/res_update_year.json', {'modified_count': result.modified_count})


# Увеличить массу на 2% для произвольно выбранных типов метеоритов
def increase_mass_by_recclass(collection):
    filter = {
        'recclass': {'$in': ['L6', 'H5', 'H6']}
    }
    update = {
        '$mul': {
            'mass(g)': 1.02
        }
    }
    result = collection.update_many(filter, update)
    write_json('res-update-delete/res_increase_mass_by_recclass.json', {'modified_count': result.modified_count})


# Изменить статус нахождения места падения для произвольно выбранных типов метеоритов
def set_fall_by_recclass(collection):
    filter = {
        'recclass': {'$nin': ['L6', 'H5', 'H6']},
        'fall': {'$ne': 'Found'}
    }
    update = {
        '$set': {
            'fall': 'Found'
        }
    }
    result = collection.update_many(filter, update)
    write_json('res-update-delete/res_set_fall_by_recclass.json', {'modified_count': result.modified_count})


# Изменить статус нахождения места падения метеорита для выборки по сложному предикату
# (произвольный набор типов метеоритов, год (year) и масса (mass(g)) в произвольно заданных диапазонах)
def set_fall_by_complex_query(collection):
    filter = {
        'recclass': {'$in': ['L6', 'H5', 'H6']},
        'mass(g)': {'$gt': 1_000},
        '$or': [
            {'year': {'$gte': 1900, '$lte': 1950}},
            {'year': {'$gte': 2005, '$lte': 2015}}
        ],
        'fall': {'$ne': 'Found'}
    }
    update = {
        '$set': {
            'fall': 'Found'
        }
    }
    result = collection.update_many(filter, update)
    write_json('res-update-delete/res_set_fall_by_complex_query.json', {'modified_count': result.modified_count})


delete_by_year(connect())
update_year(connect())
increase_mass_by_recclass(connect())
set_fall_by_recclass(connect())
set_fall_by_complex_query(connect())

