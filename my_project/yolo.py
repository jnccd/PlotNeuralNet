import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    
    to_Conv("conv1", 448, 3, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=1 ),
    to_Conv("conv2", 112, 192, offset="(1,0,0)", to="(conv1-east)", height=32, depth=32, width=5 ),
    to_Conv("conv3", 56, 256, offset="(1,0,0)", to="(conv2-east)", height=16, depth=16, width=6 ),
    to_Conv("conv4", 28, 512, offset="(1,0,0)", to="(conv3-east)", height=10, depth=10, width=12 ),
    to_Conv("conv5", 14, 1024, offset="(1,0,0)", to="(conv4-east)", height=5, depth=5, width=24 ),
    to_Conv("conv6", 7, 1024, offset="(1,0,0)", to="(conv5-east)", height=3, depth=3, width=24 ),
    to_Conv("conv7", 7, 1024, offset="(1,0,0)", to="(conv6-east)", height=3, depth=3, width=24 ),
    
    to_SoftMax("conn", 4096 ,"(3,0,0)", "(conv7-east)", depth=50,caption=""  ),
    to_Conv("out", 7, 30, offset="(1,0,0)", to="(conn-east)", height=3, depth=3, width=24 ),
    
    to_connection("conv1", "conv2"),
    to_connection("conv2", "conv3"),
    to_connection("conv3", "conv4"),
    to_connection("conv4", "conv5"),
    to_connection("conv5", "conv6"),
    to_connection("conv6", "conv7"),
    to_connection("conv7", "conn"),
    to_connection("conn", "out"),
    
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()