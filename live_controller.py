from threading import Thread
import time
import numpy as np

from db import Db
from environment import TrafficEnv

light_dict = {
    0: np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    1: np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]),
    2: np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]),
    3: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]),
    4: np.array([1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]),
    5: np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])
}


class Controller:
    def __init__(self, policy, max_cars):
        self.max_cars = max_cars
        self.policy = policy
        self.db = Db()
        self.env = TrafficEnv()
        self.num_actions = 6
        self.stop = False

    def step(self, next_light_cfg):

        # Figure out if any lane has filled up
        for num_cars in self.lane_state:
            if num_cars > self.max_cars:
                self.stop = True

        # Progress simulation
        spawn_list = self.db.get_traffic()
        new_cars, num_cars_out = self.env.step(next_light_cfg,
                                               spawn_list=spawn_list)
        return new_cars, num_cars_out

    @property
    def lane_state(self):
        return tuple([lane.num_cars for lane in self.env.lanes])

    @property
    def state(self):
        lanes = np.zeros(self.num_actions + 1)

        # Iterate through every configuration
        for light_cfg in range(self.num_actions):
            num_cars = 0
            green_lanes = light_dict[light_cfg]

            # Iterate through lanes in a config
            for lane_num, is_green in enumerate(green_lanes):
                num_cars += self.env.lanes[lane_num].num_cars * is_green

            lanes[light_cfg] = num_cars

        lanes[-1] = self.env.light_cfg
        return tuple(lanes)

    def do_loop(self):
        event_num = 0
        while not self.stop:
            best_action = np.argmax(self.policy[self.state])
            new_cars, num_cars_out = self.step(best_action)
            self.db.add_event(f'event{event_num}', best_action, new_cars)
            event_num += 1
            print(f'Event{event_num}: Light Config - {best_action}, '
                  f'New Cars - {new_cars}')
            time.sleep(1)

    def start(self):
        self.env.reset()
        self.stop = False
        Thread(target=self.do_loop, args=[self])

    def stop(self):
        self.stop = True
