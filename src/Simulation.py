import math
import random

import Optimisation
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

class Simulation:

    def __init__(self):
        self.transition_mat = None
        self.adjacent_mat = None
        self.items_mat = None
        self.rooms_mat = None
        self.users_mat = None
        self.path_hist = []
        self.user_queue = []
        self.time = 0   # timestep
        self.new_user_p = 0.5 # TODO make it a function of time

        # for visualization
        # {R1:(0,0,1,0), R4:(0,1,1,0,0,1)} is path encoding
        self.testpath = {
            "R1": (0, 0, 1, 0),
            "R4": (0, 1, 1, 0, 0, 1),
            "R6": (0, 0, 1, 1)
        }
        # set room center coordinates and corridor center coordinates
        self.room_centers = {
            "R1": [0, 0],
            "R2": [1, 0],
            "R3": [2, 0],
            "R4": [1, 1],
            "R5": [0, 2],
            "R6": [1, 2],
            "R7": [2, 2],
            "C1": [0, 1],  # corridors
            "C2": [2, 1]
        }

        self.load_data()

    def time_step(self):
        # Make new users
        if (np.random.random() > self.new_user_p):
            self.user_queue.append(self.generate_new_user())

        self.make_path()

        # current museum status
        self.visualize_museum()

        # step
        self.time += 1

    def make_path(self):
        """
        Makes a path for the new user
        :return: None
        """

        # Take a first user in a queue and generate a user's path Optimisation(all)
        user = self.user_queue.pop()
        paths = Optimisation.make_path(user)

        # select desired path
        path = self.choose_path(paths)

        # Add path to path_hist
        self.path_hist.append(path)

        # Visualize pareto front
        self.visualize_front(paths)

    def choose_path(self, paths):
        path = None
        # todo
        return path

    def generate_new_user(self):
        # preferences are over 3 categories
        # total time available is number in minutes
        # crowd preferences are bool: True is you hate crowds
        preferences = [int(random.random() * 2), int(random.random() * 2), int(random.random() * 2)]
        total_time = [int(random.random() * 180 + 30)]
        hates_crods = [int(random.random() * 2)]
        return preferences + total_time + hates_crods

    def visualize_museum(self):
        rooms = [ "R1", "R2", "R3", "R4", "R5", "R6", "R7" ]
        view_counts = {
            room: { 0: 0 } for room in rooms
        }

        # show background
        img = mpimg.imread('../data/museum_map.png')
        plt.imshow(img, extent=[-0.5, 2.5, -0.5, 2.5])

        #TODO for path in self.path_hist:
        orig_path = testpath # TODO = path
        path = testpath
        #d find path sequence
        visual_path = []
        first_path_point = path[0][0]

        for i, path_point in enumerate(path):
            path_point = path_point[0]
            if i != 0:
                # find path from first to this path point
                path = self.bfs(first_path_point, path_point)
                visual_path += path
                # print(first_path_point, path_point)
                # print(path)
                # print()
            first_path_point = path_point

        # get coordinates of all path points
        path_x = []
        path_y = []
        for node in visual_path:
            x, y = self.room_centers[node]
            path_x.append(x + random.random() * 0.2) # better visibility with noise
            path_y.append(y + random.random() * 0.2)

        # plot path
        plt.plot(path_x, path_y, "-")

        # get item view counts
        for room in orig_path:
            name, items = room
            for i, item in enumerate(items):
                if i not in view_counts[name]:
                    view_counts[name][i] = 1
                else:
                    view_counts[name][i] += item


        # plot visited objects
        for room in view_counts:
            name = room
            counts = view_counts[name]
            for i, count in enumerate(counts):
                x, y = self.room_centers[name]
                x += (i % 2) * 0.3
                y += (i/2 % 3 - 0.5) * 0.3
                plt.scatter(x, y, s=math.sqrt(count)*5)

        plt.show()


    def bfs(self, start, end):
        """
        From https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
        and edited to work with matrix represented graph
        :param start:
        :param end:
        :return:
        """
        # maintain a queue of paths
        queue = []
        # push the first path into the queue
        queue.append([start])
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1]
            # path found
            if node == end:
                return path
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for adjacent in self.make_candidates(node):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)

    def make_candidates(self, node):
        room_indices = {"R1": 0, "R2": 1, "R3": 2, "R4": 3, "R5": 4, "R6": 5, "R7": 6, "C1": 7, "C2": 8}
        index_rooms = {0: "R1", 1: "R2", 2: "R3", 3: "R4", 4: "R5", 5: "R6", 6: "R7", 7: "C1", 8: "C2"}
        cands = self.adjacent_mat[room_indices[node]]
        max = int(cands.max())
        candidates = []
        indices = np.argwhere(cands == max).flatten().tolist()
        for m in indices:
            candidate = index_rooms[m]
            candidates.append(candidate)
        return candidates

    def visualize_front(self, paths):
        """
        Generate plot of objective values
        :param paths: list[ tuple(path, obj_1, obj_2, ... ) ... ]
        :return: Null
        """
        objectives = [
            [ val for i, val in enumerate(path) if i != 0 ]
            for path in paths
        ]
        objectives = np.array(objectives, dtype=np.float).transpose()

        ax = plt.axes(projection='3d')
        ax.scatter(objectives[0], objectives[1])
        plt.show()
        input()
        return None

    def load_data(self):
        """
        Loads travel time matrices and item matrices
        :return: None
        """

        items_path = "../data/items.bin"
        travel_times_path = "../data/travel_time.bin"
        rooms_path = "../data/rooms.bin"
        adjacent_path = "../data/room_adjacent.bin"

        items_f = open(items_path)
        items_matrix = []
        for row in items_f:
            values = row.split(',')
            values = [int(v.strip()) for v in values]
            items_matrix.append(values)
        self.items_mat = np.array(items_matrix)

        travel_times_f = open(travel_times_path)
        travel_times_matrix = []
        for row in travel_times_f:
            values = row.split(',')
            values = [int(v.strip()) for v in values]
            travel_times_matrix.append(values)
        self.transition_mat = np.array(travel_times_matrix)

        rooms_f = open(rooms_path)
        rooms_matrix = []
        for row in travel_times_f:
            rooms_matrix.append(int(row))
        self.rooms_mat = np.array(rooms_matrix)

        adjacent_f = open(adjacent_path)
        adjacent_matrix = []
        for row in adjacent_f:
            values = row.split(' ')
            # skip comment
            if values[0] == '#': continue
            values = [int(v.strip()) for v in values]
            adjacent_matrix.append(values)
        self.adjacent_mat = np.array(adjacent_matrix)


# tests
if __name__ == '__main__':
    sim = Simulation()
    # print(sim.generate_new_user())

    #  [("R2", [1,0,0]),("R3", [0,1]),...] is path format
    testpath = [ ("R1", [1, 0, 0]),
                 ("R4", [0, 1, 1, 0]),
                 ("R6", [1, 0, 1]),
                 ("R5", [0, 0, 1, 1]) ]
    # sim.visualize_front(testpath)
    sim.visualize_museum()
