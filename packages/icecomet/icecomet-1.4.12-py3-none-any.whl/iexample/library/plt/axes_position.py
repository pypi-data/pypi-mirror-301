import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2, figsize=(12, 6))

axs[0, 0].plot([1, 2, 3], [4, 5, 6])
axs[0, 1].scatter([1, 2, 3], [4, 5, 6])
axs[1, 0].bar([1, 2, 3], [4, 5, 6])
axs[1, 1].hist([1, 2, 3, 4, 5, 6])

plt.show()
