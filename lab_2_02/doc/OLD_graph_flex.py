from matplotlib import pyplot as plt
import numpy as np
import random as rd
import networkx as nx


def weight(pos1, pos2):
    return np.sqrt(pow((pos1[0] - pos2[0]), 2) + pow((pos1[1] - pos2[1]), 2))

'''
def fill_rand(len, massive, upp_lim, low_lim):
    for i in range(len):
        massive[0][i] = rd.randint(low_lim, upp_lim)
        massive[1][i] = rd.randint(low_lim, upp_lim)
    return massive
'''
#looking for integer coordinates


def TSP_milp(init_graph, circles, cross):
    # Находит минимальный путь в графе методом целочисленного линейного программирования
    print('Run TSP milp', end='')
    n = len(init_graph)
    # Разворачиваем граф как матрицу смежности
    adjacency_matrix = nx.adjacency_matrix(init_graph, dtype=np.float64).todense()
    # Сортируем матрицу смежности по строкам
    adjacency_matrix.sort(axis=1)
    # Выбираем только часть матрицы
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

    # Заполняем основные элементы
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

    # Ограничение на диаппазон переменных
    variable_bounds = (0, 1)
    #     variable_bounds = (0, np.inf)

    # Начальные ограничения модели
    lower_bound = [2] * n
    upper_bound = [2] * n

    constraints = 0
    step = 0
    while True:
        # Ищем решение
        res = optimize.milp(c=objective_function,
                            constraints=optimize.LinearConstraint(matrix_a, lower_bound, upper_bound),
                            bounds=variable_bounds, integrality=1, options={'disp': True})
        step += 1
        print('.', end='')

        # Сохраняем результат в виде графа связей
        graph_resilt = nx.Graph()
        for i, val in enumerate(res.x):
            if round(val) >= 1:
                graph_resilt.add_edge(*array_index[i])

        # Разбиваем граф результата на подмножества
        result_sets = list(nx.connected_components(graph_resilt))
        qty_sets = len(result_sets)

        # Решение найдено если в графе только одно множество
        if qty_sets == 1:
            break

        # Если только два множества соединяем их напрямую
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

        # Вводим столько ограничений, сколько у нас получилось множеств
        matrix_a.resize((n + constraints + qty_sets, n_var))
        for i, val_i in enumerate(result_sets):
            # Выбираем тот алгоритм, который добавит меньше значений в разреженную матрицу
            value, add_set = algorithm_evaluation(array_key, result_sets, i)
            if value:
                lower_bound += [0]
                upper_bound += [len(val_i) - 1]
            else:
                lower_bound += [2]
                upper_bound += [np.inf]
            for j in add_set:
                matrix_a[n + constraints + i, j] = 1
        constraints += qty_sets
    print()

    return {'length': res.fun, 'graph': graph_resilt, 'constraints': constraints, 'steps': step}


len_sample = 25
low_lim = 0
upp_lim = 100
coordinates = [(round(rd.randint(low_lim, upp_lim)), round(rd.randint(low_lim, upp_lim))) for i in range(len_sample)]
init_graph = nx.complete_graph(len_sample)
for i, j in init_graph.edges():
    if j > i:
        init_graph[i][j]['weight'] = weight(coordinates[i], coordinates[j])


