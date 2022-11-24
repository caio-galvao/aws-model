from lpsolve55 import *
lpsolve()

#Model for optimizing instance selection in aws ec2
#Considering two markets (on demand and reserve) during a t period of time

# instance_values = [[[p_hr, p_up, y], [p_hr, p_up, y]], i = 0 
#                    [[p_hr, p_up, y], [p_hr, p_up, y]]] i = 1
# demand = [[1, 2, ...], t=0
#           [1, 2, ...], t=1
#           [1, 2, ...]] t=2

def otimizaModelo(t, demand, instances_values):
    lp = lpsolve('make_lp', 0, 4 * t)
    lpsolve('set_verbose', lp, 'IMPORTANT')
    
    duracao_reservas = []
    obj = []
    for values_i in instances_values: #for every instance
        num_markets = len(values_i)
        for values_m in values_i:  #for every market
            p_hr = values_m[0]
            p_up = values_m[1]
            y = values_m[2]
            duracao_reservas.append(y)
            
            cr_re = p_up + p_hr * y
            obj.append(0)
            obj.append(cr_re)

    #Objective function: C = a_od * 0 + r_od * cr_od + a_re * 0 + r_re * cr_re
    ret = lpsolve('set_obj_fn', lp, obj * t)

    #Adding constraints
    #Demand <= 1*a
    constraint1(lp, t, demand, len(instances_values), num_markets)
    # a_t = sum(r_t)
    constraint2(lp, t, len(instances_values), num_markets, duracao_reservas)
    
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

def constraint1(lp, t, demand, num_instances, num_markets):
    for i in range(t):
        coefficients_t_start = [0, 0] * num_markets * num_instances * i #p/ tempos anteriores
        coefficients_t_end = [0, 0] * num_markets * num_instances * (t - i - 1) #p/ tempos posteriores

        for j in range(num_instances): #p/ cada instancia no t atual
            coefficients_i_start = [0, 0] * num_markets * j #p/ instancias anteriores
            coefficients_middle = [1, 0] * num_markets
            coefficients_i_end = [0, 0] * num_markets * (num_instances - j - 1) #p/ instancias posteriores
            
            coefficients = coefficients_t_start + coefficients_i_start + coefficients_middle + coefficients_i_end + coefficients_t_end
            
            #print(coefficients1)
             
            ret = lpsolve('add_constraint', lp, coefficients, '>=', demand[i][j]) #Tomar cuidado com forma de entrada de demanda

def constraint2(lp, t, num_instances, num_markets, duracao_reservas): #y muda p cada mercado!

    for i in range(t): # para cada t
        coefficients_t_end = [0, 0] * num_markets * num_instances * (t - i - 1) #p/ tempos posteriores
        
        for j in range(num_instances): #para cada instancia
            coefficients_i_end = [0, 0] * num_markets * (num_instances - j - 1) #p/ instancias posteriores

            for k in range(num_markets): #para cada mercado
                coefficients_start = []
                coefficients_middle = [0, 0] * k + [1, -1] + [0, 0] * (num_markets - k - 1)
                
                duracao_re = duracao_reservas[j] - 1
                
                for l in range(i-1, -1, -1): #para cada período de tempo anterior
                    if (duracao_re > 0):
                        coefficients_start = [0, 0] * k + [0, -1] + [0, 0] * (num_markets - k - 1) + coefficients_start
                        duracao_re -= 1
                    else:
                        coefficients_start = [0, 0] * num_markets * num_instances ff+ coefficients_start
                
                coefficients = coefficients_start + coefficients_middle + coefficients_i_end + coefficients_t_end
                ret = lpsolve('add_constraint', lp, coefficients, '=', 0)

def setInt(lp, n):
    for i in range(1, n + 1):
        ret= lpsolve('set_int', lp, i, True)