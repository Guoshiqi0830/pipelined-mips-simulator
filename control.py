from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, instances, now, toVHDL



def control(opcode, RegDst, Branch, MemRead, MemtoReg, ALUop, 
            MemWrite, ALUSrc, RegWrite, NopSignal=Signal(intbv(0)[1:]), Stall=Signal(intbv(0)[1:])):
    """
    Control Unit
    @param opcode 6位操作码
    @param RegDst, ALUSrc, MemtoReg  1位信号，控制多路选择器
    @param RegWrite, MemRead, MemWrite 1位信号，控制寄存器和内存的读写
    @param Branch 1位信号，确定是否有分支
    @param ALUop 2位信号，控制ALU
    """

    @always_comb
    def logic():
        if NopSignal == 1 or Stall == 1:
            RegDst.next = 0
            ALUSrc.next = 0
            MemtoReg.next = 0
            RegWrite.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            Branch.next = 0
            ALUop.next = intbv('00')

        else:

            if opcode == 0:     #r-format
                RegDst.next = 1
                ALUSrc.next = 0
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                ALUop.next = intbv('10')
            
            elif opcode == 0x23: #lw
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 1
                RegWrite.next = 1
                MemRead.next = 1
                MemWrite.next = 0
                Branch.next = 0
                ALUop.next = intbv('00')   
     
            elif opcode == 0x2b: #sw
                ALUSrc.next = 1
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 1
                Branch.next = 0
                ALUop.next = intbv('00')   

            elif opcode == 0x04: #beq
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                ALUop.next = intbv('01')   

    return logic


def testBench():

    signal_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch = signal_1bit
    ALUop = Signal(intbv(0)[2:])

    opcode = Signal(intbv(0)[6:])

    # control_inst = toVHDL(control, opcode, RegDst, Branch, MemRead, MemtoReg, ALUop, MemWrite, ALUSrc, RegWrite)

    @instance
    def stimulus():
        for op_value in [0, int('100011', 2), int('101011', 2), int('000100', 2)]:
            opcode.next = op_value
            yield delay(10)

            print ('opcode: ', bin(opcode, 6))
            print (RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, bin(ALUop, 2))
        


    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()

if __name__ == '__main__':
    main()
    
