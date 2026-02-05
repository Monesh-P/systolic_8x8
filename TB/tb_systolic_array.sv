`timescale 1ns/1ps

module tb_systolic_array;

    // ---------------- PARAMETERS ----------------
    parameter int N = 8;
    parameter int DATA_W = 8;
    parameter int ACC_W  = 16;

    // ---------------- SIGNALS ----------------
    logic clk, rst;
    logic [DATA_W-1:0] A_in [0:N-1];
    logic [DATA_W-1:0] B_in [0:N-1];
    logic [ACC_W-1:0]  C    [0:N-1][0:N-1];

    logic [DATA_W-1:0] A [0:N-1][0:N-1];
    logic [DATA_W-1:0] B [0:N-1][0:N-1];

    integer i, j, t;
    integer mac_count_tb;

    // ---------------- DUT ----------------
    systolic_array #(
        .N(N),
        .DATA_W(DATA_W),
        .ACC_W(ACC_W)
    ) dut (
        .clk(clk),
        .rst(rst),
        .A_in(A_in),
        .B_in(B_in),
        .C(C)
    );

    // ---------------- CLOCK ----------------
    always #5 clk = ~clk;

    // ---------------- MAC COUNT (TB ONLY) ----------------
    always @(posedge clk) begin
        if (!rst)
            mac_count_tb <= mac_count_tb + 1;
    end

    // ---------------- TEST SEQUENCE ----------------
    initial begin
        clk = 0;
        rst = 1;
        mac_count_tb = 0;

        // -------- MATRIX A --------
        A[0] = '{1,1,1,1,1,1,1,1};
        A[1] = '{0,0,0,0,0,0,0,0};
        A[2] = '{0,0,0,0,0,0,0,0};
        A[3] = '{0,0,0,0,0,0,0,0};
        A[4] = '{0,0,0,0,0,0,0,0};
        A[5] = '{0,0,0,0,0,0,0,0};
        A[6] = '{0,0,0,0,0,0,0,0};
        A[7] = '{0,0,0,0,0,0,0,0};

        // -------- MATRIX B --------
        B[0] = '{1,0,0,0,0,0,0,0};
        B[1] = '{1,0,0,0,0,0,0,0};
        B[2] = '{1,0,0,0,0,0,0,0};
        B[3] = '{1,0,0,0,0,0,0,0};
        B[4] = '{1,0,0,0,0,0,0,0};
        B[5] = '{1,0,0,0,0,0,0,0};
        B[6] = '{1,0,0,0,0,0,0,0};
        B[7] = '{1,0,0,0,0,0,0,0};

        // Clear inputs
        for (i = 0; i < N; i++) begin
            A_in[i] = 0;
            B_in[i] = 0;
        end

        #20 rst = 0;

        // -------- SYSTOLIC FEED --------
        for (t = 0; t < (2*N + N); t++) begin
            @(posedge clk);
            for (i = 0; i < N; i++)
                A_in[i] = (t-i >= 0 && t-i < N) ? A[i][t-i] : 0;
            for (j = 0; j < N; j++)
                B_in[j] = (t-j >= 0 && t-j < N) ? B[t-j][j] : 0;
        end

        repeat (20) @(posedge clk);

        // ---------------- OUTPUT (GUI SAFE) ----------------
        $display("Output Matrix C:");
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++)
                $write("%0d ", C[i][j]);
            $write("\n");
        end

        // Extra info (does NOT break GUI)
        $display("MAC_COUNT = %0d", mac_count_tb);

        $finish;
    end

endmodule
