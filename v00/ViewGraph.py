import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure




class Graph(Figure):

    def __init__(self, x_data, y_data, label, title, x_axis_name=None, y_axis_name=None, way = None,parent=None, width=5, height=4, dpi=80):
        super().__init__(figsize=(width, height), dpi=dpi)  

        self.ax = self.add_subplot(111)  

        if way == None:
            self.ax.scatter(x_data, y_data, label = label, marker = "+").set(color = "red")
        elif way == "plot":
            self.ax.plot(x_data, y_data, label = label)


        self.ax.set_xlabel(x_axis_name)
        self.ax.set_ylabel(y_axis_name)
        self.ax.legend()
        self.ax.title.set_text(f"{title}")
        self.ax.grid()        



    def add_info_plot(self, additional_x, additional_y, label):
        self.ax.plot(additional_x, additional_y, label = label)
        self.ax.legend()

    def add_info_scatter(self, additional_x, additional_y, label):
        self.ax.scatter(additional_x, additional_y, label = label, marker = "^").set(color = "green")
        self.ax.legend()


    def get_figure(self):
        return ax


