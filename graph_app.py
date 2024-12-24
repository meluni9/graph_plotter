import tkinter as tk
from tkinter import ttk, messagebox
from expression_parser import ExpressionParser
from file_loader import FileLoader
from graph_plotter import GraphPlotter


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")

        self.parser = ExpressionParser()
        self.plotter = GraphPlotter()
        self.graphs = []  # Список для зберігання доданих графіків

        # Entry для математичного виразу
        tk.Label(root, text="Enter mathematical expression e.g., 1/(1+x) :").grid(row=0, column=0, padx=10, pady=5)
        self.expr_entry = tk.Entry(root, width=50)
        self.expr_entry.grid(row=0, column=1, padx=10, pady=5)

        # Entry для діапазону x
        tk.Label(root, text="Enter x range e.g., -10,10 :").grid(row=1, column=0, padx=10, pady=5)
        self.range_x_entry = tk.Entry(root, width=20)
        self.range_x_entry.grid(row=1, column=1, padx=10, pady=5)

        # Entry для діапазону для показу графіка (x, y)
        tk.Label(root, text="Enter display range e.g., -10,10,-10,10 :").grid(row=2, column=0, padx=10, pady=5)
        self.range_display_entry = tk.Entry(root, width=20)
        self.range_display_entry.grid(row=2, column=1, padx=10, pady=5)

        # Dropdown для вибору кольору
        tk.Label(root, text="Select line color:").grid(row=3, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="blue")
        self.color_dropdown = ttk.Combobox(root, textvariable=self.color_var,
                                           values=["blue", "red", "green", "orange", "purple"])
        self.color_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Кнопки
        tk.Button(root, text="Plot Graph", command=self.plot_graph).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Load Data from File", command=self.load_file).grid(row=5, column=0, columnspan=2, pady=10)

        # Список для відображення доданих графіків
        tk.Label(root, text="Graphs:").grid(row=6, column=0, padx=10, pady=5)
        self.graph_listbox = tk.Listbox(root, height=5, width=50)
        self.graph_listbox.grid(row=6, column=1, padx=10, pady=5)

        # Кнопка для очищення всіх графіків
        tk.Button(root, text="Clear All Graphs", command=self.clear_all_graphs).grid(row=7, column=0, columnspan=2,
                                                                                     pady=10)

    def plot_graph(self):
        expr = self.expr_entry.get()
        range_x = self.range_x_entry.get()
        range_display = self.range_display_entry.get()
        color = self.color_var.get()

        if len(self.graphs) >= 5:
            messagebox.showerror("Error", "Maximum number of graphs (5) reached.")
            return

        try:
            x_min, x_max = map(float, range_x.split(','))

            display_range = list(map(float, range_display.split(',')))
            if len(display_range) != 4:
                raise ValueError("Invalid display range. Please enter four values for x and y ranges.")

            x_display_min, x_display_max, y_display_min, y_display_max = display_range

            segments = self.parser.parse_expression(expr, x_min, x_max)

            graph_name = f"Graph {len(self.graphs) + 1}: {expr}"
            self.graphs.append((graph_name, segments, expr, color))
            self.update_graph_list()

            self.plotter.plot_segments(segments, expr, color=color, first_plot=False,
                                       x_display_range=(x_display_min, x_display_max),
                                       y_display_range=(y_display_min, y_display_max))

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_file(self):
        if len(self.graphs) >= 5:
            messagebox.showerror("Error", "Maximum number of graphs (5) reached.")
            return
        try:
            x_values, y_values = FileLoader.load_file()
            if x_values is not None and y_values is not None:
                self.plotter.plot_data(x_values, y_values, "Loaded Data", color=self.color_var.get())

                graph_name = f"Graph {len(self.graphs) + 1}: Loaded Data"
                self.graphs.append((graph_name, x_values, y_values, self.color_var.get()))

                self.update_graph_list()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_graph_list(self):
        self.graph_listbox.delete(0, tk.END)
        for graph in self.graphs:
            self.graph_listbox.insert(tk.END, graph[0])

    def clear_all_graphs(self):
        self.graphs.clear()
        self.plotter.clear_plot()
        self.update_graph_list()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = GraphApp(tk_root)
    tk_root.mainloop()
