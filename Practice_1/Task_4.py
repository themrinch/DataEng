import csv

avg_salary = 0
items = list()

filename = 'text_4_var_33'
with open(filename, newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        item = {
            'number': int(row[0]),
            'name': row[2] + ' ' + row[1],
            'age': int(row[3]),
            'salary': int(row[4][0:-1])
        }
        avg_salary += item['salary']
        items.append(item)
avg_salary /= len(items)

filtered = list()
for item in items:
    if (item['salary'] > avg_salary) and (item['age'] > (25 + (33 % 10))):
        filtered.append(item)

filtered = sorted(filtered, key=lambda i: i['number'])

with open('r_text_4_var_33.csv', 'w', encoding='utf-8', newline='') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in filtered:
        writer.writerow(item.values())
