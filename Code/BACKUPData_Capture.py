import pyvisa
import time

rm = pyvisa.ResourceManager()
f = open("Temp_vs_Volts.csv", "w")

# Sets up variables to directly talk with each meter
temprature_reading = rm.open_resource('USB0::1510::8464::8016446::0::INSTR')
Lockin_reading = rm.open_resource('USB0::1510::8464::8017832::0::INSTR')

# Configure each meter into desired settings, changeable
temprature_reading.write(':CONFigure:VOLTage[:DC] 10,0.00001')
Lockin_reading.write(':CONFigure:VOLTage[:DC] 10,0.001')

# Loop is what measures the system. On one pass, it outputs the reading from
# both meters, stores it into a file then it sleeps for a time then executes
# again
#f.write(f'Timestamp, Query_Number, DC, AC')
query_number = 0
while True:

    timestamp = time.strftime("%H:%M:%S", time.gmtime())
    temp = (temprature_reading.query(':MEASure:VOLTage:DC?')).rstrip()
    volts = (Lockin_reading.query(':MEASure:VOLTage:DC?')).rstrip()

    f.write(f'{timestamp}, {query_number}, {temp}, {volts}\n')

    query_number = query_number + 1

    time.sleep(1)

f.close()