import tkinter as tk
from tkinter import ttk, messagebox

from controller import Controller


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")

        self.controller = Controller()
        self.controller.register_callback(self.update_graph_list)

        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        window_width, window_height = 800, 400
        screen_width = self.root.winfo_screenwidth()
        position_x, position_y = screen_width - window_width - 100, 150
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def _create_widgets(self):
        self._create_input_fields()
        self._create_color_selector()
        self._create_buttons()
        self._create_graph_list()

    def _create_input_fields(self):
        tk.Label(self.root, text="Enter mathematical expression e.g., 1/(1+x):").grid(row=0, column=0, padx=10, pady=5)
        self.expr_entry = tk.Entry(self.root, width=50)
        self.expr_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Enter x range e.g., -10,10:").grid(row=1, column=0, padx=10, pady=5)
        self.range_x_entry = tk.Entry(self.root, width=20)
        self.range_x_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Enter display range e.g., -10,10,-10,10:").grid(row=2, column=0, padx=10, pady=5)
        self.range_var = tk.StringVar(value="-10,10,-10,10")
        self.range_display_entry = tk.Entry(self.root, textvariable=self.range_var, width=20)
        self.range_display_entry.grid(row=2, column=1, padx=10, pady=5)

    def _create_color_selector(self):
        tk.Label(self.root, text="Select line color:").grid(row=3, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="blue")
        self.color_dropdown = ttk.Combobox(self.root, textvariable=self.color_var,
                                           values=["blue", "red", "green", "orange", "purple"])
        self.color_dropdown.grid(row=3, column=1, padx=10, pady=5)

    def _create_buttons(self):
        tk.Button(self.root, text="Plot Graph", command=self.app_graph).grid(row=4, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Load Data from File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export Graph Data", command=self.export_data).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save Graph as Image", command=self.save_image).pack(side=tk.RIGHT, padx=5)

        tk.Button(self.root, text="Clear All Graphs", command=self.clear_graphs).grid(row=6, column=0, columnspan=2,
                                                                                      pady=10)

    def _create_graph_list(self):
        tk.Label(self.root, text="Graphs:").grid(row=7, column=0, padx=10, pady=5)
        self.graph_listbox = tk.Listbox(self.root, height=5, width=50)
        self.graph_listbox.grid(row=7, column=1, padx=10, pady=5)

    def app_graph(self):
        try:
            expr = self.expr_entry.get()
            range_x = self.range_x_entry.get()
            display_range = self.range_display_entry.get()
            color = self.color_var.get()
            self.controller.add_graph(expr, range_x, display_range, color)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_file(self):
        try:
            self.controller.load_file(self.color_var.get(), self.range_display_entry.get())
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_graphs(self):
        self.controller.clear_graphs()

    def update_graph_list(self):
        self.graph_listbox.delete(0, tk.END)
        for graph in self.controller.graphs:
            self.graph_listbox.insert(tk.END, graph[0])

    def export_data(self):
        selected = self.graph_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No graph selected!")
            return

        try:
            self.controller.export_data(selected[0])
        except Exception as e:
            messagebox.showerror("Error", f"Could not save graph: {e}")

    def save_image(self):
        self.controller.save_image()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = App(tk_root)
    tk_root.mainloop()
