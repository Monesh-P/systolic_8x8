import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# -------------------------------------------------
# Configuration
# -------------------------------------------------
N = 8

VIVADO_CMD = [
    r"C:\Xilinx\2025.1\Vivado\bin\vivado.bat",
    "-mode", "batch",
    "-source", "run_sim.tcl"
]

MATRIX_A_FILE = "TB/matrixA.txt"
MATRIX_B_FILE = "TB/matrixB.txt"

# -------------------------------------------------
# Save matrices from GUI to files
# -------------------------------------------------
def save_matrices():
    try:
        os.makedirs("TB", exist_ok=True)

        with open(MATRIX_A_FILE, "w") as fa:
            for i in range(N):
                row = []
                for j in range(N):
                    val = entryA[i][j].get().strip()
                    if val == "":
                        val = "0"
                    row.append(val)
                fa.write(" ".join(row) + "\n")

        with open(MATRIX_B_FILE, "w") as fb:
            for i in range(N):
                row = []
                for j in range(N):
                    val = entryB[i][j].get().strip()
                    if val == "":
                        val = "0"
                    row.append(val)
                fb.write(" ".join(row) + "\n")

    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return False

    return True


# -------------------------------------------------
# Run Vivado simulation
# -------------------------------------------------
def run_vivado():
    if not save_matrices():
        return

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Running Vivado simulation...\n\n")
    output_box.update()

    try:
        proc = subprocess.run(
            VIVADO_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout_lines = proc.stdout.splitlines()
        stderr_lines = proc.stderr.splitlines()

        # Show Vivado errors if any
        if stderr_lines:
            output_box.insert(tk.END, "Vivado Errors:\n")
            for line in stderr_lines:
                output_box.insert(tk.END, line + "\n")
            output_box.insert(tk.END, "\n")

        # Parse RESULT section
        result_started = False
        matrix = []

        for line in stdout_lines:
            if "RESULT_BEGIN" in line:
                result_started = True
                continue
            if "RESULT_END" in line:
                break
            if result_started:
                matrix.append(line)

        if matrix:
            output_box.insert(tk.END, "Output Matrix C:\n\n")
            for row in matrix:
                output_box.insert(tk.END, row + "\n")
        else:
            output_box.insert(
                tk.END,
                "No output matrix found.\n"
                "Make sure testbench prints RESULT_BEGIN / RESULT_END.\n"
            )

    except Exception as e:
        messagebox.showerror("Vivado Error", str(e))


# -------------------------------------------------
# Launch MAC visualization GUI
# -------------------------------------------------
def open_mac_gui():
    if not os.path.exists("mac_trace.csv"):
        messagebox.showwarning(
            "MAC Trace Missing",
            "mac_trace.csv not found.\nRun simulation first."
        )
        return

    try:
        subprocess.Popen(["python", "systolic_gui.py"])
    except Exception as e:
        messagebox.showerror("GUI Error", str(e))


# =================================================
# GUI LAYOUT
# =================================================
root = tk.Tk()
root.title("8×8 Systolic Array – Full Interface")
root.geometry("1250x650")

main_frame = tk.Frame(root)
main_frame.pack(pady=15)

# ---------------- Matrix A ----------------
frameA = tk.Frame(main_frame)
frameA.grid(row=0, column=0)

tk.Label(
    frameA,
    text="Matrix A",
    font=("Arial", 14, "bold")
).grid(row=0, column=0, columnspan=N, pady=10)

entryA = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameA, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")
        entryA[i][j] = e

# ---------------- Spacer ----------------
tk.Label(main_frame, text=" " * 25).grid(row=0, column=1)

# ---------------- Matrix B ----------------
frameB = tk.Frame(main_frame)
frameB.grid(row=0, column=2)

tk.Label(
    frameB,
    text="Matrix B",
    font=("Arial", 14, "bold")
).grid(row=0, column=0, columnspan=N, pady=10)

entryB = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameB, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")
        entryB[i][j] = e

# ---------------- Buttons ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(
    btn_frame,
    text="Run Vivado Simulation",
    font=("Arial", 12, "bold"),
    bg="#6fdc6f",
    padx=20,
    pady=8,
    command=run_vivado
).pack(pady=5)

tk.Button(
    btn_frame,
    text="View MAC Activity",
    font=("Arial", 12),
    bg="#6fa8dc",
    padx=20,
    pady=8,
    command=open_mac_gui
).pack(pady=5)

# ---------------- Output ----------------
tk.Label(
    root,
    text="Output Matrix C",
    font=("Arial", 14, "bold")
).pack()

output_box = tk.Text(root, height=12, width=80, font=("Courier", 10))
output_box.pack(pady=10)

root.mainloop()

