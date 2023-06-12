import numpy as np
import sympy as sy




# Relative to activity coefficients

def data_preparation(x: list, a: list, b: list, T: int, R = 8.314) -> list:
    """
    Esta función prepara los valores dados de los parámetros en matrices,
    para que puedan ser usados por la función act_coef_nrtl.
    
    Entrada: recibe una lista de la composición en el líquido a la temperatura T,
    los parámetros alfa y beta en forma de lista -> [alfa] , [beta, beta, beta ...]
    y la temperatura T de evaluación.
    
    Salida: retorna una matriz con los valores G y tau que se emplean para el 
    cálculo de los coeficientes de actividad y de la energía libre de gibbs en
    exceso."""

    A = np.zeros((len(x), len(x))) #matriz con con los valores del parámetro alfa.
    t = np.zeros((len(x), len(x))) #matriz con los valores de los parámetros energéticos. (tau)
    G = np.zeros((len(x), len(x))) #matriz con los valores del parámetro G, función de alfa y tau.
    
    c1 = 0
    c2 = 0
    for i in range(len(x)):
        A[i,i] = 0
        for j in range(i+1,len(x)): #para la matriz A
            A[i,j] = a[c1]
            A[j,i] = a[c1]
            c1+=1

        for j in range(len(x)): #para la matriz t
            if i==j:
                t[i,j] = 0
            else:
                t[i,j] = b[c2]/(R*T)
                c2 +=1
    
    
    for i in range(len(x)): #para la matriz G
        for j in range(len(x)):
            G[i,j] = np.exp(-A[i,j]*t[i,j])

    return G, t




def act_coef_by_nrtl_general_form(x: list, a: list, b: list, T: float, R = 8.314) -> list:
    """Esta función recibe una lista con las fracciones mol
    en el líquido (x) para N sustancias [x1, x2, ... xN], una lista de los parámetros de 
    interacción alfa (a) en orden :
    [a12,a13,a14 ... a1N, a23, a24 ... a2N, a34, a35, ... aN-1,N], 
    los parámetros energéticos beta (b) en orden: 
    [b12,b13,b14 ... b1N, b21, b23, b24, ... b2N, b31,b32,b34 ... b3N ... bN1, bN2 ... bN,N-1]. 
    Retorna una lista con los coeficientes de actividad para cada sustancia 
    a la temperatura T.
    """



    G, t = prep_datos(x, a, b, T, R)
    Y = np.zeros(len(x))

    for i in range(len(x)):
        suma1 = 0
        suma2 = 0
        suma3 = 0


        for j in range(len(x)):
            suma1 += t[j,i]*G[j,i]*x[j]
            suma2 += G[j,i]*x[j]

            suma4 = 0
            suma5 = 0
            suma6 = 0

            for m in range(len(x)):
                suma4 += G[m,j]*x[m]
                suma5 += t[m,j]*G[m,j]*x[m]
                suma6 += G[m,j]*x[m]
            
            suma3 += (G[i,j]*x[j]/suma4)*(t[i,j] - suma5/suma6)
        
        Y[i] = np.exp(suma1/suma2 + suma3)

    return list(Y)


def act_coef_by_nrtl2(x: list, a: list, b: list, T: float, R = 8.314):

    
    t12 = b[0]/(R*T)
    t21 = b[1]/(R*T)
    G12 = sy.exp(-a[0]*t12)
    G21 = sy.exp(-a[0]*t21)

    coef1 = sy.exp(x[1]**2*(t21*(G21/(x[0] + G21*x[1]))**2 + (t12*G12/(x[1] + G12*x[0])**2) ))
    coef2 = sy.exp(x[0]**2*(t12*(G12/(x[1] + G12*x[0]))**2 + (t21*G21/(x[0] + G21*x[1])**2) ))

    Y = [coef1,coef2]
    return Y

def coef_act(x: list, param_ab, T: list, R = 8.314):
    """
    Entrada: recibe una lista correspondiente a la composición del componente 1
    en el líquido, una lista con los parámetros NRTL y otra con las temperaturas
    de evaluación.

    Salida: retorna una matriz de dos columnas con los coeficientes de actividad
    calculados.
    """    

    a = param_ab [0]
    b = param_ab[1:]
    
    coef_act_calc = []
    for i in range(len(T)):
        # print(x[i], T[i])
        #print("fobj:\n",type(a),type(b), type(T[i]), type(x[i]))
        ca1 = coef1_func(x[i], T[i], a, b)
        ca2 = coef2_func(x[i], T[i], a, b)
        coef_act_calc.append([ca1,ca2])
        
    return np.array(coef_act_calc)

