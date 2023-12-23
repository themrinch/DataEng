import pandas as pd
import numpy as np
import os
import json


def read_file(file_name):
    return next(pd.read_csv(file_name, chunksize=100_000))  # 1


def get_memory_stat_by_column(df, filename):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    file_info = list()
    file_info.append({'file_size': os.path.getsize(filename) // 1024})  # 2/7 (a)
    file_info.append({'file_in_memory_size': int(total_memory_usage // 1024)})  # 2/7 (b)
    column_stat = list()  # 2/7 (c)
    for key in df.dtypes.keys():
        column_stat.append({
            'column_name': key,
            'memory_abs': int(memory_usage_stat[key] // 1024),
            'memory_per': float(round(memory_usage_stat[key] / total_memory_usage * 100, 4)),
            'dtype': str(df.dtypes[key])
        })
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)  # 3
    file_info.append({'column_stat': column_stat})
    return file_info


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return '{:03.2f} MB'.format(usage_mb)


def opt_obj(df):  # 4
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    return converted_obj


def opt_int(df):  # 5
    dataset_int = df.select_dtypes(include=['int'])
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')

    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)

    memory_usage = {
        'dataset_float_mem_usage': mem_usage(dataset_int),
        'converted_float_mem_usage': mem_usage(converted_int),
        'compare_floats': compare_ints.to_dict()
    }
    pd.Series(memory_usage).to_json('res/compare_ints.json', index=False, default_handler=str)

    return converted_int


def opt_float(df):  # 6
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)

    memory_usage = {
        'dataset_float_mem_usage': mem_usage(dataset_float),
        'converted_float_mem_usage': mem_usage(converted_float),
        'compare_floats': compare_floats.to_dict()
    }
    pd.Series(memory_usage).to_json('res/compare_floats.json', index=False, default_handler=str)

    return converted_float


def optimize_dataset(df):
    optimized_dataset = df.copy()

    converted_obj = opt_obj(df)  # 4
    converted_int = opt_int(df)  # 5
    converted_float = opt_float(df)  # 6

    optimized_dataset[converted_obj.columns] = converted_obj
    optimized_dataset[converted_int.columns] = converted_int
    optimized_dataset[converted_float.columns] = converted_float

#    print(f'dataset_mem_usage: {mem_usage(df)}')
#    print(f'optimized_dataset_mem_usage: {mem_usage(optimized_dataset)}')

    return optimized_dataset


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


def get_subset(opt_df, col_names, file_name_in, file_name_out):
    opt_dtypes = opt_df.dtypes
    need_column = dict()
    for key in col_names:
        need_column[key] = opt_dtypes[key]
    #    print(f'{key}: {opt_dtypes[key]}')

    with open('res/dtypes.json', mode='w') as file:
        dtype_json = need_column.copy()
        for key in dtype_json.keys():
            dtype_json[key] = str(dtype_json[key])
        json.dump(dtype_json, file)

    has_header = True
    for chunk in pd.read_csv(file_name_in,
                             usecols=lambda x: x in col_names,
                             dtype=need_column,
                             chunksize=100_000):
        #    print(mem_usage(chunk))
        chunk.to_csv(file_name_out, mode='a', header=has_header, index=False)
        has_header = False


def read_types(file_name):
    with open(file_name, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes
