from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, now, toVHDL


def instruction_dec(instruction, opcode, rs, rt, rd, shamt, func,
                    address, NopSignal=Signal(intbv(0)[1:]) ):
    """
    指令解释器
    @param instruction: 32位指令 
    @param rt = Signal(intbv(0)[5:])       #instruction 20:16
    @param rs = Signal(intbv(0)[5:])       #instruction 25:21
    @param rd = Signal(intbv(0)[5:])       #instruction 15:11
    @param shamt = Signal(intbv(0)[5:])    #instruction 10:6
    @param func = Signal(intbv(0)[6:])     #instruction 5:0
    @param address = Signal(intbv(0)[16:]) #instruction 15:0
    """
    @always_comb
    def decode():
        opcode.next = instruction[32:26]
        rs.next = instruction[26:21]
        rt.next = instruction[21:16]
        rd.next = instruction[16:11]
        shamt.next = instruction[11:6]
        func.next = instruction[6:0]
        address.next = instruction[16:0].signed()


        if instruction == 0:
            NopSignal.next = 1
        else: 
            NopSignal.next = 0

    return decode


def testBench():
    pass
    


def main():
    sim = Simulation(testBench())
    sim.run()



if __name__ == '__main__':
    main()
    
