#! /usr/bin/env python
'''
Created on Oct 29, 2017

@author: Shamanou van Leeuwen
'''

import json
from tgym.envs import SpreadTrading
from cexapi import API
from keras.models import Sequential
import sys
from generators.generator import Generator
from dqnagent import DQNAgent

market = sys.argv[1]
secret = sys.argv[2]
key = sys.argv[3]
userid = sys.argv[4]

model = Sequential.from_config(json.load(open('model.'+market+'.json', 'r')))
model.load_weights('model.'+market+'.h5')

api = API(userid,key,secret)

episodes =7600
episode_length = 200
trading_fee = .2
time_fee = 0
history_length = 5

# Instantiating the environmnent
generator = Generator(market=market[:3])
environment = SpreadTrading(spread_coefficients=[1],
                                data_generator=generator,
                                trading_fee=trading_fee,
                                time_fee=time_fee,
                                history_length=history_length)
state = environment.reset()

# Instantiating the agent
memory_size = 3000
state_size = len(state)
gamma = 0.96
epsilon_min = 0.01
batch_size = 64
action_size = len(environment._actions)
train_interval = 10
learning_rate = 0.001


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
actions = ['buy','hold','sell']

while not done:
    action = agent.act(state)
    state, _, done, info = environment.step(action)
    if 'status' in info and info['status'] == 'Closed plot':
        done = True
    balance_X = api.balance()[market[3:]]
    balance_BTC = api.balance()["BTC"]
    action_label = actions[action.index(1)]
    if action_label == "buy":
        api.place_market_order(action_label, balance_X, market+'/BTC')
    elif action_label == "sell":
        api.place_market_order(action_label, balance_BTC, market+'/BTC')
#    print action, state, _, done, info 