# Ley de raoult modificada para soluciones no ideales

def raoult_mod(coef_act: list, frac_mol: list, P_op: float, P_sat: list):
    
    y = [] 
    for i in range(len(coef_act)):
        y1 = P_sat[i][0]*coef_act[i][0]*frac_mol[i][0]/P_op
        y2 = P_sat[i][1]*coef_act[i][1]*frac_mol[i][1]/P_op
        y.append([y1,y2])
        #y.append(np.array(P_sat[i])*np.array(coef_act[i])*np.array(frac_mol[i])/P_op)
    
    return y

def coef_act_by_raoult_mod(P_sat: list, liquid_composition, vapor_composition, P_op):
    pass
    act_coef = []
    for i in range(len(P_sat)):
        act_coef1 = (P_op*vapor_composition[i][0])/(P_sat[i][0]*liquid_composition[i][0])
        act_coef2 = (P_op*vapor_composition[i][1])/(P_sat[i][1]*liquid_composition[i][1])
        act_coef.append([act_coef1,act_coef2])
    
    return act_coef


def fgibbs_exc(x: list, T: list, coef_act: list, R = 8.314):


    gibbs_exc = [
        R*T[i]*(x[i]*np.log(coef_act[i][0]) + 
        (1-x[i])*np.log(coef_act[i][1]))
        for i  in range(len(T))
        ]
    
    return gibbs_exc

def fgibbs_exc2(x: list, T: list, param_ab: list, R = 8.314):
    """
    Entrada: esta función recibe una matriz de dos columnas con los valores de 
    las composiciones en el líquido, una lista con las temperaturas de 
    evaluación, el parámetro a en una lista y los b en una lista.

    Salida: Retorna una lista con los valores de la energía libre de gibbs
    en exceso dividida entre RT.
    """
    a = [param_ab[0]]
    b = param_ab[1:]

    Ge = []
    for i in range(len(T)):
        #print(i)
        t12 = b[0]/(R*T[i])
        t21 = b[1]/(R*T[i])
        G12 = sy.exp(-a[0]*t12)
        G21 = sy.exp(-a[0]*t21)

        aa = x[i][0]*x[i][1]*(
            t12*G21/(x[i][0] + G21*x[i][1]) 
            + t12*G12/(x[i][1] + G12*x[i][0]))
        #print(aa)
        Ge.append(aa)

    return Ge

def fsgibbs_exc(x: int, T: int, param_ab, R = 8.314) -> int:
    """
    Función de evaluación simple.
    Entrada: recibe el valor de la fracción mol en el líquido del componente 1,
    la temperatura T de evaluación y los parámetros nrtl del sistema binario.

    Salida: Retorna la energía libre de Gibbs en exceso evaluada a las
    condiciones dadas.
    """
    t12,t21,G12,G21 = tau_g_nrtl(T, param_ab)
    #Ge = R*T*x*(1-x)*(t21*G21/(x+G21*(1-x)) + t12*G12/((1-x) + G12*x))
    return R*T*x*(1-x)*(t21*G21/(x+G21*(1-x)) + t12*G12/((1-x) + G12*x))

def eval_fsgibbs_exc(x: list, T: list, param_ab, R = 8.314) -> list:
    """
    Entrada: recibe una lista con la fracción mol del componente 1 en el
    líquido, una lista con las temperaturas correspondientes y los parámetros
    del modelo NRTL.

    Salida: retorna una lista con la energía libre de gibbs en exceso
    evaluada a las condiciones dadas.
    """
    Ge = []
    for i in range(len(x)):
        t12,t21,G12,G21 = tau_g_nrtl(T[i], param_ab)
        Ge.append(R*T[i]*x[i]*(1-x[i])*(t21*G21/(x[i]+G21*(1-x[i])) + t12*G12/((1-x[i]) + G12*x[i])))

    return Ge


# Presión de saturación Antoine - Yaws vapor pressure handbook

def p_sat_con_antoine(T: float, constantes: list):
    """
    Entrada: La temperatura T de evaluación y una lista de las constantes
    de antoine de las sustancias de interés
    T -> 345 en K
    constantes -> [[A1, B1, C1], [A2, B2, C2]]

    Salida: retorna una lista con las presiones de saturación de ambas
    sustancias a la temperatura de evaluación.
    p_sat -> [p_sat1, p_sat2] @T [kPa]

    """

    T_eval = T - 273.15 #Temperatura en °C
    p_sat = []
    for item in constantes:
        A,B,C = item[0],item[1],item[2]
        p_sat.append(antoine_T(T_eval, A, B, C)*0.133322) #kPa

    return p_sat

