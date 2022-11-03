import csv
import pandas as pd
from new_aws_model import otimizaModelo

def preProcessamento(instancia):
    totalDemand = pd.read_csv('TOTAL_demand.csv')
    return totalDemand[instancia].values.tolist()

def output(instancia, cost, values):
    output = open('resultCost.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(['instancia', 'total_cost'])
    writer.writerow([instancia, cost])
    
    output = open('resultValues.csv', 'w')
    writer = csv.writer(output)
    writer.writerow(values)
    writer.writerow([instancia, cost])

#Teste com instancias reais
instancia = 'c4.2xlarge' #change the instance here

demand = preProcessamento(instancia)

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
output(instancia, cost, values)