import tkinter as tk
from tk_tools import Graph
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PlotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('SerialDispatch Plotter')

        self.graph = Graph(
            self,
            x_min=0.0, x_max=1.0, x_tick=0.2,
            y_min=0.0, y_max=1.0, y_tick=0.2
        )
        self.graph.grid(row=1, column=0)

        self.plot_data = []

        self.mainloop()

    def update_plot(self):
        if len(self.plot_data) == 0:
            return

        self.graph.draw_axes()  # clear axes

        for data in self.plot_data:
            self.graph.plot_line(data)

    def load_new_data(self, data):
        if len(data) == 1:
            if self.plot_data is []:
                self.plot_data = [[]]
            self.plot_data[0].extend([(i, y) for i, y in enumerate(data)])
            return

        if len(data) == 2:
            if self.plot_data is []:
                self.plot_data = [[]]

            self.plot_data[0].extend([(x, y) for x, y in zip(*data)])
            return

        if len(data) == 3:
            if self.plot_data is []:
                self.plot_data = [[], []]

            self.plot_data[0].extend([(x, y0) for x, y0, _ in zip(*data)])
            self.plot_data[1].extend([(x, y1) for x, _, y1 in zip(*data)])
            return

        if len(data) == 4:
            if self.plot_data is []:
                self.plot_data = [[], [], []]

            self.plot_data[0].extend([(x, y0) for x, y0, _, _ in zip(*data)])
            self.plot_data[1].extend([(x, y1) for x, _, y1, _ in zip(*data)])
            self.plot_data[2].extend([(x, y2) for x, _, _, y2 in zip(*data)])
            return

        self.update_plot()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = PlotApp()
