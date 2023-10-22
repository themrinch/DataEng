filename = 'text_2_var_33'
with open(filename) as file:
    lines = file.readlines()

avg_lines = list()

for line in lines:
    nums = line.split('|')
    length = len(nums)
    sum_line = 0
    for num in nums:
        sum_line += int(num)
    avg_lines.append(sum_line/length)

with open('r_text_2_var_33.txt', 'w') as result:
    for value in avg_lines:
        result.write(str(value) + '\n')