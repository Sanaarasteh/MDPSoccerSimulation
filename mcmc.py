import json

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
        
    

def run_episode():
    env = RDDLEnv.RDDLEnv(domain='domain.rddl', instance='instance5.rddl')
    agent = RandomAgent(action_space=env.action_space, num_actions=env.numConcurrentActions)

    states = []

    total_reward = 0
    state = env.reset()
    
    for step in range(env.horizon):
        state_action = {}
        env.render()
        action = agent.sample_action()
        next_state, reward, _, _ = env.step(action)
        total_reward += reward
        # print()
        # print('step       = {}'.format(step))
        # print('state      = {}'.format(state))
        # print('next state = {}'.format(next_state))
        # print('reward     = {}'.format(reward))
        for key in state.keys():
            state_action[key] = state[key]
        for key in action.keys():
            state_action[key] = action[key]
            
        states.append(state_action)
        
        if check_for_termination(state):
            # print('lost_possession = {}'.format(next_state['lost_possession']))
            # get_termination_type(state, prev_action)    
            break
        
        # print('action     = {}'.format(action))
                
        state = next_state
    
    env.close()
    
    return states, total_reward


def all_visit_mcmc(num_iters=1000):
    state_action_values = {}
    state_action_counts = {}
    
    for itr in range(num_iters):
        print('Iteration: ', itr)
        state_actions, reward = run_episode()
        
        for state_action in state_actions:
            if str(state_action) in state_action_counts:
                state_action_counts[str(state_action)] += 1
                state_action_values[str(state_action)] += reward
            else:
                state_action_counts[str(state_action)] = 1
                state_action_values[str(state_action)] = reward
    
    print(len(state_action_values.keys()))
    # averaging the values
    for item in state_action_values.keys():
        state_action_values[item] /= state_action_counts[item]
    
    print('[*] Saving the results.')
    with open('mcmc.json', 'w') as handle:
        json.dump(state_action_values, handle)

if __name__ == '__main__':
    all_visit_mcmc(5000)
