import numpy as np
from scipy.spatial.distance import cityblock
import matplotlib.pyplot as plt


class K_Medoids:
    def __init__(self, vector_list, C, iterations=100):
        self.vector_list = vector_list
        self.C = C
        self.iterations = iterations
        self.medoids = list()
        for i in range(C):
            rand_id = np.random.randint(len(self.vector_list))
            self.medoids.append(self.vector_list[rand_id])
        self.previous_medoids = None
        self.elem2cluster = list()
        self.previous_elem2cluster = None
        self.cost = None
        self.previous_cost = None

    def __associate_to_clusters(self):
        self.previous_cost = self.cost
        self.previous_elem2cluster = self.elem2cluster
        self.cost = np.zeros((self.C, ))
        self.elem2cluster = list()
        for elem in self.vector_list:
            closest_medoid = None
            closest_medoid_distance = None
            for c, medoid in enumerate(self.medoids):
                if elem is not medoid:
                    mannathan_distance = cityblock(elem, medoid)
                    if closest_medoid_distance is None:
                        closest_medoid_distance = mannathan_distance
                        closest_medoid = c
                    elif closest_medoid_distance > mannathan_distance:
                        closest_medoid_distance = mannathan_distance
                        closest_medoid = c
            self.elem2cluster.append(closest_medoid)
            self.cost[closest_medoid] += closest_medoid_distance

    def __swap_medoid(self):
        self.previous_medoids = self.medoids
        rand_id = np.random.randint(len(self.medoids))
        rand_medoid = self.medoids[rand_id]
        rand_id = np.random.randint(len(self.vector_list))
        rand_non_medoid = self.vector_list[rand_id]
        while rand_medoid is rand_non_medoid:
            rand_id = np.random.randint(len(self.vector_list))
            rand_non_medoid = self.vector_list[rand_id]
        self.medoids = [medoid if medoid is not rand_medoid
                        else rand_non_medoid for medoid in self.medoids]

    def iterate(self):
        self.__associate_to_clusters()
        for i in range(self.iterations):
            print('iterations', i, 'cost', np.sum(self.cost))
            self.__swap_medoid()
            self.__associate_to_clusters()
            if np.sum(self.cost) > np.sum(self.previous_cost):
                self.medoids = self.previous_medoids
                self.elem2cluster = self.previous_elem2cluster
                self.cost = self.previous_cost
            # else:
            #     colors = ['r', 'g', 'b']
            #     color_list = [colors[cluster] for cluster in self.elem2cluster]
            #     plt.figure()
            #     plt.scatter(self.vector_list[:, 0], self.vector_list[:, 1], color=color_list)
            #     plt.show()

if __name__ == '__main__':
    data = np.random.uniform(0, 10, (70, 2))
    kmed = K_Medoids(data, 5, 300)
    kmed.iterate()
    print('data', data)
    print('kmed.medoids', kmed.medoids)
    print('kmed.elem2cluster', kmed.elem2cluster)
    colors = ['r', 'g', 'b', 'c', 'm']
    color_list = [colors[cluster] for cluster in kmed.elem2cluster]
    plt.figure()
    plt.scatter(data[:, 0], data[:, 1], color=color_list)
    plt.show()
