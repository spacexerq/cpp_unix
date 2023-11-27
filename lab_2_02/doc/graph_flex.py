from matplotlib import pyplot as plt
import numpy as np
import random as rd


def weight(pos1, pos2):
    return np.sqrt(pow((pos1[1] - pos2[1]), 2) + pow((pos1[2] - pos2[2]), 2))


def fill_rand(len, massive, upp_lim, low_lim):
    for i in range(len):
        massive[0][i] = rd.randint(low_lim, upp_lim)
        massive[1][i] = rd.randint(low_lim, upp_lim)
    return massive


len_sample = 10
low_lim = 0
upp_lim = 100
coordinates = []
coordinates.append([0]*len_sample)
coordinates.append([0]*len_sample)
coordinates = fill_rand(len_sample, coordinates, upp_lim, low_lim)
print(coordinates)