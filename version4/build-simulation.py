import csv
import pandas as pd
from new_aws_model import otimizaModelo

def createTotalPurchases(instance, values, market_names):
    valuesDivided = list(dividirLista(values, 2 * len(market_names)))

    output = open('total_purchases_' + instance + '.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(['instanceType', 'market', 'count_active', 'count_reserves'])
    
    # ValueSet = [a_od, r_od, a_re, r_re] for each 

    for i in range(len(market_names)):
        market = market_names[i]
        for valueSet in valuesDivided:
            writer.writerow([instance, market, int(valueSet[2*i]), int(valueSet[2*i + 1])])

def dividirLista(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]

input_data = pd.read_csv('input.csv')
instances = input_data['instance'].value_counts()

totalDemand = pd.read_csv('TOTAL_demand.csv')

resultCost = open('resultCost.csv', 'w')
writerCost = csv.writer(resultCost)
writerCost.writerow(['instance', 'total_cost'])

for instance in instances.index:
    instance_input = []
    market_names = []

    for i in range(len(input_data)):
        line = input_data.iloc[i]
        if line['instance'] == instance:
            instance_input.append([line['p_hr'],line['p_up'], line['y']])
            market_names.append(line['market_name'])

    demand = totalDemand[instance].values.tolist()
    t = len(demand)

    result = otimizaModelo(t, demand, instance_input)
    cost = result[0]
    values = result[1]

    writerCost.writerow([instance, cost])
    createTotalPurchases(instance, values, market_names)