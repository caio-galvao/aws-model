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

raw_input = pd.read_csv('input.csv')
instances = raw_input['instance'].value_counts()

raw_demand = pd.read_csv('TOTAL_demand.csv')

resultCost = open('resultCost.csv', 'w')
writerCost = csv.writer(resultCost)
writerCost.writerow(['total_cost'])

input_data = []
total_demand = []

for instance in instances.index:
    instance_input = []
    #market_names = []

    for i in range(len(raw_input)):
        line = raw_input.iloc[i]
        if line['instance'] == instance:
            instance_input.append([line['p_hr'],line['p_up'], line['y']])
            #market_names.append(line['market_name'])
    input_data.append(instance_input)

    instance_demand = raw_demand[instance].values.tolist()
    total_demand.append(instance_demand)

    #createTotalPurchases(instance, values, market_names) ver dps como criar o total purchases

t = len(total_demand[0])

result = otimizaModelo(t, total_demand, input_data)
cost = result[0]
values = result[1]

writerCost.writerow([cost])