import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv


class FCFS:
    def __init__(self):
        # 初始化参数，例如环境、网络结构、超参数等
        pass

    def run(self):
        print("Running PPO algorithm...")
        # 训练逻辑写在这里