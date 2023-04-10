
class InstanceInfo:
    def __init__(self, instance_path):
        with open(instance_path, 'r') as handle:
            self.instance_info = handle.read()
            
    
    def get_num_players(self):
        chunks = self.instance_info.split(';')
        
        for chunk in chunks:
            if chunk.strip().startswith('objects'):
                return len(chunk.split(','))
            
    def get_pitch_boundary(self):
        start_index = self.instance_info.index('LEFT_BOUNDARY_X')
        end_index = self.instance_info.index(';', start_index)
        left_x = int(self.instance_info[start_index + 17: end_index].strip())
        
        start_index = self.instance_info.index('RIGHT_BOUNDARY_X')
        end_index = self.instance_info.index(';', start_index)
        right_x = int(self.instance_info[start_index + 18: end_index].strip())
        
        start_index = self.instance_info.index('LOWER_BOUNDARY_Y')
        end_index = self.instance_info.index(';', start_index)
        lower_y = int(self.instance_info[start_index + 18: end_index].strip())
        
        start_index = self.instance_info.index('UPPER_BOUNDARY_Y')
        end_index = self.instance_info.index(';', start_index)
        upper_y = int(self.instance_info[start_index + 18: end_index].strip())
        
        return left_x, lower_y, right_x, upper_y
    
    def get_defense_offense_lines(self):
        start_index = self.instance_info.index('DEFENSE_AREA_X')
        end_index = self.instance_info.index(';', start_index)
        def_x = int(self.instance_info[start_index + 16: end_index].strip())
        
        start_index = self.instance_info.index('DEFENSE_AREA_Y')
        end_index = self.instance_info.index(';', start_index)
        def_y = int(self.instance_info[start_index + 16: end_index].strip())
        
        start_index = self.instance_info.index('OFFENSE_AREA_X')
        end_index = self.instance_info.index(';', start_index)
        off_x = int(self.instance_info[start_index + 16: end_index].strip())
        
        return def_x, def_y, off_x
        


if __name__ == '__main__':
    i = InstanceInfo('instance1.rddl')
    print(i.get_pitch_boundary()[3])