import tkinter as tk
from tkinter import ttk, messagebox
from controller import GraphController


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")

        self.controller = GraphController()
        self.controller.register_callback(self.update_graph_list)

        self._build_ui()

    def _build_ui(self):
        window_width = 800
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        position_x = screen_width - window_width - 100
        position_y = 150

        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        tk.Label(self.root, text="Enter mathematical expression e.g., 1/(1+x) :").grid(row=0, column=0, padx=10, pady=5)
        self.expr_entry = tk.Entry(self.root, width=50)
        self.expr_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Enter x range e.g., -10,10 :").grid(row=1, column=0, padx=10, pady=5)
        self.range_x_entry = tk.Entry(self.root, width=20)
        self.range_x_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Enter display range e.g., -10,10,-10,10 :").grid(row=2, column=0, padx=10, pady=5)
        self.range_display_entry = tk.Entry(self.root, width=20)
        self.range_display_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Select line color:").grid(row=3, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="blue")
        self.color_dropdown = ttk.Combobox(self.root, textvariable=self.color_var,
                                           values=["blue", "red", "green", "orange", "purple"])
        self.color_dropdown.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Plot Graph", command=self.plot_graph).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Load Data from File", command=self.load_file).grid(row=5, column=0, columnspan=2,
                                                                                      pady=10)

        tk.Label(self.root, text="Graphs:").grid(row=6, column=0, padx=10, pady=5)
        self.graph_listbox = tk.Listbox(self.root, height=5, width=50)
        self.graph_listbox.grid(row=6, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Clear All Graphs", command=self.clear_all_graphs).grid(row=7, column=0, columnspan=2,
                                                                                          pady=10)

    def plot_graph(self):
        try:
            expr = self.expr_entry.get()
            range_x = self.range_x_entry.get()
            display_range = self.range_display_entry.get()
            color = self.color_var.get()

            self.controller.add_graph(expr, range_x, display_range, color)
            self.update_graph_list()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_file(self):
        try:
            self.controller.load_file(self.color_var.get(), self.range_display_entry.get())
            self.update_graph_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_all_graphs(self):
        self.controller.clear_graphs()
        self.update_graph_list()

    def update_graph_list(self):
        self.graph_listbox.delete(0, tk.END)
        for graph in self.controller.graphs:
            self.graph_listbox.insert(tk.END, graph[0])


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = GraphApp(tk_root)
    tk_root.mainloop()
