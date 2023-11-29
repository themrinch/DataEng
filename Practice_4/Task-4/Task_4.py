import pickle
import json
import sqlite3


def load_data(file_name):
    with open(file_name, 'rb') as f:
        items = pickle.load(f)
    name_set = set()
    unique_items = list()
    for item in items:
        if 'category' not in item.keys():
            item['category'] = 'not specified'
        if item['name'] not in name_set:
            name_set.add(item['name'])
            unique_items.append(item)
    return unique_items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
    VALUES(
        :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
    )
    """, data)
    db.commit()


def load_update_data(file_name):
    items = list()
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == '=====\n':
                if item['method'] == 'available':
                    item['param'] = item['param'] == 'True'
                elif item['method'] != 'remove':
                    item['param'] = float(item['param'])
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split('::')
                item[splitted[0]] = splitted[1]
    return items


def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE name = ?", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET price = ROUND((price * (1 + ?)),2) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE products SET price = ROUND((price + ?), 2) WHERE (name = ?) AND ((price + ?) > 0)", [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                print(f'deleting {item["name"]}')
                delete_by_name(db, item['name'])
            case 'price_percent':
                print(f'update price {item["name"]} {item["param"]} %')
                update_price_by_percent(db, item['name'], item['param'])
            case 'price_abs':
                print(f'update price {item["name"]} {item["param"]}')
                update_price(db, item['name'], item['param'])
            case 'available':
                print(f'update available {item["name"]} {item["param"]}')
                update_available(db, item['name'], item['param'])
            case 'quantity_add':
                print(f'update quantity {item["name"]} {item["param"]}')
                update_quantity(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f'update quantity {item["name"]} {item["param"]}')
                update_quantity(db, item['name'], item['param'])
            case _:
                print(f'unknown method {item["method"]}')


def get_top_by_version(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM products ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def get_stat_by_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(price) as sum,
            MIN(price) as min,
            MAX(price) as max,
            AVG(price) as avg,
            COUNT(*) as count 
        FROM products
        GROUP BY category
        """)
    stat = list()
    for row in res.fetchall():
        stat.append(dict(row))
    cursor.close()
    return stat


def get_stat_by_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(quantity) as sum,
            MIN(quantity) as min,
            MAX(quantity) as max,
            AVG(quantity) as avg 
        FROM products
        GROUP BY category
        """)
    stat = list()
    for row in res.fetchall():
        stat.append(dict(row))
    cursor.close()
    return stat


# Все доступные товары по заданной категории, отсортированные по просмотрам (в порядке убывания)
def get_available_by_category(db, category):
    cursor = db.cursor()
    res = cursor.execute('''
    SELECT * FROM products
    WHERE isAvailable = True AND category = ? 
    ORDER BY views DESC
    ''', [category])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


#items = load_data('task_4_var_33_product_data.pkl')
db = connect_to_db('task-4.db')
#insert_data(db, items)
#updatable = load_update_data('task_4_var_33_update_data.text')
#handle_update(db, updatable)

top_by_version = get_top_by_version(db, 10)
stat_by_price = get_stat_by_price(db)
stat_by_quantity = get_stat_by_quantity(db)
available_by_category = get_available_by_category(db,'fruit')

write_json('res/res_top_by_version.json', top_by_version)
write_json('res/res_stat_by_price.json', stat_by_price)
write_json('res/res_stat_by_quantity.json', stat_by_quantity)
write_json('res/res_available_by_category.json', available_by_category)
