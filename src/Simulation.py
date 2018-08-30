import Optimisation
import numpy as np


class Simulation:

    def __init__(self):
        self.transition_mat = None
        self.items_mat = None
        self.rooms_mat = None
        self.users_mat = None
        self.path_hist = []
        self.user_queue = []
        self.time = 0   # timestep
        self.new_user_p = 0.5 # TODO make it a function of time

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
        user = None
        # todo
        return user

    def visualize_museum(self):
        # TODO
        return None

    def visualize_front(self, paths):
        # TODO
        return None

