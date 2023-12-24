import numpy as np
import random as rd
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import sparse
import networkx as nx
from datetime import datetime as dt

# city_data = [(1, 2), (3, 1), (4, 1), (3, 2), (4, 2), (1, 3), (3, 3), (4, 4), (6, 4), (2, 4.5), (3, 4.5), (5, 4.5),
#              (3.5, 5), (2, 5.5), (3, 5.5), (4.5, 5.5), (3.5, 6), (1, 6.5), (2, 6.5), (3, 6.5), (3, 7), (3.5, 7),
#              (4.5, 7), (3, 8)]

city_data = [(3.5, 5), (2, 5.5), (3, 5.5), (4.5, 5.5), (3.5, 6), (1, 6.5), (2, 6.5), (3, 6.5), (3, 7.5), (3.5, 7),
             (4.5, 7), (3, 8.5)]


def cross():
    return


def city_sim(city_data, w0_3_edge, w11_8_edge, start_tick=0, stop_tick=5, tickrate=1, bot_stop=1, top_stop=1):
    N = len(city_data)
    w_plus = np.empty((N, N))
    w_min = np.empty((N, N))
    for i in range(stop_tick - start_tick):
        # if i != 0:
        #         0  1  2  3  4  5  6  7  8  9 10  11
        w_adj = np.array(([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
                          [0, 0, -1, 0, 0, 2 / 5, 3 / 5, 0, 0, 0, 0, 0],  # 1
                          [0, 1 / 2, 0, 0, -1, 0, 0, 1 / 2, 0, 0, 0, 0],  # 2
                          [-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 3
                          [0, 0, 1 / 3, -1, 0, 0, 0, 1 / 3, 0, 0, 1 / 3, 0],  # 4
                          [0, -1, 0, 0, 0, 0, 2 / 5, 0, 3 / 5, 0, 0, 0],  # 5
                          [0, -1, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0],  # 6
                          [0, 0, -1, 0, -1, 0, -1, 0, 1, 0, 0, 0],  # 7
                          [0, 0, 0, 0, 0, -1, 0, -1, 0, -1, 0, 1],  # 8
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0],  # 9
                          [0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0],  # 10
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]))  # 11

        # print(np.sum(w_adj))
        if i == 0:
            w_plus[0][3] = w0_3_edge[0]
            w_plus[3][0] = w0_3_edge[0]
        else:
            w_plus_temp = np.copy(w_plus)
            flag = 0
            for x in range(N):
                if flag == 32:
                    break
                for y in range(N):
                    new_mat = np.dot(w_plus_temp, w_adj)
                    if w_adj[x][y] != 0:
                        mul11 = w_plus_temp[x]
                        mul22 = w_adj[x]
                        mul12 = w_plus_temp[y]

                        mul21 = w_adj[y]
                        mult2 = np.dot(w_plus_temp, w_adj[y])
                        mult1 = np.dot(w_plus_temp, w_adj[x])
                        connected_roads = np.nonzero(w_adj[x])
                        a = w_adj[y] * np.dot(w_plus_temp[x], w_adj[x])
                        # mult_min = np.dot(w_plus_temp, w_adj[y])
                        w_plus[y] -= w_adj[y] * np.dot(w_plus_temp[x], w_adj[x])
                        # w_plus[x] += w_adj[x]*np.dot(w_plus_temp[y], w_adj[y])
                        b = []

        w8_9_edge = [round(w_plus[9][8], 0), round(w_min[8][9], 0)]
        w9_10_edge = [round(w_plus[10][9], 0), round(w_min[9][10], 0)]
        w10_4_edge = [round(w_plus[4][10], 0), round(w_min[10][4], 0)]
        w4_3_edge = [round(w_plus[3][4], 0), round(w_min[4][3], 0)]
        w2_4_edge = [round(w_plus[4][2], 0), round(w_min[2][4], 0)]
        w1_2_edge = [round(w_plus[2][1], 0), round(w_min[1][2], 0)]
        w1_5_edge = [round(w_plus[1][5], 0), round(w_min[1][5], 0)]
        w1_6_edge = [round(w_plus[1][6], 0), round(w_min[1][6], 0)]
        w6_7_edge = [round(w_plus[7][6], 0), round(w_min[7][6], 0)]
        w2_7_edge = [round(w_plus[2][7], 0), round(w_min[2][7], 0)]
        w4_7_edge = [round(w_plus[4][7], 0), round(w_min[4][7], 0)]
        w7_8_edge = [round(w_plus[7][8], 0), round(w_min[7][8], 0)]
        w5_8_edge = [round(w_plus[5][8], 0), round(w_min[5][8], 0)]
        w5_6_edge = [round(w_plus[5][6], 0), round(w_min[5][6], 0)]
        w0_3_edge = [round(w_plus[0][3], 0), round(w_min[0][3], 0)]
        # w11_8_edge =
        # if not i < top_stop:
        #     w11_8_edge = w11_8
        # else:
        #     w11_8_edge = w11_8
        if not i < bot_stop:
            w_plus[0][3] = 0
            w_plus[3][0] = 0
        city = nx.complete_graph(N)
        points_dict = {}
        for loc in range(N):
            points_dict[loc] = (city_data[loc])
        city.add_nodes_from(points_dict)
        edged_rem = list(city.edges)
        city.remove_edges_from(edged_rem)
        d = [(0, 3, w0_3_edge), (11, 8, w11_8_edge), (8, 9, w8_9_edge), (9, 10, w9_10_edge), (10, 4, w10_4_edge),
             (4, 3, w4_3_edge), (2, 4, w2_4_edge),
             (1, 2, w1_2_edge), (1, 5, w1_5_edge), (1, 6, w1_6_edge), (6, 7, w6_7_edge), (2, 7, w2_7_edge),
             (4, 7, w4_7_edge), (7, 8, w7_8_edge),
             (5, 8, w5_8_edge), (5, 6, w5_6_edge)]
        city.add_weighted_edges_from(d)
        labels = nx.get_edge_attributes(city, 'weight')
        nx.draw(city, city_data, with_labels=True, node_color="yellow")
        nx.draw_networkx_edge_labels(city, city_data, edge_labels=labels)
        # labels = {e: city.edges[e]['score'] for e in city.edges}
        plt.show()
        # imname = "simulation_img/"+str(i+1)+"_step"+".png"
        # plt.savefig(imname)


w_start_bot = [30, 0]
w_start_top = [0, 0]
city_sim(city_data, w_start_bot, w_start_top)
