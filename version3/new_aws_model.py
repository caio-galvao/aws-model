from lpsolve55 import *
lpsolve()

#Model for optimizing instance selection in aws ec2
#Considering two markets (on demand and reserve) during a t period of time

# values = [[p_hr, p_up, y], [p_hr, p_up, y], [p_hr, p_up, y]]

def otimizaModelo(t, demand, values):
    lp = lpsolve('make_lp', 0, 4 * t)
    lpsolve('set_verbose', lp, 'IMPORTANT')

    obj = []
    for values_m in values:  #for every market
        p_hr = values_m[0]
        p_up = values_m[1]
        y = values_m[2]

        cr_re = p_up + p_hr * y
        obj.append(0)
        obj.append(cr_re)

    #Objective function: C = a_od * 0 + r_od * cr_od + a_re * 0 + r_re * cr_re
    ret = lpsolve('set_obj_fn', lp, obj * t)

    #Adding constraints
    #Demand <= 1*a
    constraint1(lp, t, demand, len(values))
    # a_t = sum(r_t)
    constraint2(lp, t, values)
    
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

def constraint1(lp, t, demand, num_markets):
    for i in range(t):
        coefficients_start = [0, 0] * num_markets * i
        coefficients_middle = [1, 0] * num_markets
        coefficients_end = [0, 0] * num_markets * (t - i - 1)

        coefficients = coefficients_start + coefficients_middle + coefficients_end

        #print(coefficients1)
        
        ret = lpsolve('add_constraint', lp, coefficients, '>=', demand[i])

def constraint2(lp, t, values): #y muda p cada mercado!
    num_markets = len(values)

    for i in range(t): # para cada t
        coefficients_end = [0, 0] * num_markets * (t - i - 1)
        for j in range(len(values)): #para cada mercado
            coefficients_start = []
            coefficients_middle = [0, 0] * j + [1, -1] + [0, 0] * (len(values) - j - 1)
            
            duracao_re = values[j][2] - 1
            
            for k in range(i-1, -1, -1):
                if (duracao_re > 0):
                    coefficients_start = [0, 0] * j + [0, -1] + [0, 0] * (len(values) - j - 1) + coefficients_start
                    duracao_re -= 1
                else:
                    coefficients_start = [0, 0] * num_markets + coefficients_start
            
            coefficients = coefficients_start + coefficients_middle + coefficients_end
            ret = lpsolve('add_constraint', lp, coefficients, '=', 0)

def setInt(lp, n):
    for i in range(1, n + 1):
        ret= lpsolve('set_int', lp, i, True)