import sympy as sp
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
        tk.Label(root, text="Enter mathematical expression (e.g., x**2 + 3*x - 5):").grid(row=0, column=0, padx=10,
                                                                                          pady=5)
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
            x = symbols('x')  # Символічна змінна для виразів
            sym_expr = sympify(expr)  # Перетворення виразу на символьний об’єкт
            f = lambdify(x, sym_expr, 'numpy')  # Перетворення в функцію

            x_values = np.linspace(x_min, x_max, 1000)
            y_values = f(x_values)

            return x_values, y_values
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse expression: {e}")
            return None, None

    def plot_graph(self):
        # Get user inputs
        expr = self.expr_entry.get()
        x_range = self.range_entry.get()
        color = self.color_var.get()

        # Validate and process inputs
        try:
            x_min, x_max = map(float, x_range.split(','))
        except ValueError:
            messagebox.showerror("Error", "Invalid x range format. Use format: -10,10")
            return

        x_values, y_values = self.parse_expression(expr, x_min, x_max)
        if x_values is None or y_values is None:
            return

        # Calculate limits for equal scaling
        y_min, y_max = np.min(y_values), np.max(y_values)
        y_range = max(abs(y_min), abs(y_max))
        x_range = max(abs(x_min), abs(x_max))
        limit = max(x_range, y_range)

        # Plot graph
        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, color=color, label=expr)
        plt.axhline(0, color='black', linewidth=0.8)  # X-axis
        plt.axvline(0, color='black', linewidth=0.8)  # Y-axis
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.axis([-limit, limit, -limit, limit])  # Set equal limits for both axes
        plt.gca().set_aspect('equal', adjustable='box')  # Ensure equal scaling
        plt.title("Graph Plotter")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.ylim(-20, 20)  # Обмеження для осі Y
        plt.xlim(-20, 20)
        plt.legend()
        plt.show()


# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
