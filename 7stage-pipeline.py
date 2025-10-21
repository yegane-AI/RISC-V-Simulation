import pyrtl
## in pyrtl, though doubts if actual vhdl is better...
# ---------------------------
# 1. Define the Instruction Set
# ---------------------------
OPCODES = {
    'ADD': 0,
    'SUB': 1,
    'AND': 2,
    'OR': 3,
    'LOAD': 4,
    'STORE': 5,
    'NOP': 15
}

# ---------------------------
# 2. Define Pipeline Stage Registers
# ---------------------------
def pipeline_registers(stage_name):
    return {
        'opcode': pyrtl.Register(4, name=f'{stage_name}_opcode'),
        'rs1': pyrtl.Register(5, name=f'{stage_name}_rs1'),
        'rs2': pyrtl.Register(5, name=f'{stage_name}_rs2'),
        'rd': pyrtl.Register(5, name=f'{stage_name}_rd'),
        'imm': pyrtl.Register(16, name=f'{stage_name}_imm'),
        'valid': pyrtl.Register(1, name=f'{stage_name}_valid'),
    }

# Create pipeline registers for each of the 7 stages
IF_ID = pipeline_registers('IF_ID')
ID_EX1 = pipeline_registers('ID_EX1')
EX1_EX2 = pipeline_registers('EX1_EX2')
EX2_MEM1 = pipeline_registers('EX2_MEM1')
MEM1_MEM2 = pipeline_registers('MEM1_MEM2')
MEM2_WB = pipeline_registers('MEM2_WB')

# ---------------------------
# 3. Core Components
# ---------------------------
reg_file = [pyrtl.Register(16, name=f'x{i}') for i in range(32)]

instr_mem = pyrtl.MemBlock(bitwidth=32, addrwidth=8, name='instr_mem')
data_mem = pyrtl.MemBlock(bitwidth=16, addrwidth=8, name='data_mem')

pc = pyrtl.Register(8, name='pc')
next_pc = pc + 1

# ---------------------------
# 4. Instruction Fetch Stage
# ---------------------------
instr = pyrtl.WireVector(32, name='fetched_instr')
instr <<= instr_mem[pc]

# Decode fields (simplified)
opcode = instr[0:4]
rs1 = instr[4:9]
rs2 = instr[9:14]
rd = instr[14:19]
imm = instr[16:32]

# Update pipeline registers
IF_ID['opcode'].next <<= opcode
IF_ID['rs1'].next <<= rs1
IF_ID['rs2'].next <<= rs2
IF_ID['rd'].next <<= rd
IF_ID['imm'].next <<= imm
IF_ID['valid'].next <<= 1

# Advance PC
pc.next <<= next_pc

# ---------------------------
# 5. Hazard Detection / Forwarding (To be added)
# ---------------------------
# For now, we assume no hazards (ideal pipeline)

# ---------------------------
# 6. Stats / Debug Info (Basic Simulation)
# ---------------------------
sim_trace = pyrtl.SimulationTrace() ### Should work a little on simulation. 
sim = pyrtl.Simulation(tracer=sim_trace)

# Initialize some sample instructions
sim.memory[instr_mem] = {
    0: int('00000000010000100001100000000000', 2),  # ADD x3, x1, x2 (example)
    1: int('11110000000000000000000000000000', 2),  # NOP
}

for cycle in range(5):
    sim.step({})

# ---------------------------
# 7. End Simulation: Print Trace
# ---------------------------
sim_trace.render_trace(symbol_len=5, segment_size=5)
