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
    4: np.array([1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]),
    5: np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])
}


class TrafficEnv:
    def __init__(self):
        self.lanes = [Lane()] * 12
        self.light_cfg = 0
        self.reset()

        # By default spawn a new car 30% of the time
        # ordered by Roads, N, E, S, W
        self.car_density = [0.4 for _ in range(4)]

    def reset(self):
        self.lanes = [Lane() for _ in range(12)]
        self.light_cfg = 0

    def step(self, next_light_cfg):
        num_cars_out = self.release_cars(next_light_cfg)
        new_cars = self.spawn_cars()
        self.light_cfg = next_light_cfg
        return new_cars, num_cars_out

    def spawn_cars(self):
        new_cars = []
        for road_num in range(4):
            spawn_prob = self.car_density[road_num]
            if np.random.random() < spawn_prob:
                # Pick most empty lane out of the 3 lanes
                empty_lane = self.get_most_empty_lane_num(road_num)
                turn_direction = self.get_direction(empty_lane)
                self.lanes[empty_lane].add_car(Car(turn_direction))
                new_cars.append((empty_lane, turn_direction))

        return new_cars

    def get_most_empty_lane_num(self, road_num):
        lane_states = [lane.num_cars for lane in self.lanes]
        min_local_lane = np.argmin(lane_states[road_num * 3:road_num * 3 + 3])
        empty_lane_num = road_num * 3 + min_local_lane
        return empty_lane_num

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
        num_cars_out = 0
        old_config = light_dict[self.light_cfg]
        new_config = light_dict[next_cfg]
        open_lanes = np.multiply(old_config, new_config)

        for lane_num, release in enumerate(open_lanes):
            if release and self.lanes[lane_num].queue:
                self.lanes[lane_num].pop_car()
                num_cars_out += 1

        return num_cars_out



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
