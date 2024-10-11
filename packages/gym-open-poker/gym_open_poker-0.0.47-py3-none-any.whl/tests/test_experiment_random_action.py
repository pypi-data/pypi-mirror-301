import gym
import gym_open_poker
import numpy as np
import yaml
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # This is for github actions

env = gym.make("gym_open_poker/OpenPoker-v0")
# env = CardDistLow(gym.make("open_poker/OpenPoker-v0", **config_dict))
observation, info = env.reset(seed=42)
print('============================')
print('---observation---')
print(observation)
print('---info---')
print(info)

count_step = 0

while (True):
    print('============================')
    print('Enter your action:')
    # user_action = input()
    action_mask = info['action_masks'].astype(bool)
    all_action_list = np.array(list(range(6)))
    user_action = np.random.choice(all_action_list[action_mask], size=1).item()

    if int(user_action) not in range(6):
        print('It is not a valid action, current value = ' + user_action)
        continue
    # print('----------------')
    observation, reward, terminated, truncated, info = env.step(int(user_action))
    print('---observation---')
    print(observation)
    print('---reward---')
    print(reward)
    print('---info---')
    print(info)
    if truncated:
        print('meet termination condition! Over!')
        break
    if terminated:
        if observation['player_status'][observation['position'][1]] == 1:
            print('WINNNN!')
        else:
            print('LOST!')
        break
    count_step += 1
    if count_step == 10:
        break
env.close()
