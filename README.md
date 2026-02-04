# 8x8 Systolic Array Matrix Multiplier

This project implements an 8x8 systolic array for matrix multiplication using SystemVerilog.

## Folder Structure
- rtl/ : RTL modules
- tb/  : Testbench and input matrices

## Simulation
- Simulator: Vivado XSIM / ModelSim / EDA Playground
- Input matrices are read from text files.

## Notes
- Wide matrix ports are kept internal to avoid FPGA I/O overutilization.
