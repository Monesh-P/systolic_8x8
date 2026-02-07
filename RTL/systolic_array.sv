module systolic_array #(
    parameter int N       = 8,
    parameter int DATA_W  = 8,
    parameter int ACC_W   = 16
)(
    input  logic clk,
    input  logic rst,

    input  logic [DATA_W-1:0] A_in [0:N-1],   // left edge inputs
    input  logic [DATA_W-1:0] B_in [0:N-1],   // top edge inputs

    output logic [ACC_W-1:0]  C    [0:N-1][0:N-1]
);

    // ------------------------------------------------------------
    // Inter-PE pipelines
    // ------------------------------------------------------------
    logic [DATA_W-1:0] a_pipe [0:N-1][0:N];
    logic [DATA_W-1:0] b_pipe [0:N][0:N-1];

    // ------------------------------------------------------------
    // Debug signals (for GUI / testbench logging)
    // ------------------------------------------------------------
    logic                 mac_valid [0:N-1][0:N-1];
    logic [DATA_W-1:0]    a_dbg     [0:N-1][0:N-1];
    logic [DATA_W-1:0]    b_dbg     [0:N-1][0:N-1];
    logic [2*DATA_W-1:0]  mac_dbg   [0:N-1][0:N-1];
    logic [31:0]          acc_dbg   [0:N-1][0:N-1];

    // ------------------------------------------------------------
    // Inject inputs into systolic array
    // ------------------------------------------------------------
    genvar i, j;
    generate
        for (i = 0; i < N; i++) begin
            assign a_pipe[i][0] = A_in[i];
        end

        for (j = 0; j < N; j++) begin
            assign b_pipe[0][j] = B_in[j];
        end
    endgenerate

    // ------------------------------------------------------------
    // Cycle counter
    // ------------------------------------------------------------
    logic [$clog2(3*N):0] cycle;

    always_ff @(posedge clk or posedge rst) begin
        if (rst)
            cycle <= '0;
        else
            cycle <= cycle + 1;
    end

    // ------------------------------------------------------------
    // PE enable window (classic systolic timing)
    // ------------------------------------------------------------
    logic pe_en [0:N-1][0:N-1];

    generate
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++) begin
                assign pe_en[i][j] =
                    (cycle >= (i + j)) &&
                    (cycle <  (i + j + N + 1));
            end
        end
    endgenerate

    // ------------------------------------------------------------
    // PE array instantiation
    // ------------------------------------------------------------
    generate
        for (i = 0; i < N; i++) begin : ROW
            for (j = 0; j < N; j++) begin : COL
                pe_node #(
                    .DATA_W(DATA_W),
                    .ACC_W (ACC_W)
                ) pe (
                    .clk   (clk),
                    .rst   (rst),
                    .en    (pe_en[i][j]),

                    .a_in  (a_pipe[i][j]),
                    .b_in  (b_pipe[i][j]),

                    .a_out (a_pipe[i][j+1]),
                    .b_out (b_pipe[i+1][j]),

                    .acc   (C[i][j]),

                    // -------- Debug / GUI ports --------
                    .mac_valid (mac_valid[i][j]),
                    .a_dbg     (a_dbg[i][j]),
                    .b_dbg     (b_dbg[i][j]),
                    .mac_dbg   (mac_dbg[i][j]),
                    .acc_dbg   (acc_dbg[i][j])
                );
            end
        end
    endgenerate

endmodule
