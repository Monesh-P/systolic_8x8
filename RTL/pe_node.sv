module pe_node #(
    parameter int DATA_W = 8,
    parameter int ACC_W  = 16
)(
    input  logic                 clk,
    input  logic                 rst,
    input  logic                 en,

    input  logic [DATA_W-1:0]    a_in,
    input  logic [DATA_W-1:0]    b_in,

    output logic [DATA_W-1:0]    a_out,
    output logic [DATA_W-1:0]    b_out,
    output logic [ACC_W-1:0]     acc,
    output logic                 mac_valid   // 🔹 NEW
);

    always_ff @(posedge clk) begin
        if (rst) begin
            acc       <= '0;
            a_out     <= '0;
            b_out     <= '0;
            mac_valid <= 0;
        end else begin
            a_out <= a_in;
            b_out <= b_in;
            mac_valid <= 0;

            if (en) begin
                acc <= acc + (a_in * b_in);
                mac_valid <= 1;   // MAC happened this cycle
            end
        end
    end
endmodule
