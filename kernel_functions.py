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