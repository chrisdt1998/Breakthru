import numpy as np
import pandas as pd

silver_array = np.array([
    [1, 1, 1, 1, 1, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 9, 9, 9, 9, 9],
    [3, 4, 5, 6, 7, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 3, 4, 5, 6, 7]
])
silver_array = silver_array.transpose()
gold_array = np.array([
    [5, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7],
    [5, 4, 5, 6, 3, 7, 3, 7, 3, 7, 4, 5, 6]
])
gold_array = gold_array.transpose()
print(silver_array)

def check_pieces(piece, array):
    x = array[np.logical_and(piece[0] == array[:, 0],
                             piece[1] == array[:, 1])]

    return x

# x = np.where(silver_array == [6, 9])
# print(x)
#
# x = check_pieces([6, 9], silver_array)
# print(x)
#
# print([6, 9] in silver_array)
#
# print(silver_array[silver_array == [6, 9]])
print(np.argwhere(silver_array == np.array([6, 9])))

x = np.argwhere(np.logical_and(silver_array[:, 0] == 6, silver_array[:, 1] == 9))
print(x)
silver_array[x] = [100, 100]
print(silver_array)
# arr = np.arange(12) + 1
# print(arr)
# mask = np.ones(len(arr), dtype=bool)
# print(mask)
# mask[[0,2,4]] = False
# print(mask)
# result = arr[mask,...]
# print(result)

