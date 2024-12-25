from expression_parser import ExpressionParser
from file_loader import FileLoader
from graph_plotter import GraphPlotter


class GraphController:
    def __init__(self):
        self.graphs = []
        self.parser = ExpressionParser()
        self.plotter = GraphPlotter()
        self.callbacks = []
        self.plotter.set_on_close_callback(self.clear_graphs)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def add_graph(self, expr, range_x, display_range, color):
        if len(self.graphs) >= 5:
            raise ValueError("Maximum number of graphs (5) reached.")

        x_min, x_max = map(float, range_x.split(','))
        display_range_values = list(map(float, display_range.split(',')))
        if len(display_range_values) != 4:
            raise ValueError("Invalid display range. Please enter four values for x and y ranges.")

        segments = self.parser.parse_expression(expr, x_min, x_max)
        graph_name = f"Graph {len(self.graphs) + 1}: {expr}"
        self.graphs.append((graph_name, segments, expr, color))

        for callback in self.callbacks:
            callback()

        x_display_min, x_display_max, y_display_min, y_display_max = display_range_values
        self.plotter.plot_segments(segments, expr, color=color, first_plot=False,
                                   x_display_range=(x_display_min, x_display_max),
                                   y_display_range=(y_display_min, y_display_max))

    def load_file(self, color, display_range):
        if len(self.graphs) >= 5:
            raise ValueError("Maximum number of graphs (5) reached.")

        x_values, y_values = FileLoader.load_file()

        display_range_values = list(map(float, display_range.split(',')))
        x_display_min, x_display_max, y_display_min, y_display_max = display_range_values

        if x_values is not None and y_values is not None:
            graph_name = f"Graph {len(self.graphs) + 1}: Loaded Data"
            self.graphs.append((graph_name, x_values, y_values, color))

            for callback in self.callbacks:
                callback()

            self.plotter.plot_data(x_values, y_values, "Loaded Data", color=color,
                                   x_display_range=(x_display_min, x_display_max),
                                   y_display_range=(y_display_min, y_display_max))

    def clear_graphs(self):
        self.graphs.clear()
        self.plotter.clear_plot()
        for callback in self.callbacks:
            callback()
