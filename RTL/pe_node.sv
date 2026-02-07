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

    output logic [ACC_W-1:0]     acc,   // ← comma FIXED

    // 🔍 Debug / GUI signals
    output logic                 mac_valid,
    output logic [DATA_W-1:0]    a_dbg,
    output logic [DATA_W-1:0]    b_dbg,
    output logic [2*DATA_W-1:0]  mac_dbg,
    output logic [31:0]          acc_dbg
);

    logic [2*DATA_W-1:0] mac_temp;

    always_ff @(posedge clk) begin
        if (rst) begin
            acc       <= '0;
            a_out     <= '0;
            b_out     <= '0;
            mac_valid <= 1'b0;
            acc_dbg   <= '0;
        end else begin
            // default
            mac_valid <= 1'b0;

            // pass data forward (systolic behavior)
            a_out <= a_in;
            b_out <= b_in;

            if (en) begin
                mac_temp <= a_in * b_in;
                acc      <= acc + (a_in * b_in);

                // 🔍 debug capture
                mac_valid <= 1'b1;
                a_dbg   <= a_in;
                b_dbg   <= b_in;
                mac_dbg <= a_in * b_in;
                acc_dbg <= acc + (a_in * b_in);
            end
        end
    end

endmodule
