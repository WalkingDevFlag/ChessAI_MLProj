import gym
import gym_chess
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecEnvWrapper, DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
import os
import shimmy

env = gym.make('Chess-v0')

done = True

for step in range(100000):
    if done:
        env.reset()
        done = False
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()
env.close()

