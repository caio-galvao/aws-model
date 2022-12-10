import csv
import pandas as pd
from new_aws_model import otimizaModelo

def outputInstances(raw_values, t, instance_names, market_names, input_data, writerCost):
    values = tranformarEmLista(raw_values, t, len(instance_names), len(market_names))

    for i_instancia in range(len(instance_names)):
        cost = 0

        output = open('total_purchases_' + instance_names[i_instancia] + '.csv', 'w')
        writer = csv.writer(output)
        writer.writerow(['instanceType', 'market', 'count_active', 'count_reserves'])
        
        for i_mercado in range(len(market_names)):
            im_values = input_data[i_instancia][i_mercado]
            cr_im = im_values[0] * im_values[2] + im_values[1]

            for i_tempo in range(t):
                activ = values[i_tempo][i_instancia][i_mercado][0]
                reserves = values[i_tempo][i_instancia][i_mercado][1]
                writer.writerow([instance_names[i_instancia], market_names[i_mercado], activ, reserves])

                cost += reserves * cr_im

        writerCost.writerow([instance_names[i_instancia], cost])        
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
writerCost.writerow(['instance','total_cost'])

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

t = len(total_demand[0])

result = otimizaModelo(t, total_demand, input_data)
cost = result[0]

writerCost.writerow(['all', cost])

outputInstances(result[1], t, instance_names, market_names, input_data, writerCost)

