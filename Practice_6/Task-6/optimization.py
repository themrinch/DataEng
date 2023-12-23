from Practice_6.gen_func import *

file_name = '2020_2021_01_JUN_TO_FROM_MODIS.csv'
dataset = read_file(file_name)  # 1

stat_no_opt = get_memory_stat_by_column(dataset, file_name)  # 2 (a, b, c) - 3
write_json('res/stat_no_opt.json', stat_no_opt)

optimized_dataset = optimize_dataset(dataset)  # 4, 5, 6

stat_opt = get_memory_stat_by_column(optimized_dataset, file_name)  # 7 (a, b, c)
write_json('res/stat_opt.json', stat_opt)

# 8
column_names = ['latitude', 'longitude', 'brightness', 'scan', 'track',
                'satellite', 'confidence', 'frp', 'daynight', 'type']

get_subset(optimized_dataset, column_names, file_name, 'res/subset_opt_2020_2021_01_JUN_TO_FROM_MODIS.csv')
