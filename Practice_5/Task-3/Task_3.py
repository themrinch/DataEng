import msgpack
from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.person


def get_from_msgpack(filename):
    with open(filename, 'rb') as f:
        items = msgpack.load(f)
    return items


def insert_many(collection, data):
    collection.insert_many(data)


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


def delete_by_salary(collection):
    result = collection.delete_many({
        '$or': [
            {'salary': {'$lt': 25_000}},
            {'salary': {'$gt': 175_000}},
        ]
    })
    write_json('res/res_delete_by_salary.json', {'deleted_count': result.deleted_count})


def update_age(collection):
    result = collection.update_many({}, {
        '$inc': {'age': 1}
    })
    write_json('res/res_update_age.json', {'modified_count': result.modified_count})


def increase_salary_by_job(collection):
    filter = {
        'job': {'$in': ['Врач', 'Строитель', 'Продавец']}
    }
    update = {
        '$mul': {
            'salary': 1.05
        }
    }
    result = collection.update_many(filter, update)
    write_json('res/res_increase_salary_by_job.json', {'modified_count': result.modified_count})


def increase_salary_by_city(collection):
    filter = {
        'city': {'$nin': ['Москва', 'Хихон', 'София']}
    }
    update = {
        '$mul': {
            'salary': 1.07
        }
    }
    result = collection.update_many(filter, update)
    write_json('res/res_increase_salary_by_city.json', {'modified_count': result.modified_count})


def increase_salary_complex_query(collection):
    filter = {
        'city': 'Москва',
        'job': {'$in': ['Врач', 'Строитель', 'Продавец']},
        '$or': [
            {'age': {'$gt': 18, '$lt': 25}},
            {'age': {'$gt': 50, '$lt': 65}}
        ]
    }
    update = {
        '$mul': {
            'salary': 1.1
        }
    }
    result = collection.update_many(filter, update)
    write_json('res/res_increase_salary_complex_query.json', {'modified_count': result.modified_count})


#Удаление из коллекции документов по предикату: year < 2010 || year > 2020
def delete_by_year(collection):
    result = collection.delete_many({
        '$or': [
            {'year': {'$lt': 2010}},
            {'year': {'$gt': 2020}},
        ]
    })
    write_json('res/res_delete_by_year.json', {'deleted_count': result.deleted_count})


#data = get_from_msgpack('task_3_item.msgpack')
#insert_many(connect(), data)

delete_by_salary(connect())
update_age(connect())
increase_salary_by_job(connect())
increase_salary_by_city(connect())
increase_salary_complex_query(connect())
delete_by_year(connect())
