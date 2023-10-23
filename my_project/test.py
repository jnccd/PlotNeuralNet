import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    to_Pool("dummy1", offset="(0.5,-8,0)", to="(conv1-east)", height=0, depth=0, width=0, opacity=0 ),
    to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(conv1-east)", height=32, depth=32, width=2 ),
    to_Conv("conv2_1", 128, 64, offset="(1,-8,0)", to="(conv1-east)", height=32, depth=32, width=2 ),
    to_Sum('sum', offset="(2,0,0)", to="(conv2-east)",),
    to_SoftMax("soft1", 10 ,"(1,0,0)", "(sum-east)", caption="SOFT"  ),
    
    to_connection("conv1", "conv2"),
    to_connection("conv1", "dummy1"),
    to_connection("dummy1", "conv2_1"),
    to_connection("conv2_1", "sum"),
    to_connection("sum", "soft1"),
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()