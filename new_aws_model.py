from lpsolve55 import *
lpsolve()

#Model for optimizing instance selection in aws ec2
#Considering two markets (on demand and reserve) during a t period of time

def otimizaModelo(t, demand, p_od, p_re, u, y):

    lp = lpsolve('make_lp', 0, 4 * t)
    lpsolve('set_verbose', lp, 'IMPORTANT')

    cr_od = 0 + p_od * 1   #u_od = 0, y_od = 1
    cr_re = u + p_re * y

    #Objective function: C = a_od * 0 + r_od * cr_od + a_re * 0 + r_re * cr_re
    ret = lpsolve('set_obj_fn', lp, [0, cr_od, 0, cr_re] * t)

    #Adding constraints
    #Demand <= 1*a
    constraint1(lp, t, demand)
    # a_t = sum(r_t)
    constraint2(lp, t, y)
    
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

def constraint1(lp, t, demand):
    for i in range(t):
        coefficients0 = [1, 0, 1, 0]
        coefficients_start = [0, 0, 0, 0] * i
        coefficients_end = [0, 0, 0, 0] * (t - i - 1)

        coefficients = coefficients_start + coefficients0 + coefficients_end

        #print(coefficients1)
        
        ret = lpsolve('add_constraint', lp, coefficients, '>=', demand[i])

def constraint2(lp, t, y):
    for i in range(t):
        #coefficientes on-demand
        coefficients_start = [0, 0, 0, 0] * i
        coefficients0 = [1, -1, 0, 0]
        coefficients_end = [0, 0, 0, 0] * (t - i - 1)

        coefficients = coefficients_start + coefficients0 + coefficients_end

        ret = lpsolve('add_constraint', lp, coefficients, '=', 0)
        
        #coefficientes reserved
        coefficients_start = []
        coefficients = [0, 0, 1, -1]
        coefficients_end = [0, 0, 0, 0] * (t - i - 1)

        duracao_re = y - 1

        for j in range(i-1, -1, -1):
            if (duracao_re > 0):
                coefficients_start = [0, 0, 0, -1] + coefficients_start
                duracao_re -= 1
            else:
                coefficients_start = [0, 0, 0, 0] + coefficients_start

        
        coefficients2 = coefficients_start + coefficients + coefficients_end

        ret = lpsolve('add_constraint', lp, coefficients2, '=', 0)

def setInt(lp, n):
    for i in range(1, n + 1):
        ret= lpsolve('set_int', lp, i, True)