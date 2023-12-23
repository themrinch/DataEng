import pandas as pd

from Practice_6.gen_func import *

file_name = '[5]asteroid.zip'
dataset = pd.read_csv(file_name)  # 1

stat_no_opt = get_memory_stat_by_column(dataset, file_name)  # 2 (a, b, c) - 3
write_json('res/stat_no_opt.json', stat_no_opt)

optimized_dataset = optimize_dataset(dataset)  # 4, 5, 6

stat_opt = get_memory_stat_by_column(optimized_dataset, file_name)  # 7 (a, b, c)
write_json('res/stat_opt.json', stat_opt)

# 8
column_names = ['pdes', 'neo', 'pha', 'H', 'diameter', 'albedo',
                'diameter_sigma', 'orbit_id', 'ma', 'moid']

get_subset(optimized_dataset, column_names, file_name, 'res/subset_opt_asteroid.csv')
