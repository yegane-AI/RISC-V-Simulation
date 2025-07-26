module tb_riscv_pipeline;
    reg clk, rst;

    riscv_pipeline uut (
        .clk(clk),
        .rst(rst)
    );

    initial begin
        clk = 0;
        rst = 1;
        #10 rst = 0;

        repeat (20) begin
            #5 clk = ~clk;
            #5 clk = ~clk;
        end
    end
endmodule
