import numpy as np


class Affine(object):
    def Ta(self, a, arr):
        transform_matrix = np.array([
            [1, 0, a[0]],
            [0, 1, a[1]],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Ro(self, phi, arr):
        transform_matrix = np.array([
            [np.cos(phi), np.sin(phi), 0],
            [-np.sin(phi), np.cos(phi), 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Sy(self, arr):
        transform_matrix = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Sx(self, arr):
        transform_matrix = np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Sxy(self, arr):
        transform_matrix = np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Ho(self, k, arr):
        transform_matrix = np.array([
            [k, 0, 0],
            [0, k, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Shx(self, k, arr):
        transform_matrix = np.array([
            [1, k, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def Shy(self, k, arr):
        transform_matrix = np.array([
            [1, 0, 0],
            [k, 1, 0],
            [0, 0, 1]
        ]).T

        return np.dot(arr, transform_matrix)

    def transform(self, transform_matrix, arr):
        return np.dot(arr, transform_matrix.T)
