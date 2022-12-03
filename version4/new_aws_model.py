from lpsolve55 import *
lpsolve()

#Model for optimizing instance selection in aws ec2
#Considering two markets (on demand and reserve) during a t period of time

# instance_values = [[[p_hr, p_up, y], [p_hr, p_up, y]], i = 0 
#                    [[p_hr, p_up, y], [p_hr, p_up, y]]] i = 1
# demand = [[1, 2, ...], t=0
#           [1, 2, ...], t=1
#           [1, 2, ...]] t=2

def otimizaModelo(t, demand, input):
    lp = lpsolve('make_lp', 0, 4 * t)
    lpsolve('set_verbose', lp, 'IMPORTANT')

    obj_func = []

    for instancia in input:
        for mercado in instancia: #mercado = [p_hr, p_up, y]
            cr_im = mercado[0] * mercado[2] + mercado[1]
            obj_func.append(0) #a_im * 0
            obj_func.append(cr_im) #r_im * cr_im

    #Objective function
    ret = lpsolve('set_obj_fn', lp, obj_func * t)

    #Adding constraints
    #Demand <= 1*a
    constraint1(lp, demand, input)
    # a_t = sum(r_t)
    constraint2(lp)

    constraint2(lp)
    
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

def constraint1(lp, t, demand, input):
    coefficients = []
    for i_tempo in t:
        coef_tempo = []
        for instancia in input:
            coef_instancia = []
            for mercado in instancia:
                coef_mercado = []
        
        ret = lpsolve('add_constraint', lp, coefficients, '>=', demand[i][j]) #Tomar cuidado com forma de entrada de demanda

def constraint2(lp): #y muda p cada mercado!
    ret = lpsolve('add_constraint', lp, coefficients, '=', 0)

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