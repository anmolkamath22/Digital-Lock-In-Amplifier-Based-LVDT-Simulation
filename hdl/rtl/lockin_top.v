`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/12/2026 10:46:20 PM
// Design Name: 
// Module Name: lockin_top
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


module lockin_top(
    input clk,
    input rst,
    input signed [15:0] sample_in,
    input sample_valid,
    output sample_ready,
    output reg signed[39:0] output_data,
    output reg output_valid
    );
    
    reg [4:0] lut_index;  
    reg [7:0] sample_count;

    reg signed [15:0] reference_lut [0:19];
    wire signed [15:0] reference_sample;
    
    wire signed [31:0] product;
    reg signed [39:0] accumulator;
    
    assign reference_sample = reference_lut[lut_index];
    assign product = sample_in * reference_sample;
    
    always @(posedge clk) begin
        if(rst) begin
          lut_index    <= 0;
          sample_count <= 0;
          accumulator  <= 0;
          output_data  <= 0;
          output_valid <= 0;
        end 
        
        else begin
        
          output_valid <= 1'b0;
          
          if(sample_valid && sample_ready) begin
             if(lut_index == 19)
               lut_index <= 0;
               
              else
               lut_index <= lut_index + 1;
               
              if(sample_count == 199) begin
                output_data <= accumulator + product;
                accumulator  <= 0;
                sample_count <= 0;
                output_valid <= 1;
              end
              
              else begin
                accumulator  <= accumulator + product;
                sample_count <= sample_count + 1;
              end
           end
        end   
    end

    assign sample_ready = 1'b1;
    
    initial begin
   $readmemh("data/reference_lut.hex", reference_lut);
end
    
endmodule
