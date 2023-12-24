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


def city_sim(city_data, w0_3_edge, w11_8_edge, start_tick=0, stop_tick=20, tickrate=1, bot_stop=2, top_stop=1):
    for i in range(stop_tick - start_tick):
        tick = tickrate
        w8_9 = [0, 0]
        w9_10 = [0, 0]
        w10_4 = [0, 0]
        w4_3 = [0, 0]
        w2_4 = [0, 0]
        w1_2 = [0, 0]
        w1_5 = [0, 0]
        w1_6 = [0, 0]
        w6_7 = [0, 0]
        w2_7 = [0, 0]
        w4_7 = [0, 0]
        w7_8 = [0, 0]
        w5_8 = [0, 0]
        w5_6 = [0, 0]
        w11_8 = [0, 0]
        w0_3 = [0, 0]
        if i != 0:
            # stream in
            # w4_3[0] = round(w4_3_edge[0] + tick * w0_3_edge[0] - w2_4[0] - w10_4[0] - w4_7[0], 1)
            # w2_4[0] = round(w2_4_edge[0] + tick * w4_3_edge[0] / 3 - w2_7[0] - w1_2[0], 1)
            # w10_4[0] = round(w10_4_edge[0] + tick * w4_3_edge[0] / 3 - w9_10[0], 1)
            # w4_7[0] = round(w4_7_edge[0] + tick * w4_3_edge[0] / 3 - w7_8[0], 1)
            # w2_7[0] = round(w2_7_edge[0] + tick * w2_4_edge[0] / 2 - w7_8[0], 1)
            # w1_2[0] = round(w1_2_edge[0] + tick * w2_4_edge[0] / 2 - w1_5[0], 1)
            # w1_5[0] = round(w1_5_edge[0] + tick * w1_2_edge[0] * 2 / 5, 1)
            # w1_6[0] = round(w1_6_edge[0] + tick * w1_2_edge[0] * 3 / 5, 1)
            # w5_6[0] = round(w5_6_edge[0] + tick * w1_5_edge[0] * 2 / 5, 1)
            # w6_7[0] = round(w6_7_edge[0] + tick * w5_6_edge[0] + tick * w1_6_edge[0], 1)
            # w5_8[0] = round(w5_8_edge[0] + tick * w1_5_edge[0] * 3 / 5, 1)
            # w7_8[0] = round(w7_8_edge[0] + tick * w6_7_edge[0] + tick * w2_7_edge[0] + tick * w4_7_edge[0], 1)
            # w9_10[0] = round(w9_10_edge[0] + tick * w10_4_edge[0], 1)
            # w8_9[0] = round(w8_9_edge[0] + tick * w9_10_edge[0], 1)
            # w11_8[0] = round(w11_8_edge[0] + tick * w5_8_edge[0] + tick * w8_9_edge[0] + tick * w7_8_edge[0], 1)

            w4_3[0] = round(tick * w0_3_edge[0] - w2_4[0] - w10_4[0] - w4_7[0], 0)
            w2_4[0] = round(tick * w4_3_edge[0] / 3 - w2_7[0] - w1_2[0], 0)
            w10_4[0] = round(tick * w4_3_edge[0] / 3 - w9_10[0], 0)
            w4_7[0] = round(tick * w4_3_edge[0] / 3 - w7_8[0], 0)
            w2_7[0] = round(tick * w2_4_edge[0] / 2 - w7_8[0], 0)
            w1_2[0] = round(tick * w2_4_edge[0] / 2 - w1_5[0], 0)
            w1_5[0] = round(tick * w1_2_edge[0] * 2 / 5 - w5_8[0] - w5_6[0], 0)
            w1_6[0] = round(tick * w1_2_edge[0] * 3 / 5 - w6_7[0], 0)
            w5_6[0] = round(tick * w1_5_edge[0] * 2 / 5 - - w6_7[0], 0)
            w6_7[0] = round(tick * w5_6_edge[0] + tick * w1_6_edge[0] - w7_8[0], 0)
            w5_8[0] = round(tick * w1_5_edge[0] * 3 / 5, 1)
            w7_8[0] = round(tick * w6_7_edge[0] + tick * w2_7_edge[0] + tick * w4_7_edge[0], 0)
            w9_10[0] = round(tick * w10_4_edge[0], 0)
            w8_9[0] = round(tick * w9_10_edge[0], 0)
            w11_8[0] = round(w11_8_edge[0] + tick * w5_8_edge[0] + tick * w8_9_edge[0] + tick * w7_8_edge[0], 0)


        w8_9_edge = w8_9
        w9_10_edge = w9_10
        w10_4_edge = w10_4
        w4_3_edge = w4_3
        w2_4_edge = w2_4
        w1_2_edge = w1_2
        w1_5_edge = w1_5
        w1_6_edge = w1_6
        w6_7_edge = w6_7
        w2_7_edge = w2_7
        w4_7_edge = w4_7
        w7_8_edge = w7_8
        w5_8_edge = w5_8
        w5_6_edge = w5_6
        # w11_8_edge =
        if not i < top_stop:
            w11_8_edge = w11_8
        else:
            w11_8_edge = w11_8
        if not i < bot_stop:
            w0_3_edge = [0, 0]
        N = len(city_data)
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


w_start_bot = [50, 0]
w_start_top = [0, 0]
city_sim(city_data, w_start_bot, w_start_top)
