from pymongo import MongoClient
from bson import json_util


def connect():
    client = MongoClient()
    db = client['practice-5-database']
    return db.meteorite_landings


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))


# Вывод min, max, avg mass(g)
def get_stat_by_mass(collection):
    q = [
        {
            '$group': {
                '_id': 'result',
                'min': {'$min': '$mass(g)'},
                'max': {'$max': '$mass(g)'},
                'avg': {'$avg': '$mass(g)'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('res-aggregation/res_stat_by_mass.json', items)


# Вывод количества данных по представленным типам метеоритов, отсортированных в порядке убывания количества данных
def get_freq_by_recclass(collection):
    q = [
        {
            '$group': {
                '_id': '$recclass',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        }
    ]
    items = collection.aggregate(q)
    write_json('res-aggregation/res_freq_by_recclass.json', items)


# Вывод min, avg, max mass(g) по типу метеоритов, отсортированные в порядке возрастания avg
def get_column_stat_by_column(collection, by_column_name, stat_column_name):
    q = [
        {
            '$group': {
                '_id': f'${by_column_name}',
                'max': {'$max': f'${stat_column_name}'},
                'min': {'$min': f'${stat_column_name}'},
                'avg': {'$avg': f'${stat_column_name}'}
            }
        },
        {
            '$sort': {'avg': 1}
        }
    ]
    items = collection.aggregate(q)
    write_json(f'res-aggregation/res_{stat_column_name}_stat_by_{by_column_name}.json', items)


# Вывод максимального значения массы при минимальном значении года
def max_mass_by_min_year(collection):
    q = [
        {
            '$group': {
                '_id': '$year',
                'max_mass(g)': {'$max': '$mass(g)'}
            }
        },
        {
            '$group': {
                '_id': 'result',
                'min_year': {'$min': '$_id'},
                'max_mass(g)': {'$max': '$max_mass(g)'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('res-aggregation/res_max_mass_by_min_year.json', items)


# Вывод min, avg, max mass(g) в произвольно заданных диапазонах по году и типу, а также
# по произвольно заданному статусу нахождения места падения
def big_query(collection):
    q = [
        {
            '$match': {
                'fall': 'Found',
                'recclass': {'$in': ['L6', 'H5', 'H6']},
                '$or': [
                    {'year': {'$gt': 1950, '$lt': 2000}},
                    {'year': {'$gt': 2010, '$lt': 2020}}
                ]
            }
        },
        {
            '$group': {
                '_id': 'result',
                'max': {'$max': '$mass(g)'},
                'min': {'$min': '$mass(g)'},
                'avg': {'$avg': '$mass(g)'}
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('res-aggregation/res_big_query.json', items)


get_stat_by_mass(connect())
get_freq_by_recclass(connect())
get_column_stat_by_column(connect(), 'recclass', 'mass(g)')
max_mass_by_min_year(connect())
big_query(connect())


