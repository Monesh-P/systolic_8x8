module tb_systolic_array;

    localparam int N      = 8;
    localparam int DATA_W = 8;
    localparam int ACC_W  = 24;   // IMPORTANT for 8x8 (avoid overflow)

    logic clk, rst;
    logic [DATA_W-1:0] A_in [0:N-1];
    logic [DATA_W-1:0] B_in [0:N-1];
    logic [ACC_W-1:0]  C    [0:N-1][0:N-1];

    logic [DATA_W-1:0] A [0:N-1][0:N-1];
    logic [DATA_W-1:0] B [0:N-1][0:N-1];

    integer i, j, t;
    integer fa, fb;

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

    // Clock
    always #5 clk = ~clk;

    initial begin
        clk = 0;
        rst = 1;

        // -----------------------------
        // Read Matrix A
        // -----------------------------
        fa = $fopen("C:/Users/wwwmo/Downloads/8X8/tb/matrixA.txt", "r");
        if (fa == 0) begin
            $fatal("ERROR: Cannot open matrixA.txt");
        end
        for (i = 0; i < N; i++)
            for (j = 0; j < N; j++)
                $fscanf(fa, "%d", A[i][j]);
        $fclose(fa);

        // -----------------------------
        // Read Matrix B
        // -----------------------------
        fb = $fopen("C:/Users/wwwmo/Downloads/8X8/tb/matrixB.txt", "r");
        if (fb == 0) begin
            $fatal("ERROR: Cannot open matrixB.txt");
        end
        for (i = 0; i < N; i++)
            for (j = 0; j < N; j++)
                $fscanf(fb, "%d", B[i][j]);
        $fclose(fb);

        // Clear inputs
        for (i = 0; i < N; i++) begin
            A_in[i] = 0;
            B_in[i] = 0;
        end

        #20 rst = 0;

        // -----------------------------
        // Correct systolic skewed feed
        // -----------------------------
        for (t = 0; t < (4*N); t++) begin
            @(posedge clk);

            for (i = 0; i < N; i++)
                A_in[i] = (t-i>=0 && t-i<N) ? A[i][t-i] : 0;

            for (j = 0; j < N; j++)
                B_in[j] = (t-j>=0 && t-j<N) ? B[t-j][j] : 0;
        end

        // Let results settle
        repeat (6*N) @(posedge clk);

        // -----------------------------
        // Print Output
        // -----------------------------
        $display("RESULT_BEGIN");
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++) begin
                $write("%0d ", C[i][j]);
            end
            $write("\n");
        end
        $display("RESULT_END");
        $display("===========================\n");

        $finish;
    end

endmodule