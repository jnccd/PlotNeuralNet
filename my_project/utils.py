import sys
sys.path.append('../')
from pycore.tikzeng import *

class ArchLayer:
    def __init__(self, size, features, caption = '""', type='conv'):
        self.size = size
        self.features = features
        self.caption = caption
        self.type = type
        self.update()
        
    def update(self, width_exp=0.7, length_exp=0.7, name='l1'):
        self.height = self.size**width_exp
        self.depth = self.size**width_exp
        self.width = self.features**length_exp
        self.name = name
        
    def __str__(self):
        return f'ArchLayer({self.size},{self.features},{self.caption})'

def to_arch(layers: list[ArchLayer], padding = 1, width_exp=0.7, length_exp=0.7):
    arch = [
        to_head( '..' ),
        to_cor(),
        to_begin(),
    ]
    
    for i, l in enumerate(layers):
        l.update(name=f'conv{i+1}', width_exp=width_exp, length_exp=length_exp)
        arch.append(
            to_Conv(l.name, l.size, l.features, offset=f"({0 if i == 0 else padding},0,0)", to=f"({layers[i-1].name}-east)" if i > 0 else '(0,0,0)', height=l.height, depth=l.depth, width=l.width, caption=l.caption )
        )
        #print(l.name, l.size, l.features, f"({0 if i == 0 else 1},0,0)", f"({layers[i-1].name if i > 0 else '(0,0,0)'}-east)", l.height, l.depth, l.width)
        
    for i in range(len(layers) - 1):
        arch.append(
            to_connection(layers[i].name, layers[i + 1].name),
        )
        #print(layers[i].name, layers[i + 1].name)
        
    arch.append(to_end())
    
    return arch