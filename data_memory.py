import random 

from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, instances, now, toVHDL



def data_memory(clk, address, write_data, read_data, memread, memwrite ):
    """
    内存读写单元
    @param clk -- 时钟驱动信号
    @param read_data -- 输出数据
    @param write_data -- 输入数据
    @param address -- 数据地址
    @param memwrite -- 控制是否写入数据
    @param memread -- 控制是否读取数据
    """    

    mem = [Signal(intbv(0, min=-(2**31), max=2**31-1)) for i in range(1024)]

    # 硬编码了一个内存数据用于测试
    mem[7] = Signal(intbv(51, min=-(2**31), max=2**31-1))
    
    @always(clk.negedge)
    def logic():
        if memwrite == 1:
            mem[int(address)].next = write_data.val
    
        elif memread == 1:
            read_data.next = mem[int(address)]

    return logic



def testBench():

    depth = 5

    address = Signal(intbv(0)[32:]) 

    data_in, data_out = [Signal( intbv(0, min=-(2**31),max=2**31-1)) for i in range(2)]

    clk = Signal(intbv(1)[1:])
    write_control = Signal(intbv(0)[1:])
    read_control = Signal(intbv(0)[1:])

    memory_i = data_memory(clk, address, data_in, data_out, read_control, write_control)

    addresses = [random.randint(0, 1024) for i in range(depth)]
    values = [random.randint(-(2**31), 2**31-1) for i in range(depth)]

    @instance
    def stimulus():

        #write
        for addr, val in zip(addresses, values):
            
            address.next = intbv( addr)[32:]
            data_in.next = intbv( val, min=-(2**31), max=2**31-1)
            
            write_control.next = 1
            clk.next = 0

            print ("Write: addr %i = %d" % ( addr, val))
            yield delay(5)
            write_control.next = 0
            clk.next = 1
            yield delay(5)
        
        #read
        for addr in addresses:
            address.next = intbv( addr)[32:]
            read_control.next = 1
            clk.next = 0
            yield delay(5)
            print ("Read: addr %i = %d" % (addr, data_out))
            clk.next = 1
            read_control.next = 0
            yield delay(5)
            
    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()

if __name__ == '__main__':
    main()
