import numpy as np
import os

filename = 'matrix_33_2.npy'
matrix = np.load(filename)
size = len(matrix)

x = list()
y = list()
z = list()

lim = 533

for i in range(size):
    for j in range(size):
        if matrix[i][j] > lim:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez('points', x=x, y=y, z=z)
np.savez_compressed('points_zip', x=x, y=y, z=z)

print(f"points     = {os.path.getsize('points.npz')}")
print(f"points_zip = {os.path.getsize('points_zip.npz')}")