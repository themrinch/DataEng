import csv
import json
import sqlite3


def load_data_text(file_name):
    items = list()
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == '=====\n':
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split('::')
                if splitted[0] in ['duration_ms', 'year']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] in ['tempo', 'loudness']:
                    item[splitted[0]] = float(splitted[1])
                elif splitted[0] in ['instrumentalness', 'explicit']:
                    continue
                else:
                    item[splitted[0]] = splitted[1]
    return items


def load_data_csv(file_name):
    items = list()
    with open(file_name, newline='\n', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        fields = next(reader)
        for row in reader:
            item = {
                'artist': row[0],
                'song': row[1],
                'duration_ms': int(row[2]),
                'year': int(row[3]),
                'tempo': float(row[4]),
                'genre': row[5],
                'loudness': float(row[8])
            }
            items.append(item)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, loudness)
    VALUES(
        :artist, :song, :duration_ms, :year, :tempo, :genre, :loudness
    )
    """, data)
    db.commit()


def get_top_by_tempo(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM songs ORDER BY tempo DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def get_stat_by_loudness(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(loudness) as sum,
            MIN(loudness) as min,
            MAX(loudness) as max,
            AVG(loudness) as avg 
        FROM songs
        """)
    stat = dict(res.fetchone())
    cursor.close()
    return stat


def get_freq_by_artist(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            artist,
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM songs) as freq
        FROM songs
        GROUP BY artist
        """)
    freq = list()
    for row in res.fetchall():
        freq.append(dict(row))
    cursor.close()
    return freq


def filter_by_year(db, min_year, limit):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        WHERE year > ?
        ORDER BY duration_ms DESC
        LIMIT ?
        """, [min_year, limit])
    filtered = list()
    for row in res.fetchall():
        filtered.append(dict(row))
    cursor.close()
    return filtered


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


#items = load_data_text('task_3_var_33_part_1.text') + load_data_csv('task_3_var_33_part_2.csv')
db = connect_to_db('task-3.db')
#insert_data(db, items)

top_by_tempo = get_top_by_tempo(db, 43)
stat_by_loudness = get_stat_by_loudness(db)
freq_by_artist = get_freq_by_artist(db)
filtered_by_year = filter_by_year(db, 2010, 48)

write_json('res/res_top_by_tempo.json', top_by_tempo)
write_json('res/res_stat_by_loudness.json', stat_by_loudness)
write_json('res/res_freq_by_artist.json', freq_by_artist)
write_json('res/res_filtered_by_year.json', filtered_by_year)
