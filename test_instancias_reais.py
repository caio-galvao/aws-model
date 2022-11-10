import csv
import pandas as pd
from new_aws_model import otimizaModelo

def preProcessamento(instance):
    totalDemand = pd.read_csv('TOTAL_demand.csv')
    return totalDemand[instance].values.tolist()

def output(instance, cost, values):
    output = open('resultCost.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(['instancia', 'total_cost'])
    writer.writerow([instance, cost])
    
    values.insert(0, instance)

    output = open('resultValues.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(values)
    createTotalPurchases(instance, values)

def createTotalPurchases(instance, values):
    values.pop(0)
    valuesDivided = list(dividirLista(values, 4))

    output = open('total_purchases.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(['instanceType', 'market', 'count_active', 'count_reserves'])
    
    # ValueSet = [a_od, r_od, a_re, r_re] for each 

    for valueSet in valuesDivided:
        writer.writerow([instance, 'OnDemand', int(valueSet[0]), int(valueSet[1])])
    
    for valueSet in valuesDivided:
        writer.writerow([instance, 'Reserved', int(valueSet[2]), int(valueSet[3])])

def dividirLista(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]

#Teste com instancias reais
instance = 'c4.2xlarge' #change the instance here

demand = preProcessamento(instance)

t = len(demand)

#Preco de 13/10/2022
p_od = 0.398 #on demand value

#Partial upfront 1 year
p_re = 0.242 #effective hourly rate
u = 0 #upfront price
y = 8760 #reserve duration (1 year)

result = otimizaModelo(t, demand, p_od, p_re, u, y)
cost = result[0]
values = result[1]
output(instance, cost, values)

info = open('info.txt', 'w')
info.writelines(["Instance: " + instance, "\nOn demand price: " + str(p_od), "\nReserve hourly price: " + str(p_re),
                "\nReserve upfront price: " + str(u), "\nReserve duration: " + str(y), "\nTotal cost: " + str(cost)]) 
info.close()
