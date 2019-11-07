from myhdl import Signal, delay, always_comb, now, Simulation, \
                  intbv, bin, instance, instances, toVHDL, toVerilog


def load_program(ROM, program=None, comment_char='#' ):
    '''
    从文件中读取指令
    '''
    if program is None:
        try:
            import sys
            program = sys.argv[1]
            import pdb;pdb.set_trace()
        except IndexError:
            #default
            program= './programs/programs.txt'

    index = 0
    for line in open(program):
        line = line.partition(comment_char)[0]
        line = line.replace(' ', '')
        if len(line) == 32:
            ROM[index] = int(line, 2)
            index += 1

    return tuple(ROM)

ROM = load_program([0] * 32)

def instruction_memory(address, instruction):
    """
    指令存储单元
    @param address: PC指定的地址
    @param instruction: 32位指令
    """

    @always_comb
    def logic():
            instruction.next = ROM[int(address)]
    return logic




def testBench():

    I = Signal(intbv(0, min=0, max=16))
    O = Signal(intbv(0)[32:])


    #pd_instance = prime_detector(E, S)
    #im_instance = toVHDL(instruction_memory, I, O)

    @instance
    def stimulus():
        for i in range(8):
            I.next = intbv(i)
            yield delay(10)
            print ("address: " + bin(I, 4) + " (" + str(I) + ") | instruction: " + bin(O, 32))

    return instances()



def main():
    sim = Simulation(testBench())
    sim.run()


if __name__ == '__main__':
    main()
