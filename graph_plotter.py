import matplotlib.pyplot as plt

class GraphPlotter:
    def __init__(self):
        self.default_color = "blue"
        self.fig = None

    def plot_segments(self, segments, expr, color="blue", first_plot=True, x_display_range=None, y_display_range=None):
        if first_plot:
            self.fig = plt.figure(figsize=(8, 6))
        else:
            if self.fig is None:
                self.fig = plt.figure(figsize=(8, 6))

            plt.figure(self.fig.number)

        first_segment = True
        for x_seg, y_seg in segments:
            if first_segment:
                plt.plot(x_seg, y_seg, color=color, linewidth=2, label=expr)
                first_segment = False
            else:
                plt.plot(x_seg, y_seg, color=color, linewidth=2)

        self._setup_axes(x_display_range, y_display_range)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc='upper right')

        plt.show()

    def plot_data(self, x_values, y_values, label, color="blue", x_display_range=None, y_display_range=None):
        if self.fig is None:
            self.fig = plt.figure(figsize=(8, 6))

        plt.figure(self.fig.number)
        plt.plot(x_values, y_values, color=color, linewidth=2, label=label)
        self._setup_axes(x_display_range, y_display_range)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc='upper right')
        plt.show()

    def _setup_axes(self, x_display_range=None, y_display_range=None):
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        if x_display_range and y_display_range:
            ax.set_xlim(x_display_range)
            ax.set_ylim(y_display_range)
        else:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            x_range = abs(xlim[1] - xlim[0])
            y_range = abs(ylim[1] - ylim[0])
            max_range = max(x_range, y_range)

            x_center = (xlim[0] + xlim[1]) / 2
            y_center = (ylim[0] + ylim[1]) / 2

            ax.set_xlim(x_center - max_range / 2, x_center + max_range / 2)
            ax.set_ylim(y_center - max_range / 2, y_center + max_range / 2)

        ax.set_aspect('equal', adjustable='box')

    def clear_plot(self):
        if self.fig:
            plt.clf()
            plt.close(self.fig)
            self.fig = None
