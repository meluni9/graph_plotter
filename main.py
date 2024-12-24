from sympy import sympify, lambdify, symbols
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")

        # Entry for mathematical expression
        tk.Label(root, text="Enter mathematical expression e.g., 1/(1+x) :").grid(row=0, column=0, padx=10, pady=5)
        self.expr_entry = tk.Entry(root, width=50)
        self.expr_entry.grid(row=0, column=1, padx=10, pady=5)

        # Entry for range
        tk.Label(root, text="Enter x range (e.g., -10,10):").grid(row=1, column=0, padx=10, pady=5)
        self.range_entry = tk.Entry(root, width=20)
        self.range_entry.grid(row=1, column=1, padx=10, pady=5)

        # Dropdown for color selection
        tk.Label(root, text="Select line color:").grid(row=2, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="blue")
        self.color_dropdown = ttk.Combobox(root, textvariable=self.color_var,
                                           values=["blue", "red", "green", "orange", "purple"])
        self.color_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Plot button
        self.plot_button = tk.Button(root, text="Plot Graph", command=self.plot_graph)
        self.plot_button.grid(row=3, column=0, columnspan=2, pady=10)

    def parse_expression(self, expr, x_min, x_max):
        try:
            x = symbols('x')
            sym_expr = sympify(expr)
            f = lambdify(x, sym_expr, 'numpy')

            # Generate x values
            x_values = np.linspace(x_min, x_max, 10000)
            y_values = f(x_values)

            # Mask to detect valid values (finite and within reasonable range)
            mask = np.isfinite(y_values)

            segments = []
            current_x = []
            current_y = []

            threshold = 50

            for i in range(1, len(x_values)):
                if mask[i] and mask[i - 1]:
                    if abs(y_values[i] - y_values[i - 1]) < threshold:
                        current_x.append(x_values[i])
                        current_y.append(y_values[i])
                    else:
                        if current_x:
                            segments.append((np.array(current_x), np.array(current_y)))
                        current_x = [x_values[i]]
                        current_y = [y_values[i]]
                else:
                    if current_x:
                        segments.append((np.array(current_x), np.array(current_y)))
                    current_x = []
                    current_y = []

            if current_x:
                segments.append((np.array(current_x), np.array(current_y)))

            return segments

        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")
            return []

    def plot_graph(self):
        expr = self.expr_entry.get()
        x_range = self.range_entry.get()
        color = self.color_var.get()

        try:
            x_min, x_max = map(float, x_range.split(','))
        except ValueError:
            messagebox.showerror("Error", "Invalid x range format. Use format: -10,10")
            return

        # Parse and generate segments
        segments = self.parse_expression(expr, x_min, x_max)
        if not segments:
            return

        plt.figure(figsize=(8, 6))

        first_segment = True
        for x_seg, y_seg in segments:
            if first_segment:
                plt.plot(x_seg, y_seg, color=color, linewidth=2, label=expr)
                first_segment = False
            else:
                plt.plot(x_seg, y_seg, color=color, linewidth=2)

        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        ax.set_aspect('equal', adjustable='datalim')

        limit = max(abs(x_min), abs(x_max))
        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)

        # plt.title(f"Graph of {expr}\n", fontsize=14)
        plt.xlabel("x", fontsize=12)
        plt.ylabel("y", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc='upper right')
        plt.show()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = GraphApp(tk_root)
    tk_root.mainloop()
