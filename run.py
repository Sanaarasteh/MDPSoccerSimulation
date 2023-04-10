import numpy as np
import mplsoccer as mpl
import matplotlib.pyplot as plt

from pyRDDLGym import RDDLEnv
from pyRDDLGym.Policies.Agents import RandomAgent



def check_for_termination(state):
    has_ball_keys = list(state.keys())
    has_ball_keys = list(filter(lambda x: x.startswith('has_ball'), has_ball_keys))
    
    terminate = True
    
    for key in has_ball_keys:
        if state[key]:
            terminate = False
    
    return terminate

def get_termination_type(state, prev_action):
    if state['has_scored']:
        print('[!] Episode terminated with a scored goal!')
    else:
        if 'shoot' in list(prev_action.keys())[0]:
            if list(prev_action.values())[0] == 1:
                print('[!] Episode terminated with a missed shot!')
            else:
                print('[!] Episode terminated with a lost-possession!')
        elif 'pass' in list(prev_action.keys())[0]:
            if list(prev_action.values())[0] == 1:
                print('[!] Episode terminated with an intercepted pass!')
            else:
                print('[!] Episode terminated with a lost-possession!')
        else:
            print('[!] Episode terminated with a lost-possession!')


def get_loc_from_state(state):
    # get the number of players
    n_players = int(len(list(filter(lambda x: x.startswith('player_pos'), list(state.keys())))) / 2)
    
    locations = np.zeros((n_players + 1, 2))
    
    # initially we assume that the ball is out of bounds
    locations[-1, :] = -10
    
    # fill in the coordinates of the players
    for i in range(n_players):
        locations[i, 0] = state[f'player_pos_x___p{i + 1}']
        locations[i, 1] = state[f'player_pos_y___p{i + 1}']
    
    # find and fill the location of the ball
    for i in range(n_players):
        if state[f'has_ball___p{i + 1}']:
            locations[-1, 0] = state[f'player_pos_x___p{i + 1}']
            locations[-1, 1] = state[f'player_pos_y___p{i + 1}']
            break
        
    return locations


def plot_players_locations(locations):
    pitch = mpl.Pitch(pitch_type='skillcorner',
                      pitch_length=134, 
                      pitch_width=68, 
                      axis=True, 
                      label=True)
    _, ax = pitch.draw(figsize=(9, 6))
    
    players_locations = locations[:-1]
    
    pitch.scatter(players_locations[:, 0], players_locations[:, 1], ax=ax, facecolor='blue', s=5, edgecolor='k')
    # pitch.scatter([locations[-1, 0]], [locations[-1, 1]], ax=ax, facecolor='yellow', s=3, edgecolor='k')
    plt.show()
        
    

env = RDDLEnv.RDDLEnv(domain='domain2.rddl', instance='instance5.rddl', debug=False)
agent = RandomAgent(action_space=env.action_space, num_actions=env.numConcurrentActions)

states = []


total_reward = 0
state = env.reset()
prev_action = None
for step in range(env.horizon):
    # env.render()
    action = agent.sample_action()
    next_state, reward, done, info = env.step(action)
    total_reward += reward
    print()
    print('step       = {}'.format(step))
    print('state      = {}'.format(state))
    # print('next state = {}'.format(next_state))
    # print('reward     = {}'.format(reward))
    if check_for_termination(state):
        print('lost_possession = {}'.format(next_state['lost_possession']))
        get_termination_type(state, prev_action)    
        break
    
    print('action     = {}'.format(action))
    states.append(state)
    prev_action = action
    
    state = next_state
    if done:
        break
print("episode ended with reward {}".format(total_reward))
env.close()

# get_loc_from_state(states[-1])

# for state in states:
#     plot_players_locations(get_loc_from_state(state))
