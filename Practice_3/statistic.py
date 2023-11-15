import numpy as np

def select_data(data, num_item, word_item):
    length = len(data)
    numbers_stat = list()
    word_stat = dict()
    for elem in data:
        numbers_stat.append(elem[num_item])
        if elem[word_item] in word_stat.keys():
            word_stat[elem[word_item]] += 1
        else:
            word_stat[elem[word_item]] = 1
    return numbers_stat, word_stat, length

def num_stat(num_data):
    result = {
        'max': float(np.max(num_data)),
        'min': float(np.min(num_data)),
        'avg': float(np.mean(num_data)),
        'sum': float(np.sum(num_data)),
        'std': float(np.std(num_data))
    }
    return result


def word_stat(word_data, length):
    result = dict(sorted(word_data.items(), reverse=True, key=lambda item: item[1]))
    for item in result:
        result[item] = str(round(((result[item] / length) * 100), 2)) + '%'
    return result

