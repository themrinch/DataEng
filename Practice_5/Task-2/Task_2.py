import pickle
from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.person


def get_from_pkl(filename):
    with open(filename, 'rb') as f:
        items = pickle.load(f)
    return items


def insert_many(collection, data):
    collection.insert_many(data)


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


def get_stat_by_salary(collection):
    q = [
        {
            '$group': {
                '_id': 'result',
                'max': {'$max': '$salary'},
                'min': {'$min': '$salary'},
                'avg': {'$avg': '$salary'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('res/res_stat_by_salary.json', items)


def get_freq_by_job(collection):
    q = [
        {
            '$group': {
                '_id': '$job',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        }
    ]
    items = collection.aggregate(q)
    write_json('res/res_freq_by_job.json', items)


def get_column_stat_by_column(collection, by_column_name, stat_column_name):
    q = [
        {
            '$group': {
                '_id': f'${by_column_name}',
                'max': {'$max': f'${stat_column_name}'},
                'min': {'$min': f'${stat_column_name}'},
                'avg': {'$avg': f'${stat_column_name}'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json(f'res/res_{stat_column_name}_stat_by_{by_column_name}.json', items)


def max_salary_by_min_age(collection):
    q = [
        {
            '$sort': {
                'age': 1,
                'salary': -1
            }
        },
        {
            '$limit': 1
        }
    ]
    items = collection.find(q)
    write_json('res/res_max_salary_by_min_age.json', items)


def min_salary_by_max_age(collection):
    q = [
        {
            '$sort': {
                'salary': 1,
                'age': -1
            }
        },
        {
            '$limit': 1
        }
    ]
    items = collection.find(q)
    write_json('res/res_min_salary_by_max_age.json', items)


def big_query(collection):
    q = [
        {
            '$match': {'salary': {'$gt': 50_000}}
        },
        {
            '$group': {
                '_id': '$city',
                'max': {'$max': '$age'},
                'min': {'$min': '$age'},
                'avg': {'$avg': '$age'}
            }
        },
        {
            '$sort': {'avg': -1}
        }
    ]
    items = collection.aggregate(q)
    write_json('res/res_big_query.json', items)


def big_query_2(collection):
    q = [
        {
            '$match': {
                'city': {'$in': ['Москва', 'Астана', 'София']},
                'job': {'$in': ['Врач', 'Строитель', 'Продавец']},
                '$or': [
                    {'age': {'$gt': 18, '$lt': 25}},
                    {'age': {'$gt': 50, '$lt': 65}}
                ]
            }
        },
        {
            '$group': {
                '_id': 'result',
                'max': {'$max': '$salary'},
                'min': {'$min': '$salary'},
                'avg': {'$avg': '$salary'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('res/res_big_query_2.json', items)


# Вывод минимального, максимального и среднего возраста по году в заданных диапазонах по городу, профессии и
# зарплате ((25 000 <= s <= 50 000) || (100 000 < s < 150 000)), отсортированных в порядке убывания среднего возраста
def my_query(collection):
    q = [
        {
            '$match': {
                'city': {'$in': ['Москва', 'Хихон', 'София']},
                'job': {'$in': ['Врач', 'Строитель', 'Продавец']},
                '$or': [
                    {'salary': {'$gte': 25_000, '$lte': 50_000}},
                    {'salary': {'$gt': 100_000, '$lt': 150_000}}
                ]
            }
        },
        {
            '$group': {
                '_id': '$city',
                'max': {'$max': '$age'},
                'min': {'$min': '$age'},
                'avg': {'$avg': '$age'}
            }
        },
        {
            '$sort': {'avg': -1}
        }
    ]
    items = collection.aggregate(q)
    write_json('res/res_my_query.json', items)


#data = get_from_pkl('task_2_item.pkl')
#insert_many(connect(), data)

get_stat_by_salary(connect())
get_freq_by_job(connect())
get_column_stat_by_column(connect(), 'city', 'salary')
get_column_stat_by_column(connect(), 'job', 'salary')
get_column_stat_by_column(connect(), 'city', 'age')
get_column_stat_by_column(connect(), 'job', 'age')
max_salary_by_min_age(connect())
min_salary_by_max_age(connect())
big_query(connect())
big_query_2(connect())
my_query(connect())
