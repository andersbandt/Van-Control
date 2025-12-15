# this file is for spitting out calibration constants to be using
# sensors must in the same area for at least the most recent 1000 or so samples?


import db.helpers as dbh
import statistics



#Mean of sensors temp 0 is 19.026165413533835
#Mean of sensors temp 1 is 20.49451127819549
#Mean of sensors temp 2 is 19.97824561403509


#Mean of sensors humidity 0 is 42.83491228070175
#Mean of sensors humidity 1 is 34.08593984962406
#Mean of sensors humidity 2 is 31.076315789473686


num_sensors = 3
limit = 50


temps = []
hums = []
for i in range (0, num_sensors):
    data = dbh.sensors.get_data(i, limit)
    s_temps = [row[1] for row in data]
    s_hum = [row[2] for row in data]
    mean_temp = statistics.mean(s_temps)
    mean_hum = statistics.mean(s_hum)
    print(f"Mean of sensors temp {i} is {mean_temp}")
    print(f"Mean of sensors humidity {i} is {mean_hum}")
    temps.append(mean_temp)
    hums.append(mean_hum)




print(f"temps: {temps}")
    
# print out final calibration constant
print("NOTE: calibrate sensor is first")
print(f"Sensor 0 to 2 temp is {temps[2] - temps[0]}")
print(f"Sensor 1 to 2 temp is {temps[2] - temps[1]}")

print(f"Sensor 0 to 2 humidity is {hums[2] - hums[0]}")
print(f"Sensor 1 to 2 humidity is {hums[2] - hums[1]}")









