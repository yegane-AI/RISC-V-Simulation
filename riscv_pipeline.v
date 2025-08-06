`timescale 1ns / 1ps

module riscv_pipeline(
    input clk,
    input rst
);

//To do: Sync the multiplier with this risc-v simulator. 
    
// --- Program Counter ---
reg [31:0] pc;
wire [31:0] next_pc;

assign next_pc = pc + 4;

// --- Instruction Memory ---
reg [31:0] instr_mem [0:255];
wire [31:0] instr;

// --- IF Stage ---
assign instr = instr_mem[pc[9:2]];

// --- Pipeline Registers Between Stages ---
reg [31:0] IF_ID_instr;
reg [31:0] ID_EX1_instr;
reg [31:0] EX1_EX2_instr;
reg [31:0] EX2_MEM1_instr;
reg [31:0] MEM1_MEM2_instr;
reg [31:0] MEM2_WB_instr;

// --- Register File ---
reg [31:0] regfile [0:31];
wire [4:0] rs1 = IF_ID_instr[19:15];
wire [4:0] rs2 = IF_ID_instr[24:20];
wire [4:0] rd  = IF_ID_instr[11:7];
wire [31:0] rs1_val = regfile[rs1];
wire [31:0] rs2_val = regfile[rs2];

// --- Basic ALU ---
reg [31:0] alu_result;
wire [6:0] opcode = ID_EX1_instr[6:0];

always @(*) begin
    case (opcode)
        7'b0110011: begin // R-type
            case (ID_EX1_instr[14:12]) // funct3
                3'b000: alu_result = rs1_val + rs2_val; // ADD
                3'b110: alu_result = rs1_val | rs2_val; // OR
                3'b111: alu_result = rs1_val & rs2_val; // AND
                default: alu_result = 0;
            endcase
        end
        default: alu_result = 0;
    endcase
end

// --- PC Update ---
always @(posedge clk or posedge rst) begin
    if (rst) begin
        pc <= 0;
    end else begin
        pc <= next_pc;

        // Pipeline registers shift
        IF_ID_instr     <= instr;
        ID_EX1_instr    <= IF_ID_instr;
        EX1_EX2_instr   <= ID_EX1_instr;
        EX2_MEM1_instr  <= EX1_EX2_instr;
        MEM1_MEM2_instr <= EX2_MEM1_instr;
        MEM2_WB_instr   <= MEM1_MEM2_instr;
    end
end

endmodule
