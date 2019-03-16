import numpy as np

light_dict = {
    0: np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    1: np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]),
    2: np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]),
    3: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]),
    4: np.array([1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]),
    5: np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])
}


class Controller:
    def __init__(self, env, max_cars):
        self.max_cars = max_cars
        self.num_actions = 6
        self.env = env

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

    def reset(self):
        self.env.reset()
        return self.state

    def step(self, next_light_cfg):

        # Figure out if any lane has filled up
        done = False
        for num_cars in self.lane_state:
            if num_cars > self.max_cars:
                done = True

        # Progress simulation
        new_cars, num_cars_out = self.env.step(next_light_cfg)

        # Calculate net cars out of intersection
        reward = num_cars_out - len(new_cars)

        return [reward, done]

    @property
    def lane_state(self):
        return tuple([lane.num_cars for lane in self.env.lanes])
