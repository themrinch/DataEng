import csv
import json
import sqlite3


def load_csv(filename):
    items = list()
    with open(filename, newline='\n', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        reader.__next__()
        for row in reader:
            item = {
                'animal_id': row[0],
                'name': row[1],
                'date_time': row[2],
                'month_year': row[3],
                'found_location': row[4],
                'intake_type': row[5],
                'intake_condition': row[6],
                'animal_type': row[7],
                'sex_upon_intake': row[8],
                'age_upon_intake': row[9],
                'breed': row[10],
                'color': row[11]
            }
            if item['age_upon_intake'] == 'NULL':
                item['age_upon_intake'] = 0
            elif item['age_upon_intake'].split(' ')[1] in ['month', 'months']:
                item['age_upon_intake'] = round((int(item['age_upon_intake'].split()[0]) / 12), 3)
            elif item['age_upon_intake'].split(' ')[1] in ['week', 'weeks']:
                item['age_upon_intake'] = round((int(item['age_upon_intake'].split()[0]) / 52), 3)
            elif item['age_upon_intake'].split(' ')[1] in ['day', 'days']:
                item['age_upon_intake'] = round((int(item['age_upon_intake'].split()[0]) / 365), 3)
            else:
                item['age_upon_intake'] = abs(int(item['age_upon_intake'].split()[0]))

            if item['name'] == '':
                item['name'] = 'not specified'
            items.append(item)
    return items


def load_json(filename):
    with open(filename) as file:
        items = json.load(file)
    return items


def pets_info(intakes, outcomes):
    pets = list()
    pet_id_set = set()
    for item in intakes:
        if item['animal_id'] not in pet_id_set:
            pet_id_set.add(item['animal_id'])
            pet = dict()
            for keys in ['animal_id', 'name', 'animal_type', 'breed', 'color']:
                pet[keys] = item[keys]
            pets.append(pet)
    for item in outcomes:
        if item['animal_id'] not in pet_id_set:
            pet_id_set.add(item['animal_id'])
            pet = dict()
            for keys in ['animal_id', 'name', 'animal_type', 'breed', 'color']:
                pet[keys] = item[keys]
            pets.append(pet)
    return pets


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_shelter_pets_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO shelter_pets (animal_id, name, animal_type, breed, color)
    VALUES(
        :animal_id, :name, :animal_type, :breed, :color
    )
    """, data)
    db.commit()


def insert_intakes_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO intakes (animal_id, date_time, found_location, intake_type, intake_condition,
                         sex_upon_intake, age_upon_intake)
    VALUES(
        :animal_id, :date_time, :found_location, :intake_type, :intake_condition,
        :sex_upon_intake, :age_upon_intake
    )
    """, data)
    db.commit()


def insert_outcomes_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO outcomes (animal_id, date_time, outcome_type, outcome_subtype, 
                         sex_upon_outcome, age_upon_outcome)
    VALUES(
        :animal_id, :date_time, :outcome_type, :outcome_subtype, 
        :sex_upon_outcome, :age_upon_outcome
    )
    """, data)
    db.commit()


# Первые n животных приюта выбранного типа, отсортированных в алфавитном порядке имен
def get_first_query(db, type, limit):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT * 
    FROM shelter_pets 
    WHERE animal_type = ?
    ORDER BY name
    LIMIT ?
    """, [type, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# Sum, Min, Max, Avg, Count по возрасту по типам переселения животных
def get_second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            outcome_type,
            ROUND(SUM(age_upon_outcome), 2) as sum,
            MIN(age_upon_outcome) as min,
            MAX(age_upon_outcome) as max,
            ROUND(AVG(age_upon_outcome), 2) as avg,
            COUNT(*) as count 
        FROM outcomes
        GROUP BY outcome_type
        """)
    stat = list()
    for row in res.fetchall():
        stat.append(dict(row))
    cursor.close()
    return stat


# Частота встречаемости типов приема животных в приют, округленная до 4 знаков после запятой
def get_third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            intake_type,
            ROUND(CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM intakes), 4) as freq
        FROM intakes
        GROUP BY intake_type
        """)
    freq = list()
    for row in res.fetchall():
        freq.append(dict(row))
    cursor.close()
    return freq


# Первые n отфильтрованных по возрасту приема в приют животных заданного типа, отсортированных
# в порядке убывания их возраста приема
def get_fourth_query(db, animal_type, age, limit):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT shelter_pets.animal_id, name, animal_type, intakes.age_upon_intake FROM shelter_pets
    JOIN intakes
    ON intakes.animal_id = shelter_pets.animal_id
    WHERE shelter_pets.animal_type = ? AND intakes.age_upon_intake < ?
    ORDER BY intakes.age_upon_intake DESC
    LIMIT ?
    """, [animal_type, age, limit])
    filtered = list()
    for row in res.fetchall():
        filtered.append(dict(row))
    cursor.close()
    return filtered


# Изменение имени животного из приюта на новое по заданному значению текущего имени
def get_fifth_query(db, old_name, new_name):
    cursor = db.cursor()
    cursor.execute("UPDATE shelter_pets SET name = ? WHERE name = ?", [new_name, old_name])
    res = cursor.execute("SELECT * FROM shelter_pets WHERE name = ?", [new_name])
    db.commit()
    result = dict(res.fetchone())
    cursor.close()
    return result


#Первые n животных приюта выбранных типов приема и переселения, отсортированных по возрасту переселения (в порядке убывания)
def get_sixth_query(db, intake_type, outcome_type, limit):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT name, intakes.intake_type, outcomes.outcome_type, outcomes.age_upon_outcome as age
    FROM shelter_pets
    JOIN intakes
    ON intakes.animal_id = shelter_pets.animal_id
    JOIN outcomes
    ON outcomes.animal_id = shelter_pets.animal_id
    WHERE intakes.intake_type = ? AND outcomes.outcome_type = ?
    ORDER BY age DESC
    LIMIT ?
    """, [intake_type, outcome_type, limit])
    items = list()
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    return items


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


#intakes_data = load_csv('Austin_Animal_Center_Intakes.csv')
#outcomes_data = load_json('Austin_Animal_Center_Outcomes.json')
#shelter_pets = pets_info(intakes_data, outcomes_data)

db = connect_to_db('task-5.db')

#insert_shelter_pets_data(db, shelter_pets)
#insert_intakes_data(db, intakes_data)
#insert_outcomes_data(db, outcomes_data)

first_query = get_first_query(db, 'Cat', 33)
second_query = get_second_query(db)
third_query = get_third_query(db)
fourth_query = get_fourth_query(db, 'Cat', 25, 33)
fifth_query = get_fifth_query(db, 'Sixlet', 'Zizi')
sixth_query = get_sixth_query(db, 'Stray', 'Adoption', 33)


write_json('res/res_first_query.json', first_query)
write_json('res/res_second_query.json', second_query)
write_json('res/res_third_query.json', third_query)
write_json('res/res_fourth_query.json', fourth_query)
write_json('res/res_fifth_query.json', fifth_query)
write_json('res/res_sixth_query.json', sixth_query)
