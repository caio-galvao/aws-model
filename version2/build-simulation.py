import csv
import pandas as pd
from new_aws_model import otimizaModelo

def createTotalPurchases(instance, values):
    valuesDivided = list(dividirLista(values, 4))

    output = open('total_purchases_' + instance + '.csv', 'w')
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

input_data = pd.read_csv('input.csv')
totalDemand = pd.read_csv('TOTAL_demand.csv')

resultCost = open('resultCost.csv', 'w')
writerCost = csv.writer(resultCost)
writerCost.writerow(['instance', 'total_cost'])

for i in range(len(input_data)):
    data = input_data.iloc[i]
    instance = data['instance']

    demand = totalDemand[instance].values.tolist()
    t = len(demand)
    p_od = data['p_od']
    p_re = data['p_re']
    u = data['u']
    y = data['y']
    
    result = otimizaModelo(t, demand, p_od, p_re, u, y)
    cost = result[0]
    values = result[1]

    writerCost.writerow([instance, cost])
    createTotalPurchases(instance, values)