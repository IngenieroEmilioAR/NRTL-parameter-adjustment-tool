from dataclasses import dataclass, field
import ast

import numpy as np

import m00.optimizers as opt
import m00.thermodynamics as thermo

@dataclass
class MetaHEvaluation:

    objective_function: str
    optimization_algorithm: str
    limit_values: list
    particles: int
    steps: int



class DoTheEvaluation():

    def __init__(self, binmix_object, optim_object):
        self.objf = getattr(binmix_object, optim_object.objective_function)
        self.limit_values = ast.literal_eval(optim_object.limit_values)
        self.population_size = int(optim_object.particles)
        self.iters = int(optim_object.steps)
        self.lb, self.ub = self.optimization_data_handling(2)
        self.dim = len(self.lb)
        

    def optim_all(self):
        """
        Esta función evalúa la función para preparar los datos y la de 
        optimización. Retorna un diccionario con los parámetros NRTL, el error
        asociado a la mejor evaluación, la mejor ruta y el tiempo de cómputo
        empleando los algoritmos pso, jaya y gwo.
        """
        mejor_eval_pso, mejor_ruta_pso, param_ab_pso, tiempo_pso = opt.pso(
            self.lb,self.ub,self.dim,  self.population_size, self.iters, self.objf
            )
        mejor_eval_gwo, mejor_ruta_gwo, param_ab_gwo, tiempo_gwo = opt.gwo(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        mejor_eval_jaya, mejor_ruta_jaya, param_ab_jaya, tiempo_jaya = opt.jaya(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        mejor_eval_de, mejor_ruta_de, param_ab_de, tiempo_de = opt.de(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        self.results = {
            "pso": {"param_ab": param_ab_pso, "mejor_eval": int(mejor_eval_pso), "mejor_ruta": mejor_ruta_pso, "tiempo": tiempo_pso}, 
            "jaya": {"param_ab": param_ab_jaya, "mejor_eval": int(mejor_eval_jaya), "mejor_ruta": mejor_ruta_jaya, "tiempo": tiempo_jaya}, 
            "gwo": {"param_ab": param_ab_gwo, "mejor_eval": int(mejor_eval_gwo), "mejor_ruta": mejor_ruta_gwo, "tiempo": tiempo_gwo},
            "de": {"param_ab": param_ab_de, "mejor_eval": int(mejor_eval_de), "mejor_ruta": mejor_ruta_de, "tiempo": tiempo_de}
            }
        return self.results

    def opt_pso(self):
        mejor_eval, mejor_ruta, param_ab, tiempo = opt.pso(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        dict_results = {"Asociated Error": [mejor_eval], "α": [param_ab[0]], "g12-g22": [param_ab[1]], "g21-g11": [param_ab[2]], "Calculation Time": [tiempo]}

        return mejor_eval, mejor_ruta, param_ab, tiempo, dict_results

    def opt_gwo(self):
        mejor_eval, mejor_ruta, param_ab, tiempo = opt.gwo(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        dict_results = {"Asociated Error": [mejor_eval], "α": [param_ab[0]], "g12-g22": [param_ab[1]], "g21-g11": [param_ab[2]], "Calculation Time": [tiempo]}

        return mejor_eval, mejor_ruta, param_ab, tiempo, dict_results


    def opt_jaya(self):
        mejor_eval, mejor_ruta, param_ab, tiempo = opt.jaya(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        dict_results = {"Asociated Error": [mejor_eval], "α": [param_ab[0]], "g12-g22": [param_ab[1]], "g21-g11": [param_ab[2]], "Calculation Time": [tiempo]}

        return mejor_eval, mejor_ruta, param_ab, tiempo, dict_results

    def opt_de(self):
        mejor_eval, mejor_ruta, param_ab, tiempo = opt.de(
            self.lb,self.ub,self.dim, self.population_size, self.iters, self.objf
            )
        dict_results = {"Asociated Error": [mejor_eval], "α": [param_ab[0]], "g12-g22": [param_ab[1]], "g21-g11": [param_ab[2]], "Calculation Time": [tiempo]}

        return mejor_eval, mejor_ruta, param_ab, tiempo, dict_results



    def optimization_data_handling(self,no_sustancias: int) -> list:
        """
        Esta función prepara datos para el proceso de optimización.
        Recibe el límite inferior y el superior de los valores de los parámetros
        a determinar y el número de sustancias (n) que componen la mezcla.
        Se designan los primeros n*(n-1)/2 valores límite, correspondientes al
        parámetro alfa, entre 0.2 y 0.5.
        Retorna dos listas, una con los límites inferiores y otra con los superiores.
        """
        lb = np.zeros(
            int(
                no_sustancias*(no_sustancias-1) + no_sustancias*(no_sustancias-1)/2
                )
            )
        ub = np.zeros(len(lb))
        for i in range(len(lb)):
            if i < int(no_sustancias*(no_sustancias-1)/2):
                lb[i] = 0.1#self.limit_values[0]
                ub[i] = 0.6#self.limit_values[1]
            else:
                lb[i] = self.limit_values[0]
                ub[i] = self.limit_values[1]
            
        return lb, ub
        

    def get_metaheuristic_results(self):
        return self.results












class ParametersEvaluation:



    def calculate_data(self, NRTL_parameters, binmix_object):
        """
        This function calculates thermodynamic data given NRTL parameters and 
        a binmix object made from ModelBinaryMixture, object which has other neccesary
        parameters such as temperatures (to give a hint for solve nonlinear system
        of equations to determine T and y), antoine coefficients and operation pressure.

        self.x_eval can have any length, but it is suggested to be equal as
        the binary mixture object's liquid_composition attribute plus a 0 as first
        value and a 1 for last value.

        Optimization cannot proceed if there is a composition of 0.

        """


        self.calculated_temperature = []
        self.calculated_composition = []
        self.x_eval = self.prepare_x_eval(binmix_object)
        here = len(binmix_object.temperatures)
        temp_hint = np.linspace(binmix_object.temperatures[0], binmix_object.temperatures[here-1], 25)

        for i in range(len(self.x_eval)):

            T, y= thermo.calcular_temp_comp(
                self.x_eval[i],
                binmix_object.antoine_constants,
                binmix_object.operation_pressure,
                NRTL_parameters,
                temp_hint[i]
                )
            self.calculated_temperature.append(T)
            self.calculated_composition.append(y)

        
        self.calc_activity_coefficient = thermo.coef_act(
            self.x_eval, 
            NRTL_parameters, 
            self.calculated_temperature
            )
        
        self.calculated_excess_gibbss_free_energy = thermo.eval_fsgibbs_exc(
            self.x_eval, 
            self.calculated_temperature, 
            NRTL_parameters
            )

        obtained_data = [
            np.array(self.x_eval),
            np.array(self.calculated_composition),
            np.array(self.calculated_temperature),
            np.array(self.calc_activity_coefficient), 
            np.array(self.calculated_excess_gibbss_free_energy),
            ]
        
        dict = {
            "T (K)": np.array(self.calculated_temperature), 
            "x1": np.array(self.x_eval), 
            "y1": np.array(self.calculated_composition),
            "Activity coefficient 1": np.array(self.calc_activity_coefficient).T[0],
            "Activity coefficient 2": np.array(self.calc_activity_coefficient).T[1],
            "Calculated Gibbs free energy": np.array(self.calculated_excess_gibbss_free_energy)}
        

        return obtained_data, dict

    def last_error_evaluation(self):

        for i in range(len(self.cal)):
            sum2 += (self.vapor_composition[i][0] - y[i][0])**2 + (
                self.vapor_composition[i][1] - y[i][1])**2



    def prepare_x_eval(self, binmix_object):
        x_eval = np.array(binmix_object.liquid_composition).T[0]
        x1 = x_eval[0]

        if (1-x1) > 0.5 and (1-x1)!= 0:
            x_eval = np.insert(x_eval, 0, 0)
            x_eval = np.append(x_eval, 1)
        if (1-x1) < 0.5 and (1-x1) != 1:
            x_eval = np.insert(x_eval, 0, 1)
            x_eval = np.append(x_eval, 0)

        return x_eval

        




    
    def get_all_results(self):
        return self.results