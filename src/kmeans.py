import numpy as np


def cosine_similarity(x, vectors):
    sims = np.dot(x, vectors.T)
    return sims


def cosine_distance(x, vectors):
    return 1 - cosine_similarity(x, vectors)


def euclid(x, vectors):
    dists = np.sqrt(np.sum((x - vectors)**2, axis=1))
    return dists


class KMeans(object):
    def __init__(self, n_clusters, max_iter=100, eps=1e-4, metrics='euclid', seed=None):

        np.random.seed(seed)

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.eps = eps

        self.n_iter = None
        self.centroids = None
        self.inertia = None

        if metrics == 'euclid':
            self.measure = euclid
        elif metrics == 'cosine':
            self.measure = cosine_distance
        else:
            raise ValueError(f'Unknown metrics: {metrics}')

    def init_centroids_zero(self, x):
        centroids = np.zeros((self.n_clusters, x.shape[1]))
        return centroids

    def init_centroids_randomly(self, x):
        indices = np.random.choice(x.shape[0], self.n_clusters)
        centroids = x[indices, :]
        return centroids

    def init_centroids_kmeanspp(self, x):
        n_data, n_feature = x.shape
        distances = np.zeros((n_data, self.n_clusters))
        centroids = self.init_centroids_zero(x)

        probs = np.repeat(1/n_data, n_data)
        for i in range(self.n_clusters):
            idx = np.random.choice(n_data, p=probs)
            centroids[i, :] = x[idx, :]
            distances[:, i] = self.measure(centroids[i, :], x)

            probs = np.sum(distances, axis=1) / np.sum(distances)
        return centroids

    def fit(self, x, init_alg='kmeans++'):
        n_data, n_feature = x.shape

        if init_alg == 'random':
            centroids = self.init_centroids_randomly(x)
        elif init_alg == 'kmeans++':
            centroids = self.init_centroids_kmeanspp(x)
        else:
            ValueError(f'Unknown initializing algorithm: {init_alg}')

        centroids_new = self.init_centroids_zero(x)

        cluster_labels = np.zeros(n_data, dtype=int)

        for epoch in range(self.max_iter):
            inertia = 0
            distances = []
            for i in range(self.n_clusters):
                # calc distances between a datapoint and centroids
                dists = self.measure(centroids[i], x)
                distances.append(dists)
            distances = np.array(distances).T
            cluster_labels = distances.argmin(axis=1)
            inertia = distances.min(axis=1).mean()

            # update centroids
            for i in range(self.n_clusters):
                centroids_new[i] = x[cluster_labels == i].mean(axis=0)

            # check convergence
            update = np.mean([
                self.measure(c, c_new[np.newaxis, :])
                for c, c_new in zip(centroids, centroids_new)
            ])
            if update <= self.eps:
                break

            # update centroids
            centroids = centroids_new.copy()

        self.n_iter = epoch + 1
        self.centroids = centroids_new.copy()
        self.inertia = inertia

        return cluster_labels
