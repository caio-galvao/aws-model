import csv
import pandas as pd
from new_aws_model import otimizaModelo

def createTotalPurchases(raw_values, t, instance_names, market_names):
    values = tranformarEmLista(raw_values, t, len(instance_names), len(market_names))

    for i_instancia in range(len(instance_names)):
        output = open('total_purchases_' + instance_names[i_instancia] + '.csv', 'w')
        writer = csv.writer(output)
        writer.writerow(['instanceType', 'market', 'count_active', 'count_reserves'])
        
        for i_mercado in range(len(market_names)):
            for i_tempo in range(t):
                activ = values[i_tempo][i_instancia][i_mercado][0]
                reserves = values[i_tempo][i_instancia][i_mercado][1]
                writer.writerow([instance_names[i_instancia], market_names[i_mercado], activ, reserves])
        
        output.close()

def tranformarEmLista(values, t, num_instances, num_markets):
    index = 0
    lista = []
    for i_tempo in range(t):
        lista_tempo = []
        for i_instancia in range(num_instances):
            lista_instancia = []
            for i_mercado in range(num_markets):
                lista_instancia.append([values[index], values[index+1]])
                index += 2
            lista_tempo.append(lista_instancia)
        lista.append(lista_tempo)
    return lista

raw_input = pd.read_csv('input.csv')
instances = raw_input['instance'].value_counts()

raw_demand = pd.read_csv('TOTAL_demand.csv')

resultCost = open('resultCost.csv', 'w')
writerCost = csv.writer(resultCost)
writerCost.writerow(['total_cost'])

input_data = []
total_demand = []
instance_names = []

for instance in instances.index:
    market_names = []
    instance_input = []
    instance_names.append(instance)

    for i in range(len(raw_input)):
        line = raw_input.iloc[i]
        if line['instance'] == instance:
            instance_input.append([line['p_hr'],line['p_up'], line['y']])
            market_names.append(line['market_name'])
    input_data.append(instance_input)

    instance_demand = raw_demand[instance].values.tolist()
    total_demand.append(instance_demand)

    #createTotalPurchases(instance, values, market_names) ver dps como criar o total purchases

t = len(total_demand[0])

result = otimizaModelo(t, total_demand, input_data)
cost = result[0]
createTotalPurchases(result[1], t, instance_names, market_names)

writerCost.writerow([cost])