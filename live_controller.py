from db import Db
from environment import TrafficEnv


class Controller:
    def __init__(self, policy, max_cars):
        self.max_cars = max_cars
        self.db = Db()
        self.env = TrafficEnv()

    def step(self, next_light_cfg):

        # Figure out if any lane has filled up
        done = False
        for num_cars in self.lane_state:
            if num_cars > self.max_cars:
                done = True

        # Progress simulation
        spawn_list = self.db.get_traffic()
        new_cars, num_cars_out = self.env.step(next_light_cfg,
                                               spawn_list=spawn_list)

        # Calculate net cars out of intersection
        reward = num_cars_out - len(new_cars)

        return [reward, done]

    @property
    def lane_state(self):
        return tuple([lane.num_cars for lane in self.env.lanes])
