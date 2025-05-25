import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

class RotatingIDM:
    def __init__(self):
        pass

    def run(self):
        print("Running PPO algorithm...")