import numpy as np

def gaussian_kernel(x, xi, h):
    return np.exp(-0.5 * ((x - xi) / h) ** 2) / (h * np.sqrt(2 * np.pi))

def kernel_regression(X_train, y_train, x_query, h, num_neighbors=10, x_min=0, x_max=None):
    if x_max is None:
        x_max = X_train.max()
    
    # Only consider the nearest neighbors for the kernel regression
    X_neighbors = np.arange(x_query - num_neighbors, x_query + num_neighbors)
    X_neighbors = X_neighbors[(X_neighbors >= x_min) & (X_neighbors < x_max)]
    
    y_neighbors = y_train[X_neighbors]  # Adjust indexing for the slice
    
    # Compute the weights for the neighbors
    weights = np.array([gaussian_kernel(x_query, xi, h) for xi in X_neighbors])
    weights /= weights.sum()  # Normalize the weights

    # Return the weighted sum of the nearest neighbors' responses
    return np.nansum(weights * y_neighbors)

def k(x):
    return x*1000

def convert_frequency_to_index(f):
    """ Function which converts input frequency in MHz to index,
    Where index 600k = 6 GHz
    index 0 = 20 MHz

    Using inverse of
    f = i*(max_f-min_f)/k(600) + min_f
    """

    min_f = 20*1e6  # 20 MHz
    max_f = 6000*1e6  # 6 GHz

    return int((f*1e6 - min_f)*k(600)/(max_f-min_f))