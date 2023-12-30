import numpy as np
import random as rd
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import sparse
import networkx as nx
import copy
from datetime import datetime as dt


city_data = [(3.5, 5), (2, 5.5), (3, 5.5), (4.5, 5.5), (3.5, 6), (1, 6.5), (2, 6.5), (3, 6.5), (3, 7.5), (3.5, 7),
             (4.5, 7), (3, 8.5)]


class Road:
    def __init__(self, num: int, max_capacity_to: int, actual_capacity_to: int, max_capacity_out: int,
                 actual_capacity_out: int, to: [], out: [], p1: int, p2: int):
        self.num = num
        self.max_cap_to = max_capacity_to
        self.act_cap_to = actual_capacity_to
        self.busy_to = actual_capacity_to >= max_capacity_to
        self.max_cap_out = max_capacity_out
        self.act_cap_out = actual_capacity_out
        self.busy_out = actual_capacity_out >= max_capacity_out
        self.to = to
        self.out = out
        self.p1 = p1
        self.p2 = p2

    def busy_to_print(self):
        print("ATTENTION! The road from", self.p1, "to", self.p2, "is now busy with",
              self.act_cap_to, "cars on it")

    def busy_out_print(self):
        print("ATTENTION! The road from", self.p2, "to", self.p1, "is now busy with",
              self.act_cap_to, "cars on it")


def cross():
    return


def wedges(roads_list, mat_to, mat_out):
    for road in roads_list:
        pos1 = road.p1
        pos2 = road.p2
        mat_to[pos1][pos2] = road.act_cap_to
        mat_to[pos2][pos1] = road.act_cap_to
        mat_out[pos1][pos2] = road.act_cap_out
        mat_out[pos2][pos1] = road.act_cap_out
    return mat_to, mat_out


