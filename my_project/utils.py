import sys
sys.path.append('../')
from pycore.tikzeng import *

class ArchLayer:
    def __init__(self, size = 256, features = 32, caption = '', type='conv', long_conn_from=-1):
        self.size = size
        self.features = features
        self.caption = caption
        self.type = type
        self.long_conn_from = long_conn_from
        self.update()
        
    def update(self, width_exp=0.7, length_exp=0.7, name='l1', index=0):
        self.height = self.size**width_exp
        self.depth = self.size**width_exp
        self.width = self.features**length_exp
        self.radius = 2.5
        self.index = index
        self.name = name
        
    def __str__(self):
        return f'ArchLayer({self.size},{self.features},{self.caption})'

def to_arch(layers: list[ArchLayer], padding = 1, long_conn_padding = 6, width_exp=0.7, length_exp=0.7):
    arch = [
        to_head( '..' ),
        to_cor(),
        to_begin(),
    ]
    
    for i, l in enumerate(layers):
        if l.type == 'conv':
            l.update(name=f'conv{i+1}', width_exp=width_exp, length_exp=length_exp)
            arch.append(
                to_Conv(l.name, l.size, l.features, offset=f"({0 if i == 0 else padding},0,0)", to=f"({layers[i-1].name}-east)" if i > 0 else '(0,0,0)', height=l.height, depth=l.depth, width=l.width, caption=l.caption )
            )
        elif l.type == 'sum':
            l.update(name=f'sum{i+1}', width_exp=width_exp, length_exp=length_exp, index=i)
            arch.append(
                to_Sum(l.name, offset=f"({padding},0,0)", to=f"({layers[i-1].name}-east)" if i > 0 else '(0,0,0)', radius=l.radius),
            )
        
    for i in range(len(layers) - 1):
        arch.append(
            to_connection(layers[i].name, layers[i + 1].name),
        )
        
    long_conn_length_sorted_layers = sorted(layers, key = lambda l: l.index - l.long_conn_from if l.long_conn_from >= 0 else 999999)
    for i, l in enumerate(long_conn_length_sorted_layers):
        if l.long_conn_from < 0:
            break
        
        long_conn_name = l.name + f'lc{i}'
        #start_dummy_name =f"{long_conn_name}_dummy_s"
        dummy1_name =f"{long_conn_name}_dummy1"
        dummy2_name =f"{long_conn_name}_dummy2"
        end_dummy_name =f"{long_conn_name}_dummy_e"
        arch.extend([
            # Long conn tensor vis
            to_Conv(long_conn_name, l.size, l.features, offset=f"({padding*2},-{long_conn_padding*(i+1)},0)", to=f"({layers[l.long_conn_from].name}-east)", height=l.height, depth=l.depth, width=l.width, caption=l.caption ),
            
            # Dummy nodes
            to_Pool(dummy1_name, offset=f"(0,-{long_conn_padding*(i+1)},0)", to=f"({layers[l.long_conn_from].name}-east)", height=0, depth=0, width=0, opacity=0 ),
            to_Pool(dummy2_name, offset=f"({l.radius / 5},-{long_conn_padding*(i+1)},0)", to=f"({l.name}-west)", height=0, depth=0, width=0, opacity=0 ),
            to_Pool(end_dummy_name, offset=f"({padding - l.radius / 5},{-l.radius / 5},0)", to=f"({l.name}-west)", height=0, depth=0, width=0, opacity=0 ),
            
            # Conns
            to_connection(layers[l.long_conn_from].name, dummy1_name),
            to_connection(dummy1_name, long_conn_name),
            to_connection(long_conn_name, dummy2_name),
            to_connection(dummy2_name, end_dummy_name),
        ])
        
    arch.append(to_end())
    
    return arch