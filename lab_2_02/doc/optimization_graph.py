import numpy as np
import random as rd
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import sparse
import networkx as nx
from datetime import datetime

INF = 2 ** 31 - 1


def TSP_dynamic(input_matrix, n):
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
    n = len(sample_points)
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

    init_graph = nx.complete_graph(len_sample)
    for i, j in init_graph.edges():
        if j > i:
            init_graph[i][j]['weight'] = distance(sample_points[i], sample_points[j])
    adj_matrix = nx.adjacency_matrix(init_graph).todense()
    points_dict = {}
    for i in range(n):
        points_dict[i] = (sample_points[i])
        adj_matrix[i, i] = INF
    plt.figure(figsize=(8, 8))
    graph = nx.Graph()
    graph.add_nodes_from(points_dict)
    for i in v1:
        graph.add_edge(i[0], i[1], weight=i[2])

    start_time = datetime.now()
    res = TSP_dynamic(adj_matrix, len_sample)
    print("Dynamic programming")
    print('time =', (datetime.now() - start_time).total_seconds())
    print('length =', res[0])
    d = []
    s = res[1]
    for i, v in enumerate(s):
        d.append([int(s[i - 1]), int(s[i])])
    nx.draw(graph, sample_points, width=1, edge_color="#C0C0C0", with_labels=True)
    nx.draw(graph, sample_points, width=2, edge_color="red", edgelist=d, style="dashed", node_size=0)
    namefile = str(len_sample) + "_dynamic.pdf"
    plt.savefig(namefile)
    plt.show()


def TSP_output_milp(points, circles, interceptions):
    init_graph = nx.complete_graph(len_sample)
    for i, j in init_graph.edges():
        if j > i:
            init_graph[i][j]['weight'] = distance(points[i], points[j])

    plt.figure(figsize=(8, 8))
    plt.axis("equal")
    start_time = datetime.now()
    res = TSP_milp(init_graph, circles, interceptions, True, False)
    date_diff = (datetime.now() - start_time).total_seconds()
    print("Optimization MILP")
    print("circles =", circles, ",interceptions =", interceptions)
    print('time =', date_diff)
    print("steps =", res["steps"])
    print("length =", res["length"], "\n")
    nx.draw(init_graph, points, width=1, edge_color="#C0C0C0", with_labels=True, font_color="black")
    nx.draw(res["graph"], points, width=2, edge_color="red", style="dashed", node_size=0)
    namefile = str(len_sample) + "_pts_" + str(
        circles) + "_circ_" + str(interceptions) + "_interc.pdf"
    plt.savefig(namefile)
    plt.show()


def distance(point1, point2):
    return np.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))


def triangle_intersection(a, b, c, vertex_array, val):
    if (b > a) or (c > a) or (a < 0.000001):
        return val
    cross_size = len(vertex_array)
    key = [True] * cross_size
    for i in range(cross_size):
        if (b == vertex_array[i]):
            key[i] = False
    p = 0.5 * (a + b + c)
    s = p * (p - a) * (p - b) * (p - c)
    r = 2 * np.sqrt(abs(s)) / a
    for i in range(cross_size):
        if key[i] and vertex_array[i] >= r:
            val += 1
    return val


