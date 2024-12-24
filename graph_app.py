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

        # Entry для діапазону
        tk.Label(root, text="Enter x range e.g., -10,10 :").grid(row=1, column=0, padx=10, pady=5)
        self.range_entry = tk.Entry(root, width=20)
        self.range_entry.grid(row=1, column=1, padx=10, pady=5)

        # Dropdown для вибору кольору
        tk.Label(root, text="Select line color:").grid(row=2, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="blue")
        self.color_dropdown = ttk.Combobox(root, textvariable=self.color_var, values=["blue", "red", "green", "orange", "purple"])
        self.color_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Кнопки
        tk.Button(root, text="Plot Graph", command=self.plot_graph).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Load Data from File", command=self.load_file).grid(row=4, column=0, columnspan=2, pady=10)

        # Список для відображення доданих графіків
        tk.Label(root, text="Graphs:").grid(row=5, column=0, padx=10, pady=5)
        self.graph_listbox = tk.Listbox(root, height=5, width=50)
        self.graph_listbox.grid(row=5, column=1, padx=10, pady=5)

        # Кнопка для видалення вибраного графіка
        tk.Button(root, text="Delete Selected Graph", command=self.delete_graph).grid(row=6, column=0, columnspan=2, pady=10)

    def plot_graph(self):
        expr = self.expr_entry.get()
        x_range = self.range_entry.get()
        color = self.color_var.get()

        # Перевірка на обмеження кількості графіків
        if len(self.graphs) >= 5:
            messagebox.showerror("Error", "Maximum number of graphs (5) reached.")
            return

        try:
            x_min, x_max = map(float, x_range.split(','))
            segments = self.parser.parse_expression(expr, x_min, x_max)
            self.plotter.plot_segments(segments, expr, color=color, first_plot=False)

            # Додаємо графік до списку
            graph_name = f"Graph {len(self.graphs) + 1}: {expr}"
            self.graphs.append((graph_name, segments, expr, color))

            # Оновлюємо список графіків
            self.update_graph_list()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_file(self):
        try:
            x_values, y_values = FileLoader.load_file()
            if x_values is not None and y_values is not None:
                self.plotter.plot_data(x_values, y_values, "Loaded Data", color=self.color_var.get())

                # Додаємо графік до списку
                graph_name = f"Graph {len(self.graphs) + 1}: Loaded Data"
                self.graphs.append((graph_name, x_values, y_values, self.color_var.get()))

                # Оновлюємо список графіків
                self.update_graph_list()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_graph_list(self):
        # Оновлення списку графіків в інтерфейсі
        self.graph_listbox.delete(0, tk.END)
        for graph in self.graphs:
            self.graph_listbox.insert(tk.END, graph[0])

    def delete_graph(self):
        selected_index = self.graph_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Error", "No graph selected.")
            return

        # Видалення вибраного графіка з списку
        self.graphs.pop(selected_index[0])
        self.update_graph_list()

        # Видалення графіка з малюнку (якщо це потрібно, можна додати)
        # Це не є необхідним для основного функціоналу, але можна розширити, якщо є потреба

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = GraphApp(tk_root)
    tk_root.mainloop()
