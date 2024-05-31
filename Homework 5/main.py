import utils
import flappy_bird_gym
import random
import time
import math


class SmartFlappyBird:
    def __init__(self, iterations):
        self.Qvalues = utils.Counter()
        self.landa = 0.9
        self.epsilon = 0  # change to proper value
        self.alpha = 0.7  # change to proper value
        self.iterations = iterations

    def policy(self, state):
        # implement the policy
        return self.max_arg(state)

    @staticmethod
    def get_all_actions():
        return [0, 1]

    @staticmethod
    def convert_continuous_to_discrete(state):
        # implement the best way to convert continuous distance values to discrete values
        discrete_state = []
        discrete_state.append(math.floor(state[0] * 100) % 2)
        discrete_state.append(0 if state[1] >= -0.022 else (1 if state[1] > 0.5 else 2))

        return discrete_state

    def compute_reward(self, prev_info, new_info, done, observation):
        # implement the best way to compute reward base on observation and score
        
        if done:
            return -1 * 100
        reward = (new_info["score"] - prev_info["score"]) * (1 - abs(observation[0])) + (
            (1 - (new_info["score"] - prev_info["score"])) * (1 - abs(observation[1]))
        )
        return reward

    def get_action(self, state):
        # implement the best way to get action base on current state
        # you can use `utils.flip_coin` and `random.choices`

        if random.uniform(0, 1) < self.epsilon:
            return utils.flip_coin(self.epsilon)
        else:
            return self.policy(state)

    def maxQ(self, state):
        # return max Q value of a state
        return max(self.Qvalues[str(state), "False"], self.Qvalues[str(state), "True"])

    def max_arg(self, state):
        # return argument of the max q of a state
        discrete_state = self.convert_continuous_to_discrete(state)
        q1 = self.Qvalues[str(discrete_state), "False"]
        q2 = self.Qvalues[str(discrete_state), "True"]
        if q1 >= q2:
            return False
        else:
            return True

    def update(self, reward, state, action, next_state):
        # update q table
        discrete_state = self.convert_continuous_to_discrete(state)
        discrete_next_state = self.convert_continuous_to_discrete(next_state)
        newValue = (
            1 - self.alpha
        ) * self.Qvalues[str(discrete_state), str(action)] + self.alpha * (
            reward + self.landa * self.maxQ(discrete_next_state)
        )
        self.Qvalues[str(discrete_state), str(action)] = newValue

    def update_epsilon_alpha(self):
        # update epsilon and alpha base on iterations
        self.alpha = max(self.alpha - self.alpha / self.iterations , 0)
        self.epsilon = max(self.epsilon - self.epsilon /self.iterations, 0)

    def run_with_policy(self, landa):
        sum = 0
        self.landa = landa
        env = flappy_bird_gym.make("FlappyBird-v0")
        observation = env.reset()
        info = {"score": 0}
        for _ in range(self.iterations):
            while True:
                action = self.get_action(observation)  # policy affects here
                this_state = observation
                prev_info = info
                observation, reward, done, info = env.step(action)
                reward = self.compute_reward(prev_info, info, done, observation)
                self.update(reward, this_state, action, observation)
                if done:
                    observation = env.reset()
                    break
            self.update_epsilon_alpha()
            sum = sum + info["score"]
        print("Omid riazi", sum / self.iterations)
        env.close()

    def run_with_no_policy(self, landa):
        self.landa = landa
        # no policy test
        env = flappy_bird_gym.make("FlappyBird-v0")
        observation = env.reset()
        info = {"score": 0}
        while True:
            action = self.get_action(observation)
            prev_info = info
            observation, reward, done, info = env.step(action)
            reward = self.compute_reward(prev_info, info, done, observation)
            env.render()
            time.sleep(1 / 30)  # FPS
            if done:
                break
        env.close()

    def run(self):
        self.run_with_policy(1)
        while True:
            self.run_with_no_policy(1)


program = SmartFlappyBird(iterations=100)
program.run()