def TSP_milp(init_graph, circles, cross, plt_show_flag=True, solver_display=False):
    n = len(init_graph)
    adjacency_matrix = nx.adjacency_matrix(init_graph, dtype=np.float64).todense()
    adjacency_matrix.sort(axis=1)
    vertex_array = adjacency_matrix[:, 1:circles + 1]
    del adjacency_matrix

    graph_of_neighbors = nx.Graph(())
    for i in range(n):
        for j in range(n):
            if i > j:
                value = 0
                for k in range(n):
                    if (k != i) and (k != j):
                        value = triangle_intersection(init_graph[i][j]['weight'], init_graph[i][k]['weight'],
                                                      init_graph[j][k]['weight'], vertex_array[k], value)
                        if value > cross:
                            break
                if value <= cross:
                    graph_of_neighbors.add_edge(i, j)
    del vertex_array

    graph_united = nx.Graph(())
    for i, j in list(graph_of_neighbors.edges()):
        for k in list(graph_of_neighbors.adj[i]):
            if j != k and not graph_united.has_edge(j, k):
                graph_united.add_edge(j, k)
        for k in list(graph_of_neighbors.adj[j]):
            if i != k and not graph_united.has_edge(i, k):
                graph_united.add_edge(i, k)

    for i, j in list(graph_of_neighbors.edges()):
        if not graph_united.has_edge(i, j):
            graph_united.add_edge(i, j)
    del graph_of_neighbors

    # Filling the objective function
    edges_list = list(graph_united.edges())
    n_var = len(edges_list)
    array_index = {}
    array_key = {}
    matrix_a = sparse.lil_matrix((n, n_var), dtype=np.int8)
    objective_function = np.empty(n_var, dtype=np.float64)
    for i, val in enumerate(edges_list):
        key = (val[0], val[1]) if val[0] > val[1] else (val[1], val[0])
        array_key[key] = i
        array_index[i] = key
        objective_function[i] = init_graph[key[0]][key[1]]['weight']
        matrix_a[key[0], i] = 1
        matrix_a[key[1], i] = 1
    del graph_united

    variable_bounds = (0, np.inf)
    lower_bound = [2] * n
    upper_bound = [2] * n

    constraints = 0
    step = 0
    while True:
        # Solving method while graph will contain only with 1 component
        res = optimize.milp(c=objective_function,
                            constraints=optimize.LinearConstraint(matrix_a, lower_bound, upper_bound),
                            bounds=variable_bounds, integrality=1, options={'disp': solver_display})
        step += 1
        graph_resilt = nx.Graph()
        for i, val in enumerate(res.x):
            if round(val) >= 1:
                graph_resilt.add_edge(*array_index[i])

        result_sets = list(nx.connected_components(graph_resilt))
        qty_sets = len(result_sets)

        if qty_sets == 1:
            break

        if qty_sets == 2:
            matrix_a.resize((n + constraints + 1, n_var))
            lower_bound += [2]
            upper_bound += [np.inf]
            for i in result_sets[0]:
                for j in result_sets[1]:
                    key = (i, j) if i > j else (j, i)
                    if key in array_key:
                        matrix_a[n + constraints, array_key[key]] = 1
            constraints += 1
            continue

        # The number of constraints equal to the number pf the components
        matrix_a.resize((n + constraints + qty_sets, n_var))
        for i, val_i in enumerate(result_sets):
            set2 = set()
            for l, val_l in enumerate(result_sets):
                if l != i:
                    for ii in result_sets[i]:
                        for j in val_l:
                            key = (ii, j) if ii > j else (j, ii)
                            if key in array_key:
                                set2.add(array_key[key])
            lower_bound += [2]
            upper_bound += [np.inf]
            for j in set2:
                matrix_a[n + constraints + i, j] = 1
        constraints += qty_sets
        # Steps showing
        if plt_show_flag:
            nx.draw(init_graph, points, width=0, with_labels=True, node_size=0, font_size=6, font_color="black")
            nx.draw(graph_resilt, points, width=1, edge_color="red", style="dashed", with_labels=False, node_size=0)
            plt.show()

    return {'length': res.fun, 'graph': graph_resilt, 'constraints': constraints, 'steps': step}


len_sample = 7

points = [(round(rd.randint(0, 1000)), round(rd.randint(0, 1000))) for i in range(len_sample)]
# TSP_output_milp(points, 4, 5)
# TSP_output_milp(points, 2, 2)
# TSP_output_dynamic(points)
points2 = [(5, 7), (4, 0), (5, 0), (-1, 0), (0, 0), (0, 2), (0, 3), (2.5, 2.5), (0, 1), (1, 0), (2, 0), (2, 1), (1, 2),
           (2, 3), (4, 1), (3, 2), (1, 1), (3, 3), (2, 2), (3, 1), (4, 2)]
len_sample = len(points)
TSP_output_milp(points, 4, 5)
#TSP_output_milp(points, 2, 2)
TSP_output_dynamic(points)
