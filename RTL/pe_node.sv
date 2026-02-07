module pe_node #(
    parameter DATA_W = 8,
    parameter ACC_W  = 16
)(
    input  logic                  clk,
    input  logic                  rst,
    input  logic                  en,
    input  logic [DATA_W-1:0]      a_in,
    input  logic [DATA_W-1:0]      b_in,
    output logic [DATA_W-1:0]      a_out,
    output logic [DATA_W-1:0]      b_out,
    output logic [ACC_W-1:0]       acc
);

    integer mac_count;

    // Pass-through
    always_ff @(posedge clk) begin
        if (rst) begin
            a_out <= '0;
            b_out <= '0;
        end
        else if (en) begin
            a_out <= a_in;
            b_out <= b_in;
        end
    end

    // ---- SPARSITY LOGIC ----
    wire valid_mul;
    assign valid_mul = (a_in != 0) && (b_in != 0);

    always_ff @(posedge clk) begin
        if (rst) begin
            acc       <= '0;
            mac_count <= 0;
        end
        else if (en) begin
            if (valid_mul) begin
                acc       <= acc + (a_in * b_in);
                mac_count <= mac_count + 1;
            end
        end
    end

    final begin
        $display("PE %m : MAC operations = %0d", mac_count);
    end

endmodule