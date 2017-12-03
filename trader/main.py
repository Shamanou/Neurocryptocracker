#! /usr/bin/env python
'''
Created on Oct 29, 2017

@author: Shamanou van Leeuwen
'''

import json
from tgym.envs import SpreadTrading

from keras.models import Sequential
import sys
from generators.generator import Generator
from train import batch_size, episodes, episode_length, trading_fee, time_fee, history_length, gamma, epsilon_min, action_size, train_interval, learning_rate, memory_size, state_size
from src import DQNAgent

market = sys.argv[1]

model = Sequential.from_config(json.load(open('model.'+market+'.json', 'r')))
model.load_weights('model.'+market+'.h5')

# Instantiating the environmnent
generator = Generator()
environment = SpreadTrading(spread_coefficients=[1],
                                data_generator=generator,
                                trading_fee=trading_fee,
                                time_fee=time_fee,
                                history_length=history_length)
state = environment.reset()

# Instantiating the agent
agent = DQNAgent(state_size=state_size,
                     action_size=action_size,
                     memory_size=memory_size,
                     episodes=episodes,
                     episode_length=episode_length,
                     train_interval=train_interval,
                     gamma=gamma,
                     learning_rate=learning_rate,
                     batch_size=batch_size,
                     epsilon_min=epsilon_min)
agent.brain = model

done = False

while not done:
    action = agent.act(state)
    state, _, done, info = environment.step(action)
    if 'status' in info and info['status'] == 'Closed plot':
        done = True
