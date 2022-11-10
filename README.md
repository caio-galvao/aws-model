# aws-model
In AWS EC2, there are several market options for buying cloud instances, each one with different pricing. The objetive of this model is to, given the instance demand for a determined period of time, find the optimal configuration of market selection. In other words, how many instances should be bought for each market in order to minimize the cost.

For running a simulation, you should run the file *test_instancias_reais.py*, changing the name of the instance and the market values. The demand values come from the file *TOTAL_demand.csv* and it can be changed (but it needs to be a csv file in the same format). The simulation output is composed of the following files:
  - *info.txt*, with the input data used in the simulation;
  - *resultCost.csv*, with the total cost;
  - *resultValues.csv*, with the values of active instances and new instances reserved for each time frame.
  - *total_purchases.csv*, with the same values of *resultValues.csv* in a more organized form.

Currently, the model is only simulating one instance at the time and for the on demand and one reserve market.

## Files
- new_aws_model.py: the model
- test_new_aws_model.py: simple tests
- test_instancias_reais.py: tests using real data
- TOTAL_demand.csv: real demand data, input for test_instancias_reais.py
- collect-cpu-usage.sh; collect-memory-usage.sh: used for testing the peformance of the model

## How to run
First, you need to have installed Python3, Pandas and [LpSolve](http://web.mit.edu/lpsolve/doc/). For installing LPSolve, you can use anaconda.

## Implementation
The problem is modeled as a Linear Programming problem and solved using LpSolve in Python. Pandas is used for processing input data.

## Future improvements
- Simulate more then one instance type at the same time;
- Consider more then one reserve market;
- Consider saving plans.

## Credits
This work is a part of an undergraduate reseach project by Computer Science student Caio Ribeiro Galvão, in UFCG, Brazil. 
