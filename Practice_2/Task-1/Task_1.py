import numpy as np
import json

filename = 'matrix_33.npy'
matrix = np.load(filename)
size = len(matrix)

matrix_stat = dict()
matrix_stat['sum'] = np.sum(matrix)
matrix_stat['avr'] = np.mean(matrix)
matrix_stat['sumMD'] = np.trace(matrix)
matrix_stat['avrMD'] = np.mean(np.diag(matrix))
matrix_stat['sumSD'] = np.trace(np.rot90(matrix))
matrix_stat['avrSD'] = np.mean(np.diag(np.rot90(matrix)))
matrix_stat['max'] = np.max(matrix)
matrix_stat['min'] = np.min(matrix)

for key in matrix_stat.keys():
    matrix_stat[key] = float(matrix_stat[key])

with open('matrix_stat.json', 'w') as result:
    result.write(json.dumps(matrix_stat))

norm_matrix = np.array([[matrix[i][j] / matrix_stat['sum'] for j in range(size)] for i in range(size)])
np.save('norm_matrix', norm_matrix)