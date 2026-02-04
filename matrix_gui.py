import tkinter as tk
from tkinter import messagebox

N = 8

def save_matrices():
    try:
        with open("TB/matrixA.txt", "w") as fa:
            for i in range(N):
                fa.write(" ".join(entryA[i][j].get() for j in range(N)) + "\n")

        with open("TB/matrixB.txt", "w") as fb:
            for i in range(N):
                fb.write(" ".join(entryB[i][j].get() for j in range(N)) + "\n")

        messagebox.showinfo(
            "Success",
            "Matrices saved successfully!\nNow run Vivado simulation."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("8×8 Matrix Input – Systolic Array")
root.geometry("1200x520")

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# -------- Matrix A --------
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


# -------- BIG SPACE BETWEEN MATRICES --------
tk.Label(
    main_frame,
    text=" " * 25   # THIS CONTROLS GAP SIZE
).grid(row=0, column=1)


# -------- Matrix B --------
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


# -------- Save Button --------
tk.Button(
    root,
    text="Save Matrices",
    font=("Arial", 12, "bold"),
    bg="#6fdc6f",
    padx=25,
    pady=8,
    command=save_matrices
).pack(pady=25)

root.mainloop()
