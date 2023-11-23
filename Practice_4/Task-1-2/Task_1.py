import pickle
import json
import sqlite3


def parse_data(file_name):
    with open(file_name, 'rb') as f:
        items = pickle.load(f)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO games (name, city, begin, system, tours_count, min_rating, time_on_game)
    VALUES(
        :name, :city, :begin, :system,
        :tours_count, :min_rating, :time_on_game
    )
    """, data)
    db.commit()


def get_top_by_min_rating(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM games ORDER BY min_rating DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def get_stat_by_tours_count(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(tours_count) as sum,
            AVG(tours_count) as avg,
            MIN(tours_count) as min,
            MAX(tours_count) as max 
        FROM games
        """)
    stat = dict(res.fetchone())
    cursor.close()
    return stat


def get_freq_by_system(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            system,
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM games) as freq
        FROM games
        GROUP BY system
        """)
    freq = list()
    for row in res.fetchall():
        freq.append(dict(row))
    cursor.close()
    return freq


def filter_by_time_on_game(db, min_time_on_game, limit):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM games
        WHERE time_on_game > ?
        ORDER BY tours_count DESC
        LIMIT ?
        """, [min_time_on_game, limit])
    filtered = list()
    for row in res.fetchall():
        filtered.append(dict(row))
    cursor.close()
    return filtered


#items = parse_data('task_1_var_33_item.pkl')

db = connect_to_db('task-1.db')

#insert_data(db, items)

top_by_min_rating = get_top_by_min_rating(db, 43)

with open('res-1/res_top_by_min_rating.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(top_by_min_rating, ensure_ascii=False))

stat_by_tours_count = get_stat_by_tours_count(db)

with open('res-1/res_stat_by_tours_count.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(stat_by_tours_count))

freq_by_system = get_freq_by_system(db)

with open('res-1/res_freq_by_system.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(freq_by_system, ensure_ascii=False))

filtered_by_time_on_game = filter_by_time_on_game(db, 100, 43)

with open('res-1/res_filtered_by_time_on_game.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_by_time_on_game, ensure_ascii=False))