def saturation_Pressure_Calculation(constantes_antoine: list, temperaturas: list) -> list:
    """
    Entrada: lista con las constantes de antoine de las sustancias de interés y
    lista de las temperaturas de evaluación.
    constantes_antoine -> [[A1, B1, C1], [A2, B2, C2]]
    temperaturas -> [35,36,37,38... ] en K

    Salida: lista con las presiones de saturación de las sustancias de interés
    a la temperatura T.

    p_sat -> [[p_sat1@T1, p_sat2@T1], [p_sat1@T2, p_sat2@T2], [...] ]
    p_sat.T (transpose of p_sat)-> [[p_sat1@T1, p_sat1@T2...], [p_sat2@T1, p_sat2@T2 ...]]
    Interesa la transpuesta
    """

    
    p_sat = []
    for i in range(len(temperaturas)):
        p_sat.append(
            p_sat_con_antoine(temperaturas[i], constantes_antoine)
        )

    return np.array(p_sat)

def antoine_T(T: float, A: float, B: float, C: float) -> float:
    """
    Entrada: recibe la temperatura de evaluación y las constantes A, B y C de
    la sustancia.

    Salida: Retorna la presión de saturación.

    Usar cuando se quiera emplear la ecuación de Antoine con log10.
    """
    return 10**(A - B/(T + C))



def antoine_TC_Pmmhg(T: float, const_antoine: list) -> float:
    A = const_antoine[0]
    B = const_antoine[1]
    C = const_antoine[2]
    T_eval = T - 273.15

    return 10**(A- B/(T_eval + C))

def calcular_temp_comp(
    x: int, 
    constantes_antoine: list, 
    p_op: int,
    param_ab: list,
    temp_init: int, 
    R = 8.314,
    ) -> list:
    """
    Entrada:
    """

    a = param_ab[0]
    b = param_ab[1:]

    T,y = sy.symbols("T,y")
    constantes_sust1 = constantes_antoine[0]
    constantes_sust2 = constantes_antoine[1]

    eq1 = coef1_func(x, T, a, b)*antoine_TC_Pmmhg(T, constantes_sust1)*0.133322*x - y*p_op
    eq2 = coef2_func(x, T, a, b)*antoine_TC_Pmmhg(T, constantes_sust2)*0.133322*(1-x) - (1-y)*p_op

    
    temp, comp = sy.nsolve((eq1,eq2),(T,y),(temp_init, x))
    
    return temp,comp

def coef1_func(x: int, T: int, a: int, b:list, R = 8.314)-> int:
    #print("dentro de coef1",x,T,a,b)
    return sy.exp((1-x)**2*(b[1]/(R*T)*(sy.exp(-a*b[1]/(R*T))/(x + sy.exp(-a*b[1]/(R*T))*(1-x)))**2 + (b[0]/(R*T)*sy.exp(-a*b[0]/(R*T))/((1-x) + sy.exp(-a*b[0]/(R*T))*x)**2)))
    

def coef2_func(x: int, T:int, a: int, b: list, R = 8.314)-> int:
    """
    Cálculo del coeficiente de actividad del componente 2 en términos de la
    fracción mol correspondiente al componente 1.
    """
    #print("dentro de coef2",x,T,a,b)
    return sy.exp(x**2*(b[0]/(R*T)*(sy.exp(-a*b[0]/(R*T))/((1-x) + sy.exp(-a*b[0]/(R*T))*x))**2 + (b[1]/(R*T)*sy.exp(-a*b[1]/(R*T))/(x + sy.exp(-a*b[1]/(R*T))*(1-x))**2) ))

def tau_g_nrtl(T:int, param_ab: list, R  = 8.314) -> list:
    a = param_ab[0]
    b = param_ab[1:]

    t12 = b[0]/(R*T)
    t21 = b[1]/(R*T)
    G12 = sy.exp(-a*t12)
    G21 = sy.exp(-a*t21)

    return t12,t21,G12,G21





# param_ab = [0.490950436,4097.766011,-1331.496671]
# constantes_antoine = [[7.79842,1557.4031,219.849],[9.69599,3145.8596,264.246]]
# p_op = 101.3
# x = 0.6584
# a = param_ab[0]
# b = param_ab[1:]

# #print(coef1_func(396.45, a, b))
# print(calcular_temp_comp(x, constantes_antoine, p_op, param_ab))


