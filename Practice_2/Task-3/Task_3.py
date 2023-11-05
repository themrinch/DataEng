import json
import msgpack
import os

filename = 'products_33.json'
with open(filename) as file:
    data = json.load(file)
# print(data)

products = dict()

for item in data:
    if item['name'] in products:
        products[item['name']].append(item['price'])
    else:
        products[item['name']] = list()
        products[item['name']].append(item['price'])

result = list()

for name, prices in products.items():
    sum_price = 0
    max_price = prices[0]
    min_price = prices[0]
    size = len(prices)
    for price in prices:
        sum_price += price
        max_price = max(max_price, price)
        min_price = min(min_price, price)

    result.append({
        'name': name,
        'max': max_price,
        'min': min_price,
        'avr': sum_price / size
    })

with open('products_result.json', 'w') as res_json:
    res_json.write((json.dumps(result)))

with open('products_result.msgpack', 'wb') as res_msgpack:
    res_msgpack.write(msgpack.dumps(result))

print(f"products_result_json     = {os.path.getsize('products_result.json')}")
print(f"products_result_msgpack = {os.path.getsize('products_result.msgpack')}")