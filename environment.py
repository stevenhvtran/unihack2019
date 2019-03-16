from collections import deque
import numpy as np

"""
The way that lanes work is that it goes from left lane, mid lane, right lane
then N -> E -> S -> W
1 is green light, 0 is red light
"""
light_dict = {
    0: np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    1: np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]),
    2: np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]),
    3: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]),
    4: np.array([0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
    5: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]),
    6: np.array([1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]),
    7: np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])
}


class TrafficEnv:
    def __init__(self):
        self.lanes = None
        self.light_cfg = None
        self.reset()

        # By default spawn a new car 30% of the time
        # ordered by Roads, N, E, S, W
        self.car_density = [0.3, 0.3, 0.3, 0.3]

    def reset(self):
        self.lanes = [Lane()] * 12
        self.light_cfg = 0

    def step(self, next_light_cfg):
        self.release_cars(next_light_cfg)
        new_cars = self.spawn_cars()
        self.light_cfg = next_light_cfg
        return new_cars

    def spawn_cars(self):
        new_cars = []
        # Do randomised spawns for simulator
        for lane_num, lane in enumerate(self.lanes):
            road_num = lane_num // 3
            if np.random.random() < self.car_density[road_num]:
                turn_direction = self.get_direction(lane_num)
                self.lanes[lane_num].add_car(Car(turn_direction))
                new_cars.append((lane_num, turn_direction))
        return new_cars

    def get_direction(self, lane_num):
        # Left turning lane
        if lane_num % 3:
            if np.random.random() < 0.5:
                turn_direction = 0
            else:
                turn_direction = 1

        # Handle middle lanes
        elif (lane_num + 1) % 3:
            turn_direction = 1

        # Handle right lanes
        else:
            turn_direction = 2

        return turn_direction

    def release_cars(self, next_cfg):
        old_config = light_dict[self.light_cfg]
        new_config = light_dict[next_cfg]
        open_lanes = np.multiply(old_config, new_config)

        for lane_num, release in enumerate(open_lanes):
            if release:
                self.lanes[lane_num].pop_car()


class Car:
    def __init__(self, direction):
        """
        :param direction: Indicates the direction the car is travelling in
            0: left
            1: straight
            2: right
        """
        self.direction = direction


class Lane:
    def __init__(self):
        self.queue = deque()

    def add_car(self, car):
        self.queue.append(car)

    def pop_car(self):
        if self.queue:
            self.queue.pop()

    @property
    def num_cars(self):
        return len(self.queue)
