`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/12/2026 11:28:17 PM
// Design Name: 
// Module Name: tb_lockin
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


`ifndef ADC_HEX
  `define ADC_HEX "data/adc_samples.hex"
`endif
`ifndef NUM_SAMPLES
  `define NUM_SAMPLES 20000
`endif

module tb_lockin;
    reg clk;
    reg rst;
    reg signed [15:0] sample_in;
    reg sample_valid;
    wire sample_ready;
    wire signed [39:0] output_data;
    wire output_valid;
    reg signed [15:0] adc_mem [0:`NUM_SAMPLES-1];

    integer i;
    integer result_count;
    integer fd;
    
    lockin_top DUT (
    .clk(clk),
    .rst(rst),
    .sample_in(sample_in),
    .sample_valid(sample_valid),
    .sample_ready(sample_ready),
    .output_data(output_data),
    .output_valid(output_valid)
    );
    
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    initial begin
        rst = 1;
        sample_valid = 0;
        sample_in = 0;
        result_count = 0;
        
        $readmemh(
            `ADC_HEX,
            adc_mem
        );

        repeat(2) @(posedge clk);
        @(negedge clk);
        rst = 0;
        
        fd = $fopen("rtl_results.csv", "w");
        $fdisplay(fd, "window_index,accumulator");

        for(i = 0; i < `NUM_SAMPLES; i = i + 1) begin
           @(negedge clk);
           sample_in = adc_mem[i];
           sample_valid = 1'b1;
           @(posedge clk);
           #1;
           if(output_valid) begin
              result_count = result_count + 1;
              $fdisplay(fd, "%0d,%0d",
              result_count, output_data);
           end
        end
        
        @(negedge clk);
        sample_valid = 0;
        $fclose(fd);
        $display("Total windows processed = %0d", result_count);
        if(result_count == `NUM_SAMPLES / 200)
           $display("TEST PASSED");
        else
           $display("TEST FAILED");
        $finish;
    end 
endmodule
