import tkinter as tk
from tkinter import messagebox
import subprocess

N = 8
VIVADO_CMD = [
    r"C:\Xilinx\2025.1\Vivado\bin\vivado.bat",
    "-mode", "batch",
    "-source", "run_sim.tcl"
]

def save_matrices():
    try:
        with open("TB/matrixA.txt", "w") as fa:
            for i in range(N):
                fa.write(" ".join(entryA[i][j].get() for j in range(N)) + "\n")

        with open("TB/matrixB.txt", "w") as fb:
            for i in range(N):
                fb.write(" ".join(entryB[i][j].get() for j in range(N)) + "\n")

    except Exception as e:
        messagebox.showerror("File Error", str(e))


def run_vivado():
    save_matrices()
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Running Vivado simulation...\n\n")

    try:
        proc = subprocess.run(
            VIVADO_CMD,
            capture_output=True,
            text=True,
            shell=True
        )

        stdout = proc.stdout.splitlines()

        result_started = False
        matrix = []
        mac_lines = []

        for line in stdout:
            if "RESULT_BEGIN" in line:
                result_started = True
                continue
            if "RESULT_END" in line:
                result_started = False
                continue 
        
            if result_started:
                matrix.append(line)

            if "MAC operations" in line:
                mac_lines.append(line)

        if matrix:
            output_box.insert(tk.END, "Output Matrix C:\n\n")
            for row in matrix:
                output_box.insert(tk.END, row + "\n")

        if mac_lines:
            output_box.insert(tk.END, "\nMAC OPERATIONS PER PE:\n\n")
            for line in mac_lines:
                output_box.insert(tk.END, line + "\n")

        else:
            output_box.insert(tk.END, "No output matrix found.\n")

    except Exception as e:
        messagebox.showerror("Vivado Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("8×8 Systolic Array – Full Interface")
root.geometry("1250x650")

main_frame = tk.Frame(root)
main_frame.pack(pady=15)

# -------- Matrix A --------
frameA = tk.Frame(main_frame)
frameA.grid(row=0, column=0)

tk.Label(frameA, text="Matrix A", font=("Arial", 14, "bold")).grid(
    row=0, column=0, columnspan=N, pady=10
)

entryA = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameA, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")
        entryA[i][j] = e

# -------- BIG GAP --------
tk.Label(main_frame, text=" " * 25).grid(row=0, column=1)

# -------- Matrix B --------
frameB = tk.Frame(main_frame)
frameB.grid(row=0, column=2)

tk.Label(frameB, text="Matrix B", font=("Arial", 14, "bold")).grid(
    row=0, column=0, columnspan=N, pady=10
)

entryB = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameB, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")
        entryB[i][j] = e

# -------- Buttons --------
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
).pack()

# -------- Output --------
tk.Label(root, text="Output Matrix C", font=("Arial", 14, "bold")).pack()

output_box = tk.Text(root, height=12, width=80, font=("Courier", 10))
output_box.pack(pady=10)

root.mainloop()