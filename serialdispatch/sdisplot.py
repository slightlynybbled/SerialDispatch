import matplotlib.pyplot as plt
import numpy as np


plt.ion()
fig = plt.figure()
plt.axis()

i = 0

while i < 1000:
    print(i)

    plt.scatter(i, np.random.random())

    i += 1
    plt.show()
    plt.pause(0.00000001)


