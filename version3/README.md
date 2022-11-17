# aws-model version 3
Same model considering more then one reserve market at the same time (based on version 2).
In this version the input changed again, but it is still a csv file:
- Rows: one for each market type of each instance;
- Columns: *instance* - instance name, *market_name*, *p_hr* - hourly price, *p_up* - upfront price, *y* - reserve duration.
The on demand market is considered as a reserve market with *p_up* = 0 and *y* = 1.