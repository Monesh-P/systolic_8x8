import tkinter as tk
from tkinter import messagebox
import subprocess

# ---------------- CONFIG ----------------
N = 8
VIVADO_CMD = [
    r"C:\Xilinx\2025.1\Vivado\bin\vivado.bat",
    "-mode", "batch",
    "-source", "run_sim.tcl"
]

# ---------------- NAVIGATION HELPERS ----------------
def move_focus(entries, r, c, dr, dc):
    nr, nc = r + dr, c + dc
    if 0 <= nr < N and 0 <= nc < N:
        entries[nr][nc].focus()
    return "break"

def select_all(event):
    event.widget.select_range(0, tk.END)
    return None

# ---------------- FILE SAVE ----------------
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

# ---------------- RUN VIVADO ----------------
def run_vivado():
    save_matrices()

    output_box.delete("1.0", tk.END)
    status_label.config(text="Status: Running simulation", fg="blue")
    root.update_idletasks()

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
            output_box.insert(tk.END, "MATRIX MULTIPLICATION RESULT\n", "title")
            for row in matrix:
                output_box.insert(tk.END, row + "\n")

        if mac_lines:
            output_box.insert(tk.END, "\nMAC OPERATIONS PER PE\n", "title")
            total_mac = 0
            for line in mac_lines:
                cnt = int(line.split("=")[-1])
                total_mac += cnt
                output_box.insert(tk.END, line + "\n", "mac")
            output_box.insert(
                tk.END,
                f"\nTOTAL MAC OPERATIONS: {total_mac}\n",
                "summary"
            )

        status_label.config(text="Status: Simulation complete ✓", fg="green")

    except Exception as e:
        messagebox.showerror("Vivado Error", str(e))
        status_label.config(text="Status: Error during simulation ✗", fg="red")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("INT8 Sparse Systolic Array – Compute & MAC Analysis")
root.geometry("1250x700")

tk.Label(root, text="INPUT MATRICES", font=("Arial", 16, "bold")).pack(pady=5)

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

# -------- MATRIX A --------
frameA = tk.Frame(main_frame)
frameA.grid(row=0, column=0)

tk.Label(frameA, text="Matrix A", font=("Arial", 14, "bold")).grid(
    row=0, column=0, columnspan=N, pady=8
)

entryA = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameA, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")

        e.bind("<FocusIn>", select_all)
        e.bind("<Right>",  lambda ev, r=i, c=j: move_focus(entryA, r, c, 0, 1))
        e.bind("<Left>",   lambda ev, r=i, c=j: move_focus(entryA, r, c, 0,-1))
        e.bind("<Down>",   lambda ev, r=i, c=j: move_focus(entryA, r, c, 1, 0))
        e.bind("<Up>",     lambda ev, r=i, c=j: move_focus(entryA, r, c,-1, 0))
        e.bind("<Return>", lambda ev, r=i, c=j: move_focus(entryA, r, c, 0, 1))

        entryA[i][j] = e

# -------- GAP --------
tk.Label(main_frame, text=" " * 25).grid(row=0, column=1)

# -------- MATRIX B --------
frameB = tk.Frame(main_frame)
frameB.grid(row=0, column=2)

tk.Label(frameB, text="Matrix B", font=("Arial", 14, "bold")).grid(
    row=0, column=0, columnspan=N, pady=8
)

entryB = [[None]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        e = tk.Entry(frameB, width=4, justify="center")
        e.grid(row=i+1, column=j, padx=3, pady=3)
        e.insert(0, "0")

        e.bind("<FocusIn>", select_all)
        e.bind("<Right>",  lambda ev, r=i, c=j: move_focus(entryB, r, c, 0, 1))
        e.bind("<Left>",   lambda ev, r=i, c=j: move_focus(entryB, r, c, 0,-1))
        e.bind("<Down>",   lambda ev, r=i, c=j: move_focus(entryB, r, c, 1, 0))
        e.bind("<Up>",     lambda ev, r=i, c=j: move_focus(entryB, r, c,-1, 0))
        e.bind("<Return>", lambda ev, r=i, c=j: move_focus(entryB, r, c, 0, 1))

        entryB[i][j] = e

# -------- BUTTON --------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(
    btn_frame,
    text="Run Vivado Simulation",
    font=("Arial", 12, "bold"),
    bg="#6fdc6f",
    padx=25,
    pady=8,
    command=run_vivado
).pack()

# -------- STATUS --------
status_label = tk.Label(root, text="Status: Ready", font=("Arial", 10))
status_label.pack(pady=5)

# -------- OUTPUT --------
tk.Label(root, text="OUTPUT & COMPUTE ANALYSIS", font=("Arial", 16, "bold")).pack(pady=5)

output_box = tk.Text(root, height=16, width=95, font=("Courier New", 11))
output_box.pack(pady=10)

output_box.tag_config("title", foreground="blue", font=("Arial", 11, "bold"))
output_box.tag_config("mac", foreground="darkgreen")
output_box.tag_config("summary", foreground="purple", font=("Arial", 11, "bold"))

root.mainloop()
