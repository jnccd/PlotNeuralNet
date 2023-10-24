import sys
sys.path.append('../')
from pycore.tikzeng import *
from utils import *

archLayers = [
    ArchLayer(448, 3, caption='Input'),
    ArchLayer(112, 192),
    ArchLayer(56, 256),
    ArchLayer(28, 512),
    ArchLayer(14, 1024),
    ArchLayer(7, 1024),
    ArchLayer(7, 1024),
    ArchLayer(1, 4096, type='softmax'),
    ArchLayer(7, 30),
]

arch = to_arch(archLayers, padding=1.5, length_exp=0.5)

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()