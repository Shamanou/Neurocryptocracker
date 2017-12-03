#! /usr/bin/env python

import json
from tgym.envs import SpreadTrading
from tgym.gens import CSVStreamer
from dqnagent import DQNAgent
from datetime import timedelta
import sys
import os.path

market = sys.argv[1]

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
data = []

# from generators.tickergenerator import TickerGenerator
# Instantiating the environmnent
generator = CSVStreamer(filename="data/"+market+"-history.csv")
episodes =3800
episode_length = 400
trading_fee = .2
time_fee = 0
history_length = 2

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
action_size = len(SpreadTrading._actions)
train_interval = 10
learning_rate = 0.001

if not os.path.isfile("./model."+market+".h5" ): 
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

    # Warming up the agent
    for _ in range(memory_size):
        action = agent.act(state)
        next_state, reward, done, _ = environment.step(action)
        agent.observe(state, action, reward, next_state, done, warming_up=True)
    # Training the agent
    for ep in range(episodes):
        state = environment.reset()
        rew = 0
        for _ in range(episode_length):
            action = agent.act(state)
            next_state, reward, done, _ = environment.step(action)
            loss = agent.observe(state, action, reward, next_state, done)
            state = next_state
            rew += reward
        if loss:
            print("Ep:" + str(ep)
              + "| rew:" + str(round(rew, 2))
              + "| eps:" + str(round(agent.epsilon, 2))
              + "| loss:" + str(round(loss.history["loss"][0], 4)))
    # saving the agent
    agent.brain.save_weights("model."+market+".h5", True)
    with open('model.'+market+'.json', 'w+') as outfile:
        json.dump(agent.brain.get_config(), outfile)
    # Running the agent
    done = False
    state = environment.reset()
    while not done:
        action = agent.act(state)
        state, _, done, info = environment.step(action)
        if 'status' in info and info['status'] == 'Closed plot':
            done = True
#         else:
#             environment.render()
