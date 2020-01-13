import numpy as np


def eigen(x):
    # calc eigen values
    eigen_values, eigen_vectors = np.linalg.eig(np.dot(x.T, x))
    indices = np.argsort(eigen_values)[::-1]

    # sort
    eigen_values = eigen_values[indices]
    eigen_vectors = eigen_vectors[:, indices]
    return eigen_values, eigen_vectors


def svd(x):
    eigen_values, eigen_vectors = eigen(x)

    # singular values and matrix
    singular_values = np.sqrt(eigen_values)
    sigma = np.diag(singular_values)

    # Right singular matrix
    v = eigen_vectors

    # Left singular matrix
    u = np.dot(x, v)
    u = np.array([u[:, i] / singular_values[i] for i in range(len(singular_values))]).T

    return u, sigma, v


class LSI(object):
    def __init__(self, x, num_topics):
        self.x = x
        self.num_topics = num_topics
        self.u, self.sigma, self.v = svd(x.T)

    def get_vectors(self):
        vecs = np.dot(self.x, self.u[:, :self.num_topics]).astype(float)
        return vecs
