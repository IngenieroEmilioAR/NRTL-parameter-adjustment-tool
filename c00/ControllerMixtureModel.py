import inspect
from dataclasses import dataclass, field

import numpy as np


from m00 import ModelBinaryMixture as mbm
from m00 import ModelEvaluations as me
from m00 import optimizers as opt

print

class Distributor:
    

    def do_HandleTheInformation(self, data_frame, type_of_evaluation, evaluation_parameters):
        self.InformationHandler = HandleTheInformation(data_frame, type_of_evaluation, evaluation_parameters)
        self.optimization_results = self.InformationHandler.get_results()
    
    def do_HandlePostOptimization(self):
        self.post_optimization = HandlePostOptimization(self.optimization_results[2], self.InformationHandler.Binary_Mixture)
        self.post_optimization_results = self.post_optimization.generate_calculated_data()

    def get_optimization_results(self):
        return self.optimization_results

    def get_results_evaluation(self):
        return self.post_optimization_results
        






@dataclass
class HandleTheInformation:

    def __init__(self, data_frame, type_of_evaluation, evaluation_parameters):


        """
        This function decides how the evaluation is done.
        Creates the Binary_Mixture object
        Creates the MetaHEvaluation object
        How to proceed when it is wanted to evaluate given NRTL parameters? 
            -> create a class which does the evaluation
        """    
        self.data_frame = data_frame
        substances = [self.data_frame.columns[3], self.data_frame.columns[4]]
        liquid_composition = self.data_frame["x1"]
        vapor_composition = self.data_frame["y1"]
        antoine_constants = [self.data_frame[substances[0]][:3], self.data_frame[substances[1]][:3]]
        operation_pressure = float(evaluation_parameters[0])
        temperatures = self.data_frame["T (K)"]

        limit_values = evaluation_parameters[1]
        particles = evaluation_parameters[2]
        steps = evaluation_parameters[3]
        objective_function = evaluation_parameters[4]
        optimization_algorithm = evaluation_parameters[5]

        type = type_of_evaluation



        self.Binary_Mixture = mbm.BinaryMixture(
            substances, 
            liquid_composition, 
            vapor_composition, 
            temperatures, 
            operation_pressure,
            antoine_constants=antoine_constants
            )
        
        MetaHEvaluaton = me.MetaHEvaluation(
            objective_function, 
            optimization_algorithm, 
            limit_values, 
            particles, 
            steps
            )


        if type == "run":
            self.results = self.run_evaluation(MetaHEvaluaton)
            #print("dentro de handle, después de evaluar self.run", self.results)

        if type == "sensibility":
            pass

    def run_evaluation(self, optimization_object):
        evaluate_me = me.DoTheEvaluation(self.Binary_Mixture, optimization_object)
        if optimization_object.optimization_algorithm == "opt_pso":
            pso_results = evaluate_me.opt_pso()
            return pso_results

        if optimization_object.optimization_algorithm == "opt_gwo":
            gwo_results = evaluate_me.opt_gwo()
            return gwo_results

        if optimization_object.optimization_algorithm == "opt_jaya":
            jaya_results = evaluate_me.opt_jaya()
            return jaya_results

        if optimization_object.optimization_algorithm == "opt_de":
            de_results = evaluate_me.opt_de()
            return de_results
    
        if optimization_object.optimization_algorithm == "opt_all":
            de_results = evaluate_me.opt_de()
            return de_results


    def sensibility_evaluation(self):
        pass


    def get_results(self):
        return self.results




class HandlePostOptimization:

    def __init__(self, NRTL_parameters, binmix_object):
        self.NRTL_parameters = NRTL_parameters
        self.binmix_object = binmix_object
        #print(self.binmix_object.antoine_constants[0], self.binmix_object.antoine_constants[1])

    def generate_calculated_data(self):
        calculated_data = me.ParametersEvaluation()
        results = calculated_data.calculate_data(self.NRTL_parameters, self.binmix_object)
        return results

