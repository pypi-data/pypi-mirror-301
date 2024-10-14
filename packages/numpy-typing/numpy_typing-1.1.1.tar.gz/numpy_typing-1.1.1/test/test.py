from numpy_typing import np, ax

a:np.float32_1d[ax.sample] = np.zeros((10,))
b = np.concatenate([a, a], axis=ax.sample)


