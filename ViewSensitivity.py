from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


from m00 import ModelBinaryMixture as mbm
from m00 import ModelEvaluations as me

from c00 import OpenDataFile as odf



class SensitivityDialog(qtw.QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Senstivity Analysis")

        self.layoutsUI()
        self.container_widgets()

        self.optimization_widgets()
        self.analysis_widgets()
        self.save_to_widgets()

    def layoutsUI(self):
        self.main_layout = qtw.QVBoxLayout()
        self.setLayout(self.main_layout) #Main layout

        self.analysis_layout = qtw.QGridLayout()
        self.optimization_layout = qtw.QGridLayout()
        self.save_layout = qtw.QGridLayout()



    def container_widgets(self):
        optimization_groupbox = qtw.QGroupBox("Optimization")
        optimization_groupbox.setLayout(self.optimization_layout)
        self.main_layout.addWidget(optimization_groupbox)

        analysis_groupbox = qtw.QGroupBox("Analysis")
        analysis_groupbox.setLayout(self.analysis_layout)
        self.main_layout.addWidget(analysis_groupbox)

        save_groupbox = qtw.QGroupBox("Saving")
        save_groupbox.setLayout(self.save_layout)
        self.main_layout.addWidget(save_groupbox)
    

    def analysis_widgets(self):
        #Analysis parameters    

        self.repeat_checkbox = qtw.QCheckBox(
            "Repeat",
            self,
            checkable = True,
            checked = False)
        self.repeat_label = qtw.QLabel("Times")
        self.repeat_lineedit = qtw.QLineEdit(
            "5",
            self)


        self.vary_particles_checkbox = qtw.QCheckBox(
            "Vary particles",
            checkable = True,
            checked = False)
        self.from_particles_label = qtw.QLabel("From")
        self.to_particles_label = qtw.QLabel("To")
        self.each_particles_label = qtw.QLabel("Step")
        self.from_particles_lineedit = qtw.QLineEdit(
            "1",
            self)
        self.to_particles_lineedit = qtw.QLineEdit(
            "5",
            self)
        self.each_particles_lineedit= qtw.QLineEdit(
            "1",
            self)


        self.vary_iterations_checkbox = qtw.QCheckBox(
            "Vary iterations",
            checkable = True,
            checked = False
        )
        self.from_iterations_label = qtw.QLabel("From")
        self.to_iterations_label = qtw.QLabel("To")
        self.each_iterations_label = qtw.QLabel("Step")
        self.from_iterations_lineedit = qtw.QLineEdit(
            "1",
            self)
        self.to_iterations_lineedit = qtw.QLineEdit(
            "5",
            self)
        self.each_iterations_lineedit = qtw.QLineEdit(
            "1",
            self)

        self.from_particles_label.setAlignment(qtc.Qt.AlignRight)
        self.to_particles_label.setAlignment(qtc.Qt.AlignRight)
        self.each_particles_label.setAlignment(qtc.Qt.AlignRight)
        self.from_iterations_label.setAlignment(qtc.Qt.AlignRight)
        self.to_iterations_label.setAlignment(qtc.Qt.AlignRight)
        self.each_iterations_label.setAlignment(qtc.Qt.AlignRight)



        self.analysis_layout.addWidget(self.repeat_checkbox, 0,0,1,1)
        self.analysis_layout.addWidget(self.repeat_lineedit, 0,1,1,1)
        self.analysis_layout.addWidget(self.repeat_label,0,2,1,1)
        
        self.analysis_layout.addWidget(self.vary_particles_checkbox, 1,0,1,1)
        self.analysis_layout.addWidget(self.from_particles_label, 1,1,1,1)
        self.analysis_layout.addWidget(self.from_particles_lineedit, 1,2,1,1)
        self.analysis_layout.addWidget(self.to_particles_label, 2,1,1,1)
        self.analysis_layout.addWidget(self.to_particles_lineedit, 2,2,1,1)
        self.analysis_layout.addWidget(self.each_particles_label,3,1,1,1)
        self.analysis_layout.addWidget(self.each_particles_lineedit,3,2,1,1)
        
        self.analysis_layout.addWidget(self.vary_iterations_checkbox, 4,0,1,1)
        self.analysis_layout.addWidget(self.from_iterations_label, 4,1,1,1)
        self.analysis_layout.addWidget(self.from_iterations_lineedit, 4,2,1,1)
        self.analysis_layout.addWidget(self.to_iterations_label, 5,1,1,1)
        self.analysis_layout.addWidget(self.to_iterations_lineedit, 5,2,1,1)
        self.analysis_layout.addWidget(self.each_iterations_label,6,1,1,1)
        self.analysis_layout.addWidget(self.each_iterations_lineedit,6,2,1,1)


        self.repeat_lineedit.setEnabled(False)
        self.from_iterations_lineedit.setEnabled(False)
        self.to_iterations_lineedit.setEnabled(False)
        self.each_iterations_lineedit.setEnabled(False)
        self.from_particles_lineedit.setEnabled(False)
        self.to_particles_lineedit.setEnabled(False)
        self.each_particles_lineedit.setEnabled(False)

        self.repeat_checkbox.stateChanged.connect(self.hide_repeat_lineedit)
        self.vary_particles_checkbox.stateChanged.connect(self.hide_particles_lineedit)
        self.vary_iterations_checkbox.stateChanged.connect(self.hide_iterations_lineedit)
                
    #optimization widgets creation and positioning into dialog
    def optimization_widgets(self):
        optimization_groupbox = qtw.QGroupBox("Optimization")

        label_objective_function = qtw.QLabel("Objective Function")
        label_optimization_algorithm = qtw.QLabel("Optimization algorithm")
        label_limit_values = qtw.QLabel("Limit values")

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


        self.optimization_layout.addWidget(label_objective_function, 0,0,1,1)
        self.optimization_layout.addWidget(label_optimization_algorithm, 1,0,1,1)
        self.optimization_layout.addWidget(label_limit_values, 2,0,1,1)

        self.optimization_layout.addWidget(self.combobox_objective_functions, 0,1,1,1)
        self.optimization_layout.addWidget(self.combobox_optimization_algorithms, 1,1,1,1)
        self.optimization_layout.addWidget(self.lineedit_limit_values, 2,1,1,1)


    def save_to_widgets(self):
        
        self.save_to_f_button = qtw.QPushButton(
            "Save to existing file",
            self,
            clicked = self.save_to_existing_file
        )
        self.run_sensibility_button = qtw.QPushButton(
            "Run",
            self,
            clicked = self.run_sensitivity
        )

        self.save_layout.addWidget(self.save_to_f_button)
        self.save_layout.addWidget(self.run_sensibility_button)


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


    def hide_repeat_lineedit(self, state):
        if state == qtc.Qt.Checked:
            self.repeat_lineedit.setEnabled(True)
        else:
            self.repeat_lineedit.setEnabled(False)


    def hide_particles_lineedit(self, state):
        if state == qtc.Qt.Checked:
            self.from_particles_lineedit.setEnabled(True)
            self.to_particles_lineedit.setEnabled(True)
            self.each_particles_lineedit.setEnabled(True)
        else:
            self.from_particles_lineedit.setEnabled(False)
            self.to_particles_lineedit.setEnabled(False)
            self.each_particles_lineedit.setEnabled(False)

    def hide_iterations_lineedit(self, state):
        if state == qtc.Qt.Checked:
            self.from_iterations_lineedit.setEnabled(True)
            self.to_iterations_lineedit.setEnabled(True)
            self.each_iterations_lineedit.setEnabled(True)
        else:
            self.from_iterations_lineedit.setEnabled(False)
            self.to_iterations_lineedit.setEnabled(False)
            self.each_iterations_lineedit.setEnabled(False)

    def save_to_existing_file(self):
        route = odf.DataFileRoute()


    def save_to_new_file(self):
        pass


    def run_sensitivity(self):
        pass