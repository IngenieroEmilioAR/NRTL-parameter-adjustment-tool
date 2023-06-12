import numpy as np
from dataclasses import dataclass, field

import m00.thermodynamics as thermo



@dataclass
class BinaryMixture:

    substances: list
    liquid_composition: list
    vapor_composition: list
    temperatures: list
    operation_pressure: list
    antoine_constants: list
    saturation_pressure: list = None
    activity_coefficients: list = None
    NRTL_parameters: list = None
    R = 8.314


    def __post_init__(self):
        """Only data threatment"""

        self.liquid_composition = mod1(self.liquid_composition)
        self.vapor_composition = mod1(self.vapor_composition)
        self.saturation_pressure = thermo.saturation_Pressure_Calculation(self.antoine_constants, self.temperatures)
        self.activity_coefficients = thermo.coef_act_by_raoult_mod(self.saturation_pressure, self.liquid_composition, self.vapor_composition, self.operation_pressure)



    def objective_function_vapor_composition(self, param_ab: list):
        """
        Entry: recieves a, b12 and b21 NRTL parameters.

        Returns NRTL parameter's associated error, calculating ir based on the difference
        in vapor compositions
        """

        coef_act = thermo.coef_act(
            self.liquid_composition.T[0], 
            param_ab, 
            self.temperatures)

        y = thermo.raoult_mod(
            coef_act, 
            self.liquid_composition, 
            self.operation_pressure, 
            self.saturation_pressure)

        sum2 = 0

        for i in range(len(self.temperatures)):
            sum2 += (self.vapor_composition[i][0] - y[i][0])**2 + (
                self.vapor_composition[i][1] - y[i][1])**2

        return sum2



    def objective_function_activity_coefficients(self, param_ab: list):
        """
        Retorna el error asociado a los parámetros NRTL con respecto a los
        coeficientes de actividad.
        """

        # temp_calc = []
        # for i in range(len(self.temperaturas)):
        #     t = thermo.calcular_temp_comp(self.composicion_liq[i][0], self.constantes_antoine, self.presion_operacion, param_ab)
        #     temp_calc.append(t)

        coef_act_calc = thermo.coef_act(
            self.liquid_composition.T[0], 
            param_ab, 
            self.temperatures)


        sum1 = 0
        for i in range(len(self.temperatures)):
            a = (self.activity_coefficients[i][0] - coef_act_calc[i][0])**2
            b = (self.activity_coefficients[i][1] - coef_act_calc[i][1])**2
            sum1 += a+b
        
        

        return sum1


    def objf3(self, param_ab):
        """
        Entrada: recibe los parámetros NRTL para el cálculo de los coeficientes 
        de actividad.
        
        Salida: retorna la sumatoria de las diferencias elevadas al cuadrado de
        la energía libre de gibbs experimental vs la calculada.
        """
        

        # temp_calc = []
        # for i in range(len(self.temperaturas)):
        #     t = thermo.calcular_temp_comp(self.composicion_liq[i][0], self.constantes_antoine, self.presion_operacion, param_ab)
        #     temp_calc.append(t)

        
        gibbs_calc = thermo.fgibbs_exc2(
                    self.liquid_composition, 
                    self.temperatures, 
                    param_ab)

        sum1 = 0
        for i in range(len(self.temperatures)):
            sum1 += (self.gibbs_exceso[i] - gibbs_calc[i])**2
        return sum1

        # def calcular_temp_comp2(
        # x: int, 
        # constantes_antoine: list, 
        # p_op: int,
        # param_ab: list,
        # temp: list, 
        # R = 8.314,
        # ) -> list:
        # """
        # Entrada:
        # """


        # a = param_ab[0]
        # b = param_ab[1:]

        # T,y = sy.symbols("T,y")
        # constantes_sust1 = constantes_antoine[0]
        # constantes_sust2 = constantes_antoine[1]


        # eq1 = coef1_func(x, T, a, b)*antoine_TC_Pmmhg(T, constantes_sust1)*0.133322*x - y*p_op
        # eq2 = coef2_func(x, T, a, b)*antoine_TC_Pmmhg(T, constantes_sust2)*0.133322*(1-x) - (1-y)*p_op

        
        # temp, comp = sy.nsolve((eq1,eq2),(T,y),(temp_init, 0.5))
        # return (temp,comp)

    

    def objf4(self, x):
        """
        Entrada: recibe un valor de la composición del sistema en la fase
        líquida.

        Funcionalidad: calcula la temperatura correspondiente a esa composición
        y con T y x evalúa la energía libre de gibbs en exceso (Ge), empleando 
        los parámetros nrtl del sistema.

        Salida: retorna la Ge(T,x)
        """
            
        temp_eval = thermo.calcular_temp_comp(
            x, 
            self.constantes_antoine, 
            self.presion_operacion, 
            self.param_ab
            )

        Ge = thermo.fsgibbs_exc(x, t_eval, self.param_ab)

        return Ge







def mod1(x: list)->list:
    """Recibe un vector de fracciones mol del componente 1 (mezcla binaria)
    y retorna una matriz de dos columnas con las fracciones mol de ambos.
    """
    x = np.array([x])
    x2 = []
    for item in x:
        x2.append(1-item)
    x = np.concatenate((np.transpose(x),np.transpose(x2)), axis = 1)

    return np.array(x)
