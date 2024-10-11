"""
This testing method was deprecated, as the previously tested novelty will still affect the current one.
Specifically, the previous novelty modified the imported modules using monkey patching. Two methods to conquer this problem:
1. re-import all original module
2. separate every novelty testing files

The second method was chosen, as we might need to test other unit tests, so it is better to isolate every testing file. 
"""

import gym

# import gym_open_poker
import yaml
import os
from gym_open_poker.envs.poker_util.novelty_generator import NoveltyGenerator
import numpy as np
import unittest
import pytest

import importlib


testing_arg = [
    "CardDistHigh",
    "CardDistLow",
    "Card1",
    "Action1",
    "RANDOM",
    "Environment1",
    "Environment2",
    "Agent1",
    "Agent2",
    "Agent3",
    "Event1",
    "Rule2",
    "Rule3",
    "Event2",
    "Card2",
    "Rule4",
    "Card3",
]


@pytest.mark.parametrize("novelty_name", testing_arg)
def test_novelty(novelty_name):
    with open(f"./tests/config/config_{novelty_name}.yaml", "r") as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    log_file_path = config_dict["log_file_path"]

    # original environment
    env = gym.make("gym_open_poker/OpenPoker-v0", **config_dict)
    # env = gym.make("gym_open_poker/OpenPoker-v0")

    # novelty injection
    ng = NoveltyGenerator()

    # print out supported novelies
    # print(ng.get_support_novelties())
    # injecting
    if "novelty_list" in config_dict and config_dict["novelty_list"] and len(config_dict["novelty_list"]) > 0:
        env = ng.inject(env, config_dict["novelty_list"])

    # start gaming
    observation, info = env.reset(seed=65)

    while True:
        print("============================")
        action_mask = info["action_masks"].astype(bool)
        all_action_list = np.array(list(range(6)))
        user_action = np.random.choice(all_action_list[action_mask], size=1).item()
        # print('----------------')
        observation, reward, terminated, truncated, info = env.step(int(user_action))
        # print("---observation---")
        # print(observation)
        # print("---reward---")
        # print(reward)
        # print("---info---")
        # print(info)
        if truncated:
            print("Meet termination condition! Over!")
            break
        if terminated:
            if observation["player_status"][observation["position"][1]] == 1:
                print("WINNNN!")
            else:
                if reward == -999:
                    print("Use an invalid move! LOST!")
                else:
                    print("LOST!")
            break
    env.close()
    assert terminated or truncated
    assert os.path.isfile(log_file_path)
