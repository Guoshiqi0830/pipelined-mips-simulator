# pipelined-mips-simulator

原代码参考 https://github.com/mgaitan/pymips

基于此代码增加了中文注释

## 环境需求
- python myhdl

## 总体架构
五级流水线: IF ID EXE MEM WB
- IF中包括 PC、InstructionMemory
- ID中包括 ControlUnit、RegisterFile、HazerdDetectionUnit
- EXE中包括 ALU、ForwardingUnit
- MEM中包括 DataMemory

其他一些模块包括
- ALUControl
- ClockDriver
- DataMemory
- InstrucntionDecoder
- IF/ID
- ID/EX
- EX/MEM
- MEM/WB
- SignExtender

顶层模块为dlx

指令从programs文件夹的programs.txt中读取

## 运行
直接运行 dlx.py即可

参数dlx.py 中定义了一些常量
- SIM_TIME 模拟的时间长度
- DEBUG 是否打印调试信息

## 程序
programs 文件中写入了3个程序，分别测试了：
1. 数据冒险
2. 阻塞
3. 控制冒险
