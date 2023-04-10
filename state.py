

class State:
    def __init__(self, rddl_state, environment_engine, pitch_dim, num_players, defense_offense_lines):
        self.state = rddl_state
        self.env_engine = environment_engine
        self.pitch_dim = pitch_dim
        self.num_players = num_players
        self.def_off = defense_offense_lines
    
    def move(self, action):
        next_state = self.env_engine.step(action)[0]
        
        return State(next_state, self.env_engine, self.pitch_dim, self.num_players, self.def_off)
    
    def is_game_over(self):
        has_ball_keys = list(self.state.keys())
        has_ball_keys = list(filter(lambda x: x.startswith('has_ball'), has_ball_keys))
        
        terminate = True
        
        for key in has_ball_keys:
            if self.state[key]:
                terminate = False
        
        return terminate
    
    def game_result(self):
        if self.state['has_scored']:
            return 1
        else:
            return -1
    
    def get_legal_actions(self):
        move_actions = ['move_up', 'move_left', 'move_right', 'move_down']
        shoot_action = 'shoot'
        pass_action = 'pass'
        
        legal_actions = []
        
        for move_action in move_actions:
            for i in range(self.num_players):
                action  = move_action + '___p' +  str(i + 1)
                if self.check_action_feasibility(action):
                    legal_actions.append({action: 1})
        
        for i in range(self.num_players):
            action = shoot_action + '___p' +  str(i + 1)
            if self.check_action_feasibility(action):
                    legal_actions.append({action: 1})
        
        for i in range(self.num_players):
            for j in range(self.num_players):
                if i != j:
                    action = pass_action + '___p' + str(i + 1) + '__p' + str(j + 1)
                    if self.check_action_feasibility(action):
                        legal_actions.append({action: 1})
        
        return legal_actions
        
    def check_action_feasibility(self, action):
        if action.startswith('move_up'):
            player = action[-2:]
            if int(self.state[f'player_pos_y___{player}']) + 1 <= self.pitch_dim[3]:
                return True
            else:
                return False
        elif action.startswith('move_down'):
            player = action[-2:]
            if int(self.state[f'player_pos_y___{player}']) - 1 >= self.pitch_dim[1]:
                return True
            else:
                return False
        elif action.startswith('move_left'):
            player = action[-2:]
            if int(self.state[f'player_pos_x___{player}']) - 1 >= self.pitch_dim[0]:
                return True
            else:
                return False
        elif action.startswith('move_right'):
            player = action[-2:]
            if int(self.state[f'player_pos_x___{player}']) + 1 <= self.pitch_dim[2]:
                return True
            else:
                return False
        elif action.startswith('pass'):
            player = action[7:9]
            if self.state[f'has_ball___{player}']:
                return True
            else:
                return False
        elif action.startswith('shoot'):
            player = action[-2:]
            if self.state[f'has_ball___{player}']:
                if self.check_in_offense(player):
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception('[!] Invalid action encountered')
        
    
    def check_in_offense(self, player):
        x = self.state[f'player_pos_x___{player}']
        y = self.state[f'player_pos_y___{player}']
        
        if x >= self.def_off[2] and y <= self.def_off[1] and y >= -self.def_off[1]:
            return True
        elif x >= self.def_off[2] and y <= self.def_off[1] + ((self.pitch_dim[3] - self.def_off[1]) / (self.pitch_dim[2] - self.def_off[2])) * (x - self.def_off[2]):
            if y >= -self.def_off[1] + ((self.pitch_dim[1] + self.def_off[1]) / (self.pitch_dim[2] - self.def_off[2])) * (x - self.def_off[2]):
                return True
            else:
                return False
        else:
            return False