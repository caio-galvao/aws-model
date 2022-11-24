# aws-model version 2
Same model receiving more than one instance type at the same time. The changes are in *build-simulation.py*.
In this version, the input format changed to a csv file:
- Rows: one for each instance;
- Columns: *instance* - instance name, *p_od* - on demand price, *p_re* - reserve hourly price, *u* - reserve upfront price, *y* - reserve duration.