def city_sim(city_data, w0_3_edge, w11_8_edge, start_tick=0, stop_tick=6, tickrate=1, bot_stop=1, top_stop=1):
    N = len(city_data)
    w_plus = np.empty((N, N))
    w_min = np.empty((N, N))
    income0 = w0_3_edge[0]
    income1 = w11_8_edge[1]
    road0cap_to = w0_3_edge[0]
    road1cap_to = 0
    road0cap_out = 0
    road1cap_out = 0
    road2cap_to = 0
    road2cap_out = 0
    road3cap_to = 0
    road3cap_out = 0
    road4cap_to = 0
    road4cap_out = 0
    road5cap_to = 0
    road5cap_out = 0
    road6cap_to = 0
    road6cap_out = 0
    road7cap_to = 0
    road7cap_out = 0
    road8cap_to = 0
    road8cap_out = 0
    road9cap_to = 0
    road9cap_out = 0
    road10cap_to = 0
    road10cap_out = 0
    road11cap_to = 0
    road11cap_out = 0
    road12cap_to = 0
    road12cap_out = 0
    road13cap_to = 0
    road13cap_out = 0
    road14cap_to = 0
    road14cap_out = 0
    road15cap_to = 0
    road15cap_out = w11_8_edge[1]
    roads = [Road(0, 100, road0cap_to, 100, road0cap_out, [1], [], 0, 3),
             Road(1, 100, road1cap_to, 100, road1cap_out, [2, 3, 4], [0], 3, 4),
             Road(2, 100, road2cap_to, 100, road2cap_out, [5, 6], [1, 3, 4], 4, 2),
             Road(3, 3, road3cap_to, 100, road3cap_out, [5, 7, 8], [1, 2, 4], 4, 7),
             Road(4, 100, road4cap_to, 100, road4cap_out, [9], [1, 2, 3], 4, 10),
             Road(5, 100, road5cap_to, 100, road5cap_out, [3, 7, 8], [2, 6], 2, 7),
             Road(6, 100, road6cap_to, 100, road6cap_out, [11, 12], [2, 5], 2, 1),
             Road(7, 100, road7cap_to, 100, road7cap_out, [11, 13], [3, 5, 8], 7, 6),
             Road(8, 100, road8cap_to, 100, road8cap_out, [10, 14, 15], [3, 5, 7], 7, 8),
             Road(9, 100, road9cap_to, 100, road9cap_out, [10], [4], 10, 9),
             Road(10, 100, road10cap_to, 100, road10cap_out, [8, 14, 15], [9], 9, 8),
             Road(11, 100, road11cap_to, 100, road11cap_out, [7, 13], [6, 12], 1, 6),
             Road(12, 100, road12cap_to, 100, road12cap_out, [13, 14], [11, 6], 1, 5),
             Road(13, 100, road13cap_to, 100, road13cap_out, [12, 14], [11, 7], 6, 5),
             Road(14, 100, road14cap_to, 100, road14cap_out, [8, 10, 15], [12, 13], 5, 8),
             Road(15, 100, road15cap_to, 100, road15cap_out, [], [8, 10, 14], 8, 11)]
    roads_output = copy.deepcopy(roads)
    crosses_transfer = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    #     cross number   0   1   2   3   4   5   6   7   8   9  10  11
    for tick in range(stop_tick - start_tick):
        # every tick 10 cars can transfer through any cross
        transfer_cars = 20
        if tick != 0:
            road0cap_to = roads_output[0].act_cap_to + income0
            road1cap_to = roads_output[1].act_cap_to
            road0cap_out = roads_output[0].act_cap_out
            road1cap_out = roads_output[1].act_cap_out
            road2cap_to = roads_output[2].act_cap_to
            road2cap_out = roads_output[2].act_cap_out
            road3cap_to = roads_output[3].act_cap_to
            road3cap_out = roads_output[3].act_cap_out
            road4cap_to = roads_output[4].act_cap_to
            road4cap_out = roads_output[4].act_cap_out
            road5cap_to = roads_output[5].act_cap_to
            road5cap_out = roads_output[5].act_cap_out
            road6cap_to = roads_output[6].act_cap_to
            road6cap_out = roads_output[6].act_cap_out
            road7cap_to = roads_output[7].act_cap_to
            road7cap_out = roads_output[7].act_cap_out
            road8cap_to = roads_output[8].act_cap_to
            road8cap_out = roads_output[8].act_cap_out
            road9cap_to = roads_output[9].act_cap_to
            road9cap_out = roads_output[9].act_cap_out
            road10cap_to = roads_output[10].act_cap_to
            road10cap_out = roads_output[10].act_cap_out
            road11cap_to = roads_output[11].act_cap_to
            road11cap_out = roads_output[11].act_cap_out
            road12cap_to = roads_output[12].act_cap_to
            road12cap_out = roads_output[12].act_cap_out
            road13cap_to = roads_output[13].act_cap_to
            road13cap_out = roads_output[13].act_cap_out
            road14cap_to = roads_output[14].act_cap_to
            road14cap_out = roads_output[14].act_cap_out
            road15cap_to = roads_output[15].act_cap_to
            road15cap_out += roads_output[15].act_cap_out
            roads = [Road(0, 100, road0cap_to, 100, road0cap_out, [1], [], 0, 3),
                     Road(1, 100, road1cap_to, 100, road1cap_out, [2, 3, 4], [0], 3, 4),
                     Road(2, 3, road2cap_to, 100, road2cap_out, [5, 6], [1, 3, 4], 4, 2),
                     Road(3, 4, road3cap_to, 100, road3cap_out, [5, 7, 8], [1, 2, 4], 4, 7),
                     Road(4, 10, road4cap_to, 100, road4cap_out, [9], [1, 2, 3], 4, 10),
                     Road(5, 100, road5cap_to, 1, road5cap_out, [3, 7, 8], [2, 6], 2, 7),
                     Road(6, 100, road6cap_to, 100, road6cap_out, [11, 12], [2, 5], 2, 1),
                     Road(7, 100, road7cap_to, 100, road7cap_out, [11, 13], [3, 5, 8], 7, 6),
                     Road(8, 100, road8cap_to, 100, road8cap_out, [10, 14, 15], [3, 5, 7], 7, 8),
                     Road(9, 100, road9cap_to, 100, road9cap_out, [10], [4], 10, 9),
                     Road(10, 100, road10cap_to, 100, road10cap_out, [8, 14, 15], [9], 9, 8),
                     Road(11, 100, road11cap_to, 100, road11cap_out, [7, 13], [6, 12], 1, 6),
                     Road(12, 100, road12cap_to, 100, road12cap_out, [13, 14], [11, 6], 1, 5),
                     Road(13, 100, road13cap_to, 100, road13cap_out, [12, 14], [11, 7], 6, 5),
                     Road(14, 100, road14cap_to, 100, road14cap_out, [8, 10, 15], [12, 13], 5, 8),
                     Road(15, 100, road15cap_to, 100, road15cap_out, [], [8, 10, 14], 8, 11)]
            roads_output = copy.deepcopy(roads)
            for road_num in range(16):
                if roads[road_num].busy_to:
                    roads[road_num].busy_to_print()
                if not roads[road_num].to:
                    True
                else:
                    transfer_cars = crosses_transfer[roads[road_num].p2]
                    cars_from_to_int = roads[road_num].act_cap_to // transfer_cars
                    cars_from_to_rem = roads[road_num].act_cap_to % transfer_cars
                    if cars_from_to_int > 0:
                        cars_from_to = transfer_cars
                    else:
                        cars_from_to = cars_from_to_rem
                    cars_left_to = roads_output[road_num].act_cap_to - cars_from_to
                    cars_plus_to = cars_from_to % len(roads[road_num].to)
                    cars_from_to = cars_from_to // len(roads[road_num].to)
                    cars_add = 0
                    for cross_road in roads[road_num].to:
                        cars_left_to += cars_add
                        cars_add = 0
                        if roads[road_num].p2 != roads[cross_road].p2:
                            if roads[cross_road].act_cap_to + cars_from_to + cars_plus_to < roads[
                                cross_road].max_cap_to:
                                roads_output[cross_road].act_cap_to = roads_output[
                                                                          cross_road].act_cap_to + cars_from_to + cars_plus_to
                                cars_plus_to -= cars_plus_to
                                roads_output[road_num].act_cap_to = cars_left_to
                            else:
                                cars_add = -roads_output[cross_road].max_cap_to + (
                                        roads_output[cross_road].act_cap_to + cars_from_to + cars_plus_to)
                                cars_plus_to -= cars_plus_to
                                roads_output[cross_road].act_cap_to = roads_output[cross_road].max_cap_to
                        else:
                            if roads[cross_road].act_cap_out + cars_from_to + cars_plus_to < roads[
                                cross_road].max_cap_out:
                                roads_output[cross_road].act_cap_out = roads_output[
                                                                           cross_road].act_cap_out + cars_from_to + cars_plus_to
                                cars_plus_to -= cars_plus_to
                                roads_output[road_num].act_cap_to = cars_left_to
                            else:
                                cars_add = -roads_output[cross_road].max_cap_out + (
                                        roads_output[cross_road].act_cap_out + cars_from_to + cars_plus_to)
                                cars_plus_to -= cars_plus_to
                                roads_output[cross_road].act_cap_out = roads_output[cross_road].max_cap_out
                if roads[road_num].busy_out:
                    roads[road_num].busy_out_print()
                else:
                    if not roads[road_num].out:
                        True
                    else:
                        transfer_cars = crosses_transfer[roads[road_num].p1]
                        cars_from_out_int = roads[road_num].act_cap_out // transfer_cars
                        cars_from_out_rem = roads[road_num].act_cap_out % transfer_cars
                        if cars_from_out_int > 0:
                            cars_from_out = transfer_cars
                        else:
                            cars_from_out = cars_from_out_rem
                        cars_left_out = roads_output[road_num].act_cap_out - cars_from_out
                        cars_plus_out = cars_from_out % len(roads[road_num].out)
                        cars_from_out = cars_from_out // len(roads[road_num].out)
                        cars_add = 0
                        for cross_road in roads[road_num].out:
                            cars_left_out += cars_add
                            cars_add = 0
                            if roads[road_num].p1 != roads[cross_road].p1:
                                if roads[cross_road].act_cap_out + cars_from_out + cars_plus_out < roads[
                                    cross_road].max_cap_out:
                                    roads_output[cross_road].act_cap_out = roads_output[
                                                                               cross_road].act_cap_out + cars_from_out + cars_plus_out
                                    cars_plus_out -= cars_plus_out
                                    roads_output[road_num].act_cap_out = cars_left_out
                                else:
                                    cars_add = -roads_output[cross_road].max_cap_out + (
                                            roads_output[cross_road].act_cap_out + cars_from_out + cars_plus_out)
                                    cars_plus_out -= cars_plus_out
                                    roads_output[cross_road].act_cap_out = roads_output[cross_road].max_cap_out
                            else:
                                if roads[cross_road].act_cap_out + cars_from_out + cars_plus_out < roads[
                                    cross_road].max_cap_out:
                                    roads_output[cross_road].act_cap_out = roads_output[
                                                                               cross_road].act_cap_out + cars_from_out + cars_plus_out
                                    cars_plus_out -= cars_plus_out
                                    roads_output[road_num].act_cap_out = cars_left_out
                                else:
                                    cars_add = -roads_output[cross_road].max_cap_to + (
                                            roads_output[cross_road].act_cap_to + cars_from_out + cars_plus_out)
                                    cars_plus_out -= cars_plus_out
                                    roads_output[cross_road].act_cap_to = roads_output[cross_road].max_cap_to
        for road in roads_output:
            print("The road from", road.p1, "to", road.p2, "is now busy for",
                  round(100 * road.act_cap_to / road.max_cap_to, 1), "%")
            print("The road from", road.p2, "to", road.p1, "is now busy for",
                  round(100 * road.act_cap_out / road.max_cap_out, 1), "%")
        print("Tick = ", tick)
        w_plus, w_min = wedges(roads_output, w_plus, w_min)
        w8_9_edge = int(w_plus[9][8]), int(w_min[8][9])
        w9_10_edge = int(w_plus[10][9]), int(w_min[9][10])
        w10_4_edge = int(w_plus[4][10]), int(w_min[10][4])
        w4_3_edge = int(w_plus[3][4]), int(w_min[4][3])
        w2_4_edge = int(w_plus[4][2]), int(w_min[2][4])
        w1_2_edge = int(w_plus[2][1]), int(w_min[1][2])
        w1_5_edge = int(w_plus[1][5]), int(w_min[5][1])
        w1_6_edge = int(w_plus[1][6]), int(w_min[6][1])
        w6_7_edge = int(w_plus[7][6]), int(w_min[7][6])
        w2_7_edge = int(w_plus[2][7]), int(w_min[2][7])
        w4_7_edge = int(w_plus[4][7]), int(w_min[4][7])
        w7_8_edge = int(w_plus[7][8]), int(w_min[7][8])
        w5_8_edge = int(w_plus[5][8]), int(w_min[5][8])
        w5_6_edge = int(w_plus[5][6]), int(w_min[5][6])
        w0_3_edge = int(w_plus[0][3]), int(w_min[0][3])
        w11_8_edge = int(w_plus[11][8]), int(w_min[11][8])
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
        #labels = {e: city.edges[e]['score'] for e in city.edges}
        imname = str(tick)+"_step"+".png"
        plt.savefig(imname)


w_start_bot = [20, 0]
w_start_top = [0, 0]
city_sim(city_data, w_start_bot, w_start_top)
