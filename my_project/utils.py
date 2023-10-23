import sys
sys.path.append('../')
from pycore.tikzeng import *

class ArchLayer:
    def __init__(self, size = 256, features = 32, caption = '""', type='conv', long_conn_from=-1):
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
                to_Sum(l.name, offset=f"({padding},0,0)", to=f"({layers[i-1].name}-east)" if i > 0 else '(0,0,0)'),
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
        arch.extend([
            to_Conv(long_conn_name, l.size, l.features, offset=f"({padding},-{long_conn_padding},0)", to=f"({layers[l.long_conn_from].name}-east)", height=l.height, depth=l.depth, width=l.width, caption=l.caption ),
            to_connection(layers[l.long_conn_from].name, long_conn_name),
            to_connection(long_conn_name, l.name),
        ])
        
    arch.append(to_end())
    
    return arch