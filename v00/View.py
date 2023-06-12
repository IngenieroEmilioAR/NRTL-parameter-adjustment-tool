import os


from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


from v00.ViewGraph import Graph
from v00.ViewStatus import Status
#from v00.ViewSensitivity import SensitivityDialog 

import c00.OpenDataFile as odf

from c00 import ControllerMixtureModel as cmm
from m00 import ModelBinaryMixture as mbm
from m00 import ModelEvaluations as me



class ViewClass(qtw.QWidget):
    

    def __init__(self):
        super().__init__()

        self.layoutsUI()
        self.container_widgets()

        self.entry_widgets()
        self.optimization_widgets()

        self.view_class_status = Status()       
        self.status_Widgets()

        self.main_controller = cmm.Distributor()

        self.count = 0




    def layoutsUI(self):

        self.main_layout = qtw.QHBoxLayout() #Main layout
        self.setLayout(self.main_layout) #Stablishing the main layout as the main layout

        self.layout_entry = qtw.QVBoxLayout()#Layout of the Data Entry zone
        self.layout_graphs = qtw.QVBoxLayout()#Layout of the Graphs zone
        
        self.layout_entry_entry = qtw.QGridLayout() #Layout of the Data Entry's Entry zone
        self.layout_entry_optim = qtw.QGridLayout() #Layout of the Data Entry's Optimization zone
        self.layout_entry_status = qtw.QVBoxLayout()#Layout for the data table zone


    def container_widgets(self):

        entry = qtw.QWidget(self)
        #data = qtw.QGroupBox("Status")
        graphs = qtw.QGroupBox("Graphs")


        self.main_mdi_area = qtw.QMdiArea()
        self.main_mdi_area.showMinimized()


        entry_entry = qtw.QGroupBox("Thermodynamic Data Entry")
        entry_optim = qtw.QGroupBox("Optimization Data Entry")
        entry_status = qtw.QGroupBox("Status")

        self.main_layout.addWidget(entry)
        #self.main_layout.addWidget(data)
        #self.main_layout.addWidget(graphs)
        self.main_layout.addWidget(self.main_mdi_area)


        entry.setLayout(self.layout_entry)
        graphs.setLayout(self.layout_graphs)
        #data.setLayout(self.layout_status)

        self.layout_entry.addWidget(entry_entry)
        self.layout_entry.addWidget(entry_optim)
        self.layout_entry.addWidget(entry_status)

        entry_entry.setLayout(self.layout_entry_entry)
        entry_optim.setLayout(self.layout_entry_optim)
        entry_status.setLayout(self.layout_entry_status)


    def entry_widgets(self):

        search_button = qtw.QPushButton(
            "Select File",
            clicked = self.open_file_and_modify
            )

        pressure_label = qtw.QLabel("Pressure")
        kPa_label = qtw.QLabel("kPa")

        self.lineedit_pressure = qtw.QLineEdit(
            "101.325",
            self,
        )

        self.layout_entry_entry.addWidget(search_button,0,0,1,3)
        self.layout_entry_entry.addWidget(pressure_label,1,0)
        self.layout_entry_entry.addWidget(self.lineedit_pressure,1,1)
        self.layout_entry_entry.addWidget(kPa_label,1,2)


    def optimization_widgets(self):

        #Labels for the different options

        label_objective_function = qtw.QLabel("Objective Function")
        label_optimization_algorithm = qtw.QLabel("Optimization algorithm")
        label_limit_values = qtw.QLabel("Limit values")
        label_particles_or_population = qtw.QLabel("Particles/Population")
        label_steps_iterations = qtw.QLabel("Iterations")


        #ComboBoxes
        self.combobox_objective_functions = qtw.QComboBox(self)
        self.combobox_optimization_algorithms = qtw.QComboBox(self)

        items_in_objective_functions = self.get_objective_functions()
        items_in_optimization_algorithms = self.get_optimization_algorithms()

        self.combobox_objective_functions.addItems(items_in_objective_functions)
        self.combobox_optimization_algorithms.addItems(items_in_optimization_algorithms)

        self.combobox_objective_functions.setCurrentIndex(self.combobox_objective_functions.count() -1)
        self.combobox_optimization_algorithms.setCurrentIndex(self.combobox_optimization_algorithms.count() -1)


        #LineEdits
        self.lineedit_limit_values = qtw.QLineEdit(
            "[-50000,50000]",
            self,
        )
        self.lineedit_particles_or_population = qtw.QLineEdit(
            "10",
            self,
        )
        self.lineedit_steps_iterations = qtw.QLineEdit(
            "5",
            self,
        )

        #Buttons
        self.run_button = qtw.QPushButton(
            "Run",
            self,
            clicked = self.run_Function
            )

        # self.sensitivity_analysis_button = qtw.QPushButton(
        #     "Sensitivity Analysis",
        #     self,
        #     clicked = self.sensitivity_analysis_function
        #     )



        #Putting widgets into label
        self.layout_entry_optim.addWidget(label_objective_function, 0, 0)
        self.layout_entry_optim.addWidget(label_optimization_algorithm, 1, 0)
        self.layout_entry_optim.addWidget(label_limit_values, 2, 0)
        self.layout_entry_optim.addWidget(label_particles_or_population, 3, 0)
        self.layout_entry_optim.addWidget(label_steps_iterations, 4, 0)
        

        self.layout_entry_optim.addWidget(self.combobox_objective_functions, 0, 1, 1, 2)
        self.layout_entry_optim.addWidget(self.combobox_optimization_algorithms, 1, 1, 1, 2)
        self.layout_entry_optim.addWidget(self.lineedit_limit_values, 2, 1, 1, 2)
        self.layout_entry_optim.addWidget(self.lineedit_particles_or_population, 3, 1, 1, 2)
        self.layout_entry_optim.addWidget(self.lineedit_steps_iterations, 4, 1, 1, 2)
        self.layout_entry_optim.addWidget(self.run_button, 5, 1, 1, 1)
        #self.layout_entry_optim.addWidget(self.sensitivity_analysis_button, 5, 2, 1, 1)

    #pending extention
    def status_Widgets(self):
        self.status_text_edit = qtw.QTextEdit(
            readOnly = True
        )

        self.layout_entry_status.addWidget(self.status_text_edit)

        self.status_text_edit.append(self.view_class_status.initial_text())


    def get_objective_functions(self):
        members = dir(mbm.BinaryMixture)
        functions = []

        for element in members:
            if element.startswith('objective'):
                functions.append(element)
        return functions

    
    def get_optimization_algorithms(self):
        members = dir(me.DoTheEvaluation)
        functions = []

        for element in members:
            if element.startswith('opt_'):
                functions.append(element)
        return functions
    

    def MDI(self, widget, title, span = 0, type = "table"):
        """
        To create a sub window with given title and widget
        """
        new_MDI_window = qtw.QMdiSubWindow()
        new_MDI_window.setWindowTitle(title)
        new_MDI_window.setWidget(widget)
        self.main_mdi_area.addSubWindow(new_MDI_window)      
        new_MDI_window.show()

        if type == "table":
            new_MDI_window.setGeometry(0,0 + span, 1200,100)
            try:
                new_MDI_window.setWindowIcon(qtg.QIcon(".\images\table.png"))        
            except:
                pass
        else: 
            new_MDI_window.setGeometry(0,0 + span, 1200,700)
            try:
                new_MDI_window.setWindowIcon(qtg.QIcon(".\images\graph.png"))
            except:
                pass



    def run_Function(self):
        self.count += 1
        self.span = 0
        self.minimize_all_subwindows()

        run_parameters = [
            self.lineedit_pressure.text(), 
            self.lineedit_limit_values.text(), 
            self.lineedit_particles_or_population.text(), 
            self.lineedit_steps_iterations.text(),
            self.combobox_objective_functions.currentText(),
            self.combobox_optimization_algorithms.currentText()
            ]


        try:
            self.status_text_edit.append(self.view_class_status.optimization_initialized())
            qtw.QApplication.processEvents()
            #optimization results (has the best_evaluation (error) route, NRTL parameters and time of evaluation)
            self.run_optimization_results = self.common_function('run', run_parameters)
        except ValueError:
            print("Value error, No datafile was selected")
            return
        except KeyError:
            self.status_text_edit.append(self.view_class_status.optimization_cannot_be_initialized())
            qtw.QApplication.processEvents()
            return
        except AttributeError:
            self.status_text_edit.append(self.view_class_status.no_data())
            return

        self.status_text_edit.append(self.view_class_status.optimization_completed())
        self.show_run_results_tabulated(self.run_optimization_results[-1], f"Optimization results, run {self.count} - {self.true_name}", self.span)
        self.span += 100

        qtw.QApplication.processEvents()

        #calculated data liquid and vapor composition for component 1, temperature, activity coefficients and gibbs' free energy
        try:
            calculated_data = self.evaluate_obtained_parameters()
            calculated_data, calculated_dict = calculated_data[0], calculated_data[1] 
            self.status_text_edit.append(self.view_class_status.evaluation_completed())
        except ZeroDivisionError:
            print("Thermodynamics calculations did not converge")
            pass
        except ValueError:
            print("Thermodynamics calculations did not converge")
            pass

        #Showing results
        self.show_run_results_tabulated(calculated_dict, f"Calculated data run {self.count} - {self.true_name}", self.span)
        self.span += 100
        self.show_run_results_graphically(calculated_dict, self.span)


    def show_run_results_tabulated(self, data, title, span):
        data_table = odf.TableCreation().get_Data_Table(data)
        self.MDI(data_table, title, span)
        
        
    def show_run_results_graphically(self, data, span):
        
        graphs_layout = qtw.QGridLayout()
        graphs_container = qtw.QWidget(self)
        graphs_container.setLayout(graphs_layout)

        xy_canvas = self.graphs_section_xy(data)
        xvsac_canvas = self.graphs_section_xvsac(data)
        xyT_canvas = self.graphs_section_xyT(data)
        xvsGe_canvas = self.graphs_section_xGe(data)

        graphs_layout.addWidget(xy_canvas, 0,0)
        graphs_layout.addWidget(xvsac_canvas, 0,1)
        graphs_layout.addWidget(xyT_canvas, 1,0)
        graphs_layout.addWidget(xvsGe_canvas, 1,1)

        
        

        self.MDI(graphs_container, f"Graphical results run {self.count} - {self.true_name}", span, type = "graphs")
        


