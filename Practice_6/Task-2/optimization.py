from Practice_6.gen_func import *

file_name = 'automotive_fin.csv'
dataset = read_file(file_name)  # 1

stat_no_opt = get_memory_stat_by_column(dataset, file_name)  # 2 (a, b, c) - 3
write_json('res/stat_no_opt.json', stat_no_opt)

optimized_dataset = optimize_dataset(dataset)  # 4, 5, 6

stat_opt = get_memory_stat_by_column(optimized_dataset, file_name)  # 7 (a, b, c)
write_json('res/stat_opt.json', stat_opt)

get_subset(optimized_dataset, dataset.columns, file_name, 'res/subset_opt_automotive.csv')  # 8

# =============================================================================================
# # file_name = '[2]automotive.csv.zip'
# file_name = 'automotive.csv'
# column_dtype = {
#      'firstSeen': pd.StringDtype,
#      'brandName': pd.CategoricalDtype,
#      'modelName': pd.CategoricalDtype,
# #     'askPrice': pd.StringDtype,
#      'askPrice': np.dtype('int64'),
#      'isNew': pd.CategoricalDtype,
# #     'vf_Wheels': pd.StringDtype,
#      'vf_Wheels': np.dtype('uint8'),
# #     'vf_Seats': pd.StringDtype,
#      'vf_Seats': np.dtype('uint8'),
# #     'vf_Windows': pd.StringDtype,
#      'vf_Windows': np.dtype('uint8'),
# #     'vf_WheelSizeRear': pd.StringDtype,
#      'vf_WheelSizeRear': np.dtype('int64'),
# #     'vf_WheelBaseShort': pd.StringDtype
#      'vf_WheelBaseShort': np.dtype('float64')
# }
#
# total_size = 0
# has_header = True
#
# for part in pd.read_csv(file_name,
#                         usecols=lambda x: x in column_dtype.keys(),
#                         dtype=column_dtype,
#                         chunksize=500_000):
#     total_size += part.memory_usage(deep=True).sum()
# #    part.dropna().to_csv('automotive.csv', mode='a', header=has_header, index=False)
#     part.to_csv('automotive_fin.csv', mode='a', header=has_header, index=False)
#     has_header = False
#
# print(total_size)  # total_size_zip = 2537498438; total_size_csv_w_dtypes = 12451153
# =============================================================================================
