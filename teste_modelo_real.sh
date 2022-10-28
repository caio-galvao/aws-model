bash collect-cpu-usage.sh > cpu_output.csv &
bash collect-memory-usage.sh > memory_output.csv &
python3 test_instancias_reais.py
ps -ef | grep collect-cpu-usage.sh | awk '{ print $2 }' | xargs kill -9
ps -ef | grep collect-memory-usage.sh | awk '{ print $2 }' | xargs kill -9
