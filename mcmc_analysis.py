import json

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

def str_to_dict(state):
    state = state[1:-1]
    
    state = state.split(',')
    
    new_state = {}
    
    for item in state:
        key, val = item.split(':')
        key = key.strip()[1:-1]
        val = val.strip()
        if val == 'False':
            val = False
        elif val == 'True':
            val == True
        else:
            val = int(val)
        new_state[key] = val
        
    return new_state
        
        

def plot_players_loc_heatmap(state_action_dict):
    key_locations = []
    for state_action_key in state_action_dict.keys():
        state_action_key = str_to_dict(state_action_key)
        if state_action_key['has_scored']:
            locations = get_loc_from_state(state_action_key)[:-1]
            key_locations.append(locations)
    
    unique_locs, counts = np.unique(key_locations, axis=0, return_counts=True)
    
    heat_map = np.zeros((11, 11))
    
    for i in range(len(unique_locs)):
        loc = (unique_locs[i] + 5).astype(np.int16)
        for j in range(len(loc)):
            heat_map[loc[j, 1], loc[j, 0]] += counts[i]
    
    sns.heatmap(heat_map, annot=False, cbar=False)
    plt.axis('off')
    plt.show()
    

def plot_players_loc_value_heatmap(state_action_dict):
    key_locations = []
    values = []
    for state_action_key in state_action_dict.keys():
        values.append(state_action_dict[state_action_key])
        state_action_key = str_to_dict(state_action_key)
        locations = get_loc_from_state(state_action_key)[:-1]
        key_locations.append(locations)
    
    heat_map = np.zeros((11, 11))
    
    for i in range(len(key_locations)):
        loc = (key_locations[i] + 5).astype(np.int16)
        for j in range(len(loc)):
            heat_map[loc[j, 1], loc[j, 0]] += values[i]
    
    sns.heatmap(heat_map, annot=False, cbar=False)
    plt.axis('off')
    plt.show()


def bar_plot(state_action_dict):
    heights = [len(state_action_dict.keys()), 0]
    for state_action_key in state_action_dict.keys():
        state_action_key = str_to_dict(state_action_key)
        if state_action_key['has_scored']:
            heights[1] += 1
    
    print(heights[1])
    plt.bar(['All States', 'Goal States'], heights, color=['blue', 'red'])
    plt.show()
    
    


for i in range(1, 6):
    with open(f'mcmc{i}.json', 'r') as handle:
        data = json.load(handle)
        

    # data_sorted = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}

    # print(len(data_sorted.keys()))

    plot_players_loc_heatmap(data)
    plot_players_loc_value_heatmap(data)
    bar_plot(data)