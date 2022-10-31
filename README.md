# aws-model
Model for optimizing instance market selection in AWS EC2.

## Files
- new_aws_model.py: the model
- test_new_aws_model.py: simple tests
- test_instancias_reais.py: tests using real data
- TOTAL_demand.csv: real demand data, input for test_instancias_reais.py
- collect-cpu-usage.sh; collect-memory-usage.sh: used for testing the peformance of the model

## How to run
First, you need to have installed Python3, Pandas and [LpSolve](http://web.mit.edu/lpsolve/doc/). For installing LPSolve, it is possible to use anaconda.
