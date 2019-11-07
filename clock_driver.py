from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, instances, now, toVHDL


def clock_driver(clk, period=1):
    '''
    时钟驱动
    '''
    halfPeriod = delay(period)

    @always(halfPeriod)
    def drive_clock():
        clk.next = not clk

    return drive_clock
