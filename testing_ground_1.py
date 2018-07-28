import serial
import math
import pandas as pd

####################
# DEFINE VARIABLES #
###################

ser = serial.Serial('/dev/cu.usbmodem1411')
ser.flushInput()
tempF = []
humF = []
wallTempF = []
dp_array = []
emc_array = []
temp_size = len(tempF) - 1
hum_size = len(humF) - 1
emc_size = len(emc_array)
constant = 0.000045

dict = {"Data Type": ["Temperature", "Humidity", "Wall Temperature", "Dew Point", "EMC"],
            "Value": [tempF, humF, wallTempF, dp_array, emc_array]}



#########################
# TRANSLATE SERIAL DATA #
########################

while True:  # While loop that loops forever
    while (ser.inWaiting()==0): #Wait here until there is data
        pass #do nothing

    ser_bytes_1 = ser.readline()    #reading serial data
    decoded_bytes_temp = float(ser_bytes_1[0:len(ser_bytes_1) - 2].decode("utf-8")) #decoding bytes
    tempF.append(decoded_bytes_temp)    #putting decoded bytes into tempF array

    ser_bytes_2 = ser.readline()
    decoded_bytes_hum = float(ser_bytes_2[0:len(ser_bytes_2) - 2].decode("utf-8"))
    humF.append(decoded_bytes_hum)

    ser_bytes_3 = ser.readline()
    decoded_bytes_wallTemp = float(ser_bytes_3[0:len(ser_bytes_3) - 2].decode("utf-8"))
    wallTempF.append(decoded_bytes_wallTemp)

    dp_c_float = tempF[temp_size] - (20 - humF[hum_size] / 5)  # Calculating dew point
    dp_c = round(dp_c_float, 2)
    dp_array.append(dp_c)

    decimal_rh = humF[hum_size] / 100   # Calculate estimated moisture content
    emc_float = ((-math.log((1 - decimal_rh))) / (constant * (tempF[temp_size] + 460))) ** 0.638
    emc = round(emc_float, 2)
    emc_array.append(emc)

    brics = pd.DataFrame(dict)
    print(brics)

    brics.to_csv('live_data.csv')

    isotherm_60 = (3171.9) * math.exp((-0.3118) * (emc_array[emc_size]))
    isotherm_65 = (8444.7) * math.exp((-0.368) * (emc_array[emc_size]))
    isotherm_70 = (214095) * math.exp((-0.572) * (emc_array[emc_size]))
    isotherm_75 = (106860) * math.exp((-0.525) * (emc_array[emc_size]))
    isotherm_80 = (187333) * math.exp((-0.571) * (emc_array[emc_size]))
    isotherm_85 = (162897) * math.exp((-0.568) * (emc_array[emc_size]))



    if (16.0 < wallTempF[temp_size] <= 18):
        print("Days till mold is", isotherm_60)

    else:
        continue

    if (18 < wallTempF[temp_size] <= 21):
            print("Days till mold is", isotherm_65)

    else:
        continue

    if (21 < wallTempF[temp_size] <= 24):
            print("Days till mold is", isotherm_70)

    else:
        continue

    if (24 < wallTempF[temp_size] <= 27):
            print("Days till mold is", isotherm_75)

    else:
        continue

    if (27 <= wallTempF[temp_size] <= 29):
            print("Days till mold is", isotherm_80)

    else:
        continue

    if (wallTempF[temp_size] > 29):
            print("Days till mold is: ", isotherm_85)

    else:
        continue

    #def function_fitter(argument):
    #    selector = {
    #        1: isotherm_60,
    #        2: isotherm_65,
    #        3: isotherm_70,
    #        4: isotherm_75,
    #        5: isotherm_80,
    #        6: isotherm_85
    #    }



    #    print(selector.get(argument, "Low Risk"))
