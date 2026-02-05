module systolic_array #(
    parameter int N       = 8,
    parameter int DATA_W  = 8,
    parameter int ACC_W   = 16
)(
    input  logic clk,
    input  logic rst,

    input  logic [DATA_W-1:0] A_in [0:N-1],
    input  logic [DATA_W-1:0] B_in [0:N-1],

    output logic [ACC_W-1:0]  C    [0:N-1][0:N-1]
);

    // Inter-PE pipelines
    logic [DATA_W-1:0] a_pipe [0:N-1][0:N];
    logic [DATA_W-1:0] b_pipe [0:N][0:N-1];

    // Inject inputs
    genvar i, j;
    generate
        for (i = 0; i < N; i++)
            assign a_pipe[i][0] = A_in[i];

        for (j = 0; j < N; j++)
            assign b_pipe[0][j] = B_in[j];
    endgenerate

    // Cycle counter
    logic [$clog2(4*N):0] cycle;
    always_ff @(posedge clk or posedge rst) begin
        if (rst)
            cycle <= 0;
        else
            cycle <= cycle + 1;
    end

    // PE enable window
    logic pe_en [0:N-1][0:N-1];
    generate
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++) begin
                assign pe_en[i][j] =
                    (cycle >= (i + j)) &&
                    (cycle <  (i + j + N));
            end
        end
    endgenerate

    // PE array
    generate
        for (i = 0; i < N; i++) begin
            for (j = 0; j < N; j++) begin
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
                    .acc   (C[i][j])
                );
            end
        end
    endgenerate

endmodule
