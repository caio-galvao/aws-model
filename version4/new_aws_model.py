from lpsolve55 import *
lpsolve()
import copy

#Model for optimizing instance selection in aws ec2

# instance_values = [[[p_hr, p_up, y], [p_hr, p_up, y]], i = 0 
#                    [[p_hr, p_up, y], [p_hr, p_up, y]]] i = 1
# demand = [[1, 2, ...], i=0
#           [1, 2, ...], i=1
#           [1, 2, ...]] i=2

#Todas as instâncias com o mesmo número de mercados (e mercados iguais)

def otimizaModelo(t, demand, input_data):
    num_markets = len(input_data[0])
    num_instances = len(input_data)
    lp = lpsolve('make_lp', 0, num_markets * num_instances * 2 * t)
    lpsolve('set_verbose', lp, 'IMPORTANT')

    obj_func = []

    for instancia in input_data:
        for mercado in instancia: #mercado = [p_hr, p_up, y]
            cr_im = mercado[0] * mercado[2] + mercado[1]
            obj_func.append(0) #a_im * 0
            obj_func.append(cr_im) #r_im * cr_im

    #Objective function
    ret = lpsolve('set_obj_fn', lp, obj_func * t)

    coefficientesBase = criarListaBaseCoefficients(t, num_instances, num_markets)
    #Adding constraints
    #Demand <= 1*a
    constraint1(lp, demand, coefficientesBase)
    # a_t = sum(r_t)
    constraint2(lp, coefficientesBase, input_data)
    
    setInt(lp, 4 * t)
    ret = lpsolve('write_lp', lp, 'a.lp')
    #print(lpsolve('get_mat', lp, 1, 2))
    lpsolve('solve', lp)

    obj = lpsolve('get_objective', lp)
    var = lpsolve('get_variables', lp)[0]
    const = lpsolve('get_constraints', lp)[0]
    #print("Obj: " + str(obj))
    #print("Var: " + str(var))
    #print("Const: " + str(const))

    lpsolve('delete_lp', lp)

    return((round(obj), var))

def constraint1(lp, demand, coefficientsBase):
    for i_tempo in range(len(coefficientsBase)):
        tempo = coefficientsBase[i_tempo]
        for i_instancia in range(len(tempo)):
            coefficients = copy.deepcopy(coefficientsBase) #fazendo uma cópia antes de alterar os coeficientes
            for i_mercado in range(len(coefficients[i_tempo][i_instancia])):
                coefficients[i_tempo][i_instancia][i_mercado] = [1,0]
            ret = lpsolve('add_constraint', lp, transformaEmArray(coefficients), '>=', demand[i_instancia][i_tempo])

def constraint2(lp, coefficientsBase, input_data):
    for i_tempo in range(len(coefficientsBase)):
        tempo = coefficientsBase[i_tempo]
        for i_instancia in range(len(tempo)):
            instancia = tempo[i_instancia]
            for i_mercado in range(len(instancia)):
                coefficients = copy.deepcopy(coefficientsBase) #fazendo uma cópia antes de alterar os coeficientes

                coefficients[i_tempo][i_instancia][i_mercado] = [1, -1]
                
                y = input_data[i_instancia][i_mercado][2]
                duracao_re = y - 1

                for i in range(i_tempo - 1, -1, -1):
                    if duracao_re > 0:
                        coefficients[i][i_instancia][i_mercado] = [0, -1]
                        duracao_re -= 1
                    else: break

                ret = lpsolve('add_constraint', lp, transformaEmArray(coefficients), '=', 0)


def criarListaBaseCoefficients(t, num_instancias, num_mercados): #[[[[0,0], [0,0]], [[0,0], [0,0]]], [[[0,0], [0,0]], [[0,0], [0,0]]]] para t=2, i=2 e m=2
    coefficients = []
    for i_tempo in range(t):
        coef_tempo = []
        for i_instancia in range(num_instancias):
            coef_instancia = []
            for i_mercado in range(num_mercados):
                coef_mercado = [0, 0]
                coef_instancia.append(coef_mercado)
            coef_tempo.append(coef_instancia)
        coefficients.append(coef_tempo)
    
    return coefficients

def transformaEmArray(lista):
    array = []
    for tempo in lista:
        for instancia in tempo:
            for mercado in instancia:
                for valor in mercado:
                    array.append(valor)
    return array

def setInt(lp, n):
    for i in range(1, n + 1):
        ret= lpsolve('set_int', lp, i, True)