import numpy as np
import random
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import sparse
import networkx as nx
from datetime import datetime


# what does sparse doing?

def TSP_output(points, circles, interceptions):
    init_graph = nx.complete_graph(len_sample)
    for i, j in init_graph.edges():
        if j > i:
            init_graph[i][j]['weight'] = distance(points[i], points[j])

    plt.figure(figsize=(12, 9))
    plt.axis("equal")
    start_time = datetime.now()
    res = TSP_milp(init_graph, circles, interceptions, False, False)
    date_diff = (datetime.now() - start_time).total_seconds()
    print("circles =", circles, ",interceptions =", interceptions)
    print('time =', date_diff)
    print("steps =", res["steps"])
    print("length =", res["length"])
    nx.draw(init_graph, points, width=0, with_labels=True, node_size=0, font_size=6, font_color="black")
    nx.draw(res["graph"], points, width=1, edge_color="red", style="-", with_labels=False, node_size=0)
    namefile = str(len_sample) + "_pts_" + str(circles) + "_circ_" + str(interceptions) + "_interc.pdf"
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


def TSP_milp(init_graph, circles, cross, plt_show_flag=False, solver_display=False):
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
            nx.draw(graph_resilt, points, width=1, edge_color="red", style="-", with_labels=False, node_size=0)
            plt.show()

    return {'length': res.fun, 'graph': graph_resilt, 'constraints': constraints, 'steps': step}


len_sample = 100
points = [(round(random.randint(0, 300)), round(random.randint(0, 200))) for i in range(len_sample)]
TSP_output(points, 4, 5)
TSP_output(points, 2, 2)
