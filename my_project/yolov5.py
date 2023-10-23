import sys
sys.path.append('../')
from pycore.tikzeng import *
from utils import *

archLayers = [
    ArchLayer(640, 3, caption='Input'),
    ArchLayer(320, 64, caption='P1'),
    ArchLayer(160, 128, caption='P2'),
    ArchLayer(80, 256, caption='C3'),
    ArchLayer(40, 512, caption='C3'),
    ArchLayer(20, 1024, caption='C3'),
    ArchLayer(20, 1024, caption='SPPF'),
    ArchLayer(40, 512, type='sum', long_conn_from=4),#ArchLayer(40, 1024, caption='CONCAT'),
    ArchLayer(40, 512, caption='C3'),
    ArchLayer(80, 256, type='sum', long_conn_from=3),#ArchLayer(80, 512, caption='CONCAT'),
    ArchLayer(80, 256, caption='C3'),
    ArchLayer(40, 256, type='sum', long_conn_from=8),#ArchLayer(40, 512, caption='CONCAT'),
    ArchLayer(20, 512, caption='C3'),
    ArchLayer(20, 512, type='sum', long_conn_from=6),#ArchLayer(20, 1024, caption='CONCAT'),
    ArchLayer(20, 1024, caption='C3'),
]

arch = to_arch(archLayers, padding=1, length_exp=0.5)

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()