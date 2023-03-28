module multiplier(input [3:0] A,    // 4-bit input value to be multiplied
                  output [7:0] B);  // 8-bit output value of the multiplication

   wire [3:0] shifted_A; // wire for storing the shifted input value
   wire [3:0] sum; // wire for storing the sum of shifted and original input value
   
   // Shift the input value left by one position and add it to itself (multiply by 2)
   assign shifted_A = {A[2:0], 0}; // Shift left by 1 bit
   assign sum = A + shifted_A; // Add the shifted and original input values
   
   // Shift the sum left by one position and add it to itself (multiply by 4)
   assign shifted_A = {sum[2:0], 0}; // Shift left by 1 bit
   assign sum = sum + shifted_A; // Add the shifted and original sum values
   
   // Assign the final output value to the sum multiplied by 2
   assign B = {sum, sum};

endmodule