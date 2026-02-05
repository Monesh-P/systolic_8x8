`timescale 1ns/1ps

module tb_systolic_array;

    parameter int N       = 8;
    parameter int DATA_W  = 8;
    parameter int ACC_W   = 16;

    logic clk, rst;
    logic [DATA_W-1:0] A_in [0:N-1];
    logic [DATA_W-1:0] B_in [0:N-1];
    logic [ACC_W-1:0]  C    [0:N-1][0:N-1];

    logic [DATA_W-1:0] A [0:N-1][0:N-1];
    logic [DATA_W-1:0] B [0:N-1][0:N-1];

    // DUT
    systolic_array #(
        .N(N),
        .DATA_W(DATA_W),
        .ACC_W(ACC_W)
    ) dut (
        .clk (clk),
        .rst (rst),
        .A_in(A_in),
        .B_in(B_in),
        .C   (C)
    );

    // Clock generation
    always #5 clk = ~clk;

    int t, i, j;

    initial begin
        clk = 0;
        rst = 1;

        // -----------------------------
        // TEST MATRIX
        // -----------------------------
        // Matrix A: first row = 1s
        A[0] = '{1,1,1,1,1,1,1,1};
        for (i = 1; i < N; i++)
            A[i] = '{default:0};

        // Matrix B: first column = 1s
        for (i = 0; i < N; i++) begin
            B[i] = '{default:0};
            B[i][0] = 1;
        end

        // Clear inputs
        for (i = 0; i < N; i++) begin
            A_in[i] = 0;
            B_in[i] = 0;
        end

        // Release reset
        #20 rst = 0;

        // -----------------------------
        // SYSTOLIC FEED (SKEWED)
        // -----------------------------
        for (t = 0; t < (2*N); t++) begin
            @(posedge clk);

            for (i = 0; i < N; i++)
                A_in[i] = (t-i >= 0 && t-i < N) ? A[i][t-i] : 0;

            for (j = 0; j < N; j++)
                B_in[j] = (t-j >= 0 && t-j < N) ? B[t-j][j] : 0;
        end

        // -----------------------------
        // DRAIN PIPELINE (IMPORTANT)
        // -----------------------------
        repeat (6*N) @(posedge clk);

        // -----------------------------
        // PRINT RESULT
        // -----------------------------
        $display("RESULT_BEGIN");
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++)
                $write("%0d ", C[i][j]);
            $write("\n");
        end
        $display("RESULT_END");

        $finish;
    end

endmodule
