import random as rd
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import numpy as np

INF = 2 ** 31 - 1

def distance1(x1, y1, x2, y2):
    return np.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

def distance(p1,p2):
    return np.sqrt(pow((p1[1] - p2[1]), 2) + pow((p1[0]-p2[0]), 2))


def TSP_dynamic(input_matrix):
    n = len(input_matrix)
    # Генерация служебных массивов
    s = (1 << (n - 1)) - 1
    path = [0] * s
    local_sum = [0] * s

    for i in range(s):
        path[i] = [0] * (n - 1)
        local_sum[i] = [-1] * (n - 1)
    m = [n - 1, input_matrix.copy(), path, local_sum]

    sum_path = INF
    for i in range(m[0]):
        index = 1 << i
        if s & index != 0:
            sum_temp = tsp_next(m, s ^ index, i) + m[1][i + 1][0]
            if sum_temp < sum_path:
                sum_path = sum_temp
                m[2][0][0] = i + 1
    m[3][0][0] = sum_path

    # Вывод оптимального пути
    res = []
    init_point = int(path[0][0])
    res.append(init_point)
    s = ((1 << m[0]) - 1) ^ (1 << init_point - 1)
    for i in range(1, m[0]):
        init_point = int(path[s][init_point - 1])
        res.append(init_point)
        s = s ^ (1 << init_point - 1)
    res.append(0)
    return [sum_path, res]


def tsp_next(m, s, init_point):
    if m[3][s][init_point] != -1:
        return m[3][s][init_point]
    if s == 0:
        return m[1][0][init_point + 1]
    sum_path = INF
    for i in range(m[0]):
        index = 1 << i
        if s & index != 0:
            sum_temp = tsp_next(m, s ^ index, i) + m[1][i + 1][init_point + 1]
            if sum_temp < sum_path:
                sum_path = sum_temp
                m[2][s][init_point] = i + 1
    m[3][s][init_point] = sum_path
    return sum_path


def TSP_output_dynamic(sample_points):
    n = 5
    v1 = []
    input_matrix1 = []
    for k1 in range(len_sample):
        m1 = []
        p1 = sample_points[k1]
        for k2 in range(len_sample):
            p2 = sample_points[k2]
            if k1 == k2:
                m1.append(INF)
            else:
                m1.append(int(distance(p1, p2)))
                v1.append([k1, k2, int(distance(p1, p2))])
        input_matrix1.append(m1.copy())
    points_dict = {}
    for i in range(n):
        points_dict[i] = (sample_points[i])
    plt.figure(figsize=(8, 8))
    graph = nx.Graph()
    graph.add_nodes_from(points_dict)
    for i in v1:
        graph.add_edge(i[0], i[1], weight=i[2])

    start_time = datetime.now()
    res = TSP_dynamic(input_matrix1)
    print('time =', (datetime.now() - start_time).total_seconds())
    d = []
    s = res[1]
    for i, v in enumerate(s):
        d.append([int(s[i - 1]), int(s[i])])
    nx.draw(graph, sample_points, width=1, edge_color="#C0C0C0", with_labels=True)
    nx.draw(graph, sample_points, width=2, edge_color="red", edgelist=d, style="dashed")
    plt.show()

len_sample = 10
points = [(round(rd.randint(0, 100)), round(rd.randint(0, 100))) for i in range(len_sample)]
TSP_output_dynamic(points)
