import sys
sys.path.append('../')
from pycore.tikzeng import *
from utils import *

archLayers = [
    ArchLayer(416, 3, caption='Input'),
    ArchLayer(416, 32),
    ArchLayer(104, 128),
    ArchLayer(52, 256),
    ArchLayer(26, 512),
    ArchLayer(13, 1024),
    ArchLayer(13, 1024),
    ArchLayer(13, 1024),
    ArchLayer(13, 1024, type='sum', long_conn_from=4),
    ArchLayer(13, 125),
]

arch = to_arch(archLayers, padding=1, length_exp=0.5)

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()