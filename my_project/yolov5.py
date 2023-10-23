import sys
sys.path.append('../')
from pycore.tikzeng import *
from utils import *

archLayers = [
    ArchLayer(640, 3),
    ArchLayer(320, 64),
    ArchLayer(160, 128),
]

arch = to_arch(archLayers, 3)

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()