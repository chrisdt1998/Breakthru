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

print(np.random.randint(0, 10))
print(np.argwhere(silver_array == [1,3]))