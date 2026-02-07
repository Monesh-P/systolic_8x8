`timescale 1ns/1ps

module tb_systolic_array;

    // ------------------------------------------------------------
    // Parameters
    // ------------------------------------------------------------
    localparam int N      = 8;
    localparam int DATA_W = 8;
    localparam int ACC_W  = 16;

    // ------------------------------------------------------------
    // Clock & Reset
    // ------------------------------------------------------------
    logic clk;
    logic rst;

    // ------------------------------------------------------------
    // Inputs / Outputs
    // ------------------------------------------------------------
    logic [DATA_W-1:0] A_in [0:N-1];
    logic [DATA_W-1:0] B_in [0:N-1];
    logic [ACC_W-1:0]  C    [0:N-1][0:N-1];

    // ------------------------------------------------------------
    // DUT
    // ------------------------------------------------------------
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

    // ------------------------------------------------------------
    // Clock generation (10ns period)
    // ------------------------------------------------------------
    always #5 clk = ~clk;

    // ------------------------------------------------------------
    // File handle for MAC trace
    // ------------------------------------------------------------
    integer fd;

    // ------------------------------------------------------------
    // Test sequence
    // ------------------------------------------------------------
    initial begin
        clk = 0;
        rst = 1;

        // Initialize inputs
        for (int i = 0; i < N; i++) begin
            A_in[i] = 0;
            B_in[i] = 0;
        end

        // Open CSV file for MAC trace
        fd = $fopen("./mac_trace.csv", "w");
        $fwrite(fd, "time,row,col,a,b,mac,acc\n");

        // Hold reset
        #20;
        rst = 0;

        // --------------------------------------------------------
        // Feed matrix A (left) and B (top)
        // --------------------------------------------------------
        for (int k = 0; k < N; k++) begin
            A_in[k] = k + 1;        // 1 2 3 4 5 6 7 8
            B_in[k] = (k + 1) * 2;  // 2 4 6 8 10 12 14 16
        end

        // --------------------------------------------------------
        // Let systolic array complete computation
        // --------------------------------------------------------
        #(20*N);

        // --------------------------------------------------------
        // PRINT RESULT MATRIX (FOR PYTHON GUI)
        // --------------------------------------------------------
        $display("RESULT_BEGIN");
        for (int i = 0; i < N; i++) begin
            $display("%0d %0d %0d %0d %0d %0d %0d %0d",
                C[i][0], C[i][1], C[i][2], C[i][3],
                C[i][4], C[i][5], C[i][6], C[i][7]
            );
        end
        $display("RESULT_END");

        // --------------------------------------------------------
        // Finish simulation
        // --------------------------------------------------------
        #100;
        $finish;
    end

    // ------------------------------------------------------------
    // MAC logging (cycle-accurate)
    // ------------------------------------------------------------
    always @(posedge clk) begin
        for (int i = 0; i < N; i++) begin
            for (int j = 0; j < N; j++) begin
                if (dut.mac_valid[i][j]) begin
                    $fwrite(fd,
                        "%0t,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        $time,
                        i, j,
                        dut.a_dbg[i][j],
                        dut.b_dbg[i][j],
                        dut.mac_dbg[i][j],
                        dut.acc_dbg[i][j]
                    );
                end
            end
        end
    end

    // ------------------------------------------------------------
    // Close file cleanly
    // ------------------------------------------------------------
    final begin
        $fclose(fd);
    end

endmodule
