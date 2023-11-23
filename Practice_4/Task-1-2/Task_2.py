import msgpack
import json
import sqlite3


def parse_data(file_name):
    with open(file_name, 'rb') as f:
        items = msgpack.load(f)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO awards (game_id, place, prise)
    VALUES(
        (SELECT id FROM games WHERE name = :name),
        :place, :prise
    )
    """, data)
    db.commit()


# Все награды по заданному названию игры, отсортированные по местам (в порядке возрастания)
def get_first_query(db, name):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT * 
    FROM awards 
    WHERE game_id = (SELECT id FROM games WHERE name = ?)
    ORDER BY place
    """, [name])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# Количество наград в каждой игре, отсортированные в порядке возрастания
def get_second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT 
        name,
        (SELECT COUNT(*) FROM awards WHERE game_id = games.id) as award_count
    FROM games
    ORDER BY award_count
    """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# Средний выигрыш по каждой игре, округленный до 2 знаков после запятой, в порядке убывания
def get_third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT 
        name,
        (SELECT ROUND(AVG(prise),2) FROM awards WHERE game_id = games.id) as avg_prise
    FROM games
    ORDER BY avg_prise DESC
    """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


#items = parse_data('task_2_var_33_subitem.msgpack')
db = connect_to_db('task-1.db')
#insert_data(db, items)

first_query = get_first_query(db, 'Вейк-ан-Зее 1993')

with open('res-2/res_first_query.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(first_query, ensure_ascii=False))

second_query = get_second_query(db)

with open('res-2/res_second_query.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(second_query, ensure_ascii=False))

third_query = get_third_query(db)
with open('res-2/res_third_query.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(third_query, ensure_ascii=False))

