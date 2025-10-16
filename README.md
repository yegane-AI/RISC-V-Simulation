# RISC-V 7-Stage Pipeline Simulator (PyRTL)
This project is a simple educational RISC-V pipeline simulator built in Python using PyRTL. PyRTL has been developed in ArchLab at UCSB: 
https://github.com/UCSBarchlab/PyRTL

Other HDLs coming up... Will be mostly focused on Verilog...

This project models a 7-stage pipeline based on a subset of the RISC-V instruction set and simulates how instructions move through the pipeline cycle-by-cycle.

**Current Features:** 7-stage pipeline structure:
IF → ID → EX1 → EX2 → MEM1 → MEM2 → WB

**Basic instruction decoding:**
Register file and instruction/data memory modeling
Clock-cycle simulation
Waveform trace for debugging

**Coming Soon:**
ALU operations in EX stages
Memory access support (LOAD/STORE)
Hazard detection and pipeline stalling
Forwarding paths
Performance stats (CPI, stalls, etc.)

**Example:**
The simulator currently loads a couple of hardcoded instructions into instruction memory, like a mock ADD x3, x1, x2, and advances them through the pipeline. More instructions and functionality will be added soon.

**Why PyRTL?**
PyRTL is a Python-based hardware description and simulation framework. It's great for teaching and prototyping hardware without needing a full Verilog toolchain. With it, you can:
1. Define RTL-level hardware in Python
2. Simulate clocked logic
3. Trace waveforms and debug visually

**Contributions**
Pull requests are welcome! Feel free to fork the repo and help build out:

ALU logic
Forwarding and hazard detection
Branch prediction
Testbench support


**Further Task**
Hazard Control! 
