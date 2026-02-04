import tkinter as tk
from tkinter import messagebox

N = 8

def save_matrices():
    try:
        with open("TB/matrixA.txt", "w") as fa:
            for i in range(N):
                row = []
                for j in range(N):
                    row.append(entryA[i][j].get())
                fa.write(" ".join(row) + "\n")

        with open("TB/matrixB.txt", "w") as fb:
            for i in range(N):
                row = []
                for j in range(N):
                    row.append(entryB[i][j].get())
                fb.write(" ".join(row) + "\n")

        messagebox.showinfo(
            "Success",
            "Matrices saved successfully!\n\nNow run Vivado simulation."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("8x8 Matrix Input - Systolic Array")
root.geometry("900x500")

tk.Label(root, text="Matrix A", font=("Arial", 12, "bold")).grid(row=0, column=1, columnspan=8)
tk.Label(root, text="Matrix B", font=("Arial", 12, "bold")).grid(row=0, column=10, columnspan=8)

entryA = [[None]*N for _ in range(N)]
entryB = [[None]*N for _ in range(N)]

# Matrix A entries
for i in range(N):
    for j in range(N):
        e = tk.Entry(root, width=4)
        e.grid(row=i+1, column=j+1, padx=2, pady=2)
        e.insert(0, "0")
        entryA[i][j] = e

# Matrix B entries
for i in range(N):
    for j in range(N):
        e = tk.Entry(root, width=4)
        e.grid(row=i+1, column=j+10, padx=2, pady=2)
        e.insert(0, "0")
        entryB[i][j] = e

# Save button
tk.Button(
    root,
    text="Save Matrices",
    font=("Arial", 11),
    bg="lightgreen",
    command=save_matrices
).grid(row=10, column=1, columnspan=18, pady=15)

root.mainloop()