#pass
    def sensitivity_analysis_function(self):
        self.dialogo = SensitivityDialog()
        self.dialogo.exec()



    def common_function(self,type_of_evaluation, evaluation_parameters):
        self.main_controller.do_HandleTheInformation(self.data_frame, type_of_evaluation, evaluation_parameters)        
        results_optimization = self.main_controller.get_optimization_results()
        #print("En common function", results_optimization)
        return results_optimization



    def graphs_section_xy(self, data):
        
        graph = Graph(x_data = self.data_frame["x1"], y_data =self.data_frame["y1"], label = "Experimental", title = "x vs y", x_axis_name = "Liquid composition", y_axis_name = "Vapor composition")
        graph.add_info_plot(data["x1"], data["y1"], label = "Calculated")
        canvas = FigureCanvasQTAgg(graph)

        return canvas


        
    def graphs_section_xvsac(self, data):
        graph = Graph(data["x1"], data["Activity coefficient 1"], label = "Activity coefficient for 1", title = "Activity coefficients vs x", x_axis_name = "Liquid composition for 1", y_axis_name = "Activity coefficients", way ="plot")
        graph.add_info_plot(data["x1"], data["Activity coefficient 2"], label ="Activity coefficient 2")
        canvas = FigureCanvasQTAgg(graph)
        return canvas


    def graphs_section_xyT(self, data):
        graph = Graph(self.data_frame["x1"], self.data_frame["T (K)"], label = "Experimental Liquid Frac", title = "x1 and y1 vs T", x_axis_name="Molar composition", y_axis_name="Temperature (K)")
        graph.add_info_scatter(self.data_frame["y1"], self.data_frame["T (K)"], label = "Experimental Vapor Frac")
        graph.add_info_plot(data["x1"], data["T (K)"], label = "Calculated Liquid Frac")
        graph.add_info_plot(data["y1"], data["T (K)"], label = "Calculated Vapor Frac")
        canvas = FigureCanvasQTAgg(graph)

        return canvas
        




    def graphs_section_xGe(self, data):
        graph = Graph(data["x1"], data["Calculated Gibbs free energy"], label = "Calculated liquid composition",  title = "x1 vs Ge", x_axis_name="Molar composition", y_axis_name="Excess Gibbss Free Energy", way = "plot")
        canvas = FigureCanvasQTAgg(graph)
        return canvas





    def open_file_and_modify(self):
        """
        Add a controller to fit the table shape.
        The creation of the mdi sub window is here, try to
        move it to only create the dataframe and
        make it possible to the user to decide either if the data is
        instantly shown or just saved, and can be visualized if user decides so.
        
        For now, it is just ok.
        """
        self.count = 0
        try:
            self.data_table, self.data_frame, self.route = odf.TableCreation().get_Data_Table()
            self.true_name = self.get_true_name_of_route(self.route).split(".")[0]
            title = f"{self.true_name} experimental data"
            self.MDI(self.data_table,title)
            self.status_text_edit.append(self.view_class_status.after_data_selection(self.true_name))

        except FileNotFoundError:
            print("open and modifyNo datafile was selected")
        
        
        
    def get_true_name_of_route(self, route):
        name = os.path.basename(route)
        return name

    def evaluate_obtained_parameters(self):
        self.main_controller.do_HandlePostOptimization()
        results_evaluation = self.main_controller.get_results_evaluation()
        return results_evaluation

    def minimize_all_subwindows(self):
        subwindows = self.main_mdi_area.subWindowList()
        for subwindow in subwindows:
            subwindow.showMinimized()

            
            

    # def close_all_subwindows(self):
    #     self.main_mdi_area.closeAllSubWindows()
    
    # def cascade_subwindows(self):
    #     self.main_mdi_area.cascadeSubWindows()

    # def tile_subwindows(self):
    #     self.main_mdi_area.tileSubWindows()
