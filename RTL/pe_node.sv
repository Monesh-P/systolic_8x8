
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

    output logic [ACC_W-1:0]     acc
);
    integer mac_count;   // 🔹 MAC counter

    always_ff @(posedge clk) begin
        if (rst) begin
            acc   <= '0;
            a_out <= '0;
            b_out <= '0;
            mac_count <= 0;   // reset counter
        end 
        else begin
            a_out <= a_in;
            b_out <= b_in;

            if (en) begin
                acc <= acc + (a_in * b_in);
                mac_count <= mac_count + 1;  // ✅ count every MAC
            end
        end
    end

    final begin
        $display("NORMAL PE %m : MAC operations = %0d", mac_count);
    end

endmodule