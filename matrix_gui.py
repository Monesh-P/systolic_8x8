import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import time

# ---------------- CONFIG ----------------
N = 8

VIVADO_CMD = r"C:\Xilinx\2025.1\Vivado\bin\vivado.exe"
TCL_SCRIPT = "run_sim.tcl"
XSIM_LOG = "vivado_systolic_8x8.sim/sim_1/behav/xsim/xsim.log"

# ---------------- GUI ----------------
root = tk.Tk()
root.title("8×8 Systolic Array – Full Interface")

entries_A = []
entries_B = []

# ---------------- MATRIX INPUT UI ----------------
def create_matrix(frame, entries):
    for i in range(N):
        row = []
        for j in range(N):
            e = tk.Entry(frame, width=3, justify="center")
            e.insert(0, "0")
            e.grid(row=i, column=j, padx=3, pady=3)
            row.append(e)
        entries.append(row)

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

frame_A = tk.Frame(frame_top)
frame_A.pack(side="left", padx=40)

frame_B = tk.Frame(frame_top)
frame_B.pack(side="left", padx=40)

tk.Label(frame_A, text="Matrix A", font=("Arial", 12, "bold")).pack()
tk.Label(frame_B, text="Matrix B", font=("Arial", 12, "bold")).pack()

matA_frame = tk.Frame(frame_A)
matA_frame.pack()
create_matrix(matA_frame, entries_A)

matB_frame = tk.Frame(frame_B)
matB_frame.pack()
create_matrix(matB_frame, entries_B)

# ---------------- SAVE MATRICES ----------------
def save_matrices():
    with open("matrixA.txt", "w") as fa:
        for row in entries_A:
            fa.write(" ".join(e.get() for e in row) + "\n")

    with open("matrixB.txt", "w") as fb:
        for row in entries_B:
            fb.write(" ".join(e.get() for e in row) + "\n")

# ---------------- READ OUTPUT ----------------
def read_output_matrix():
    if not os.path.exists(XSIM_LOG):
        return None

    with open(XSIM_LOG, "r") as f:
        lines = f.readlines()

    matrix = []
    capture = False

    for line in lines:
        if "Output Matrix C:" in line:
            capture = True
            continue
        if capture:
            if line.strip() == "" or "MAC_COUNT" in line:
                break
            try:
                row = [int(x) for x in line.strip().split()]
                matrix.append(row)
            except:
                pass

    return matrix

# ---------------- RUN VIVADO ----------------
def run_vivado():
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Running Vivado simulation...\n")

    save_matrices()

    try:
        subprocess.run(
            [VIVADO_CMD, "-mode", "batch", "-source", TCL_SCRIPT],
            check=True
        )
    except subprocess.CalledProcessError:
        output_box.insert(tk.END, "Vivado execution failed.\n")
        return

    time.sleep(1)  # allow log to flush

    matrix = read_output_matrix()

    output_box.delete("1.0", tk.END)

    if not matrix:
        output_box.insert(tk.END, "No output matrix found.\n")
    else:
        output_box.insert(tk.END, "Output Matrix C:\n")
        for row in matrix:
            output_box.insert(tk.END, " ".join(map(str, row)) + "\n")

# ---------------- BUTTON ----------------
tk.Button(
    root,
    text="Run Vivado Simulation",
    bg="lightgreen",
    font=("Arial", 12, "bold"),
    command=run_vivado,
    width=25,
    height=2
).pack(pady=10)

# ---------------- OUTPUT ----------------
tk.Label(root, text="Output Matrix C", font=("Arial", 12, "bold")).pack()

output_box = tk.Text(root, height=10, width=60)
output_box.pack(pady=10)

# ---------------- START GUI ----------------
root.mainloop()
