import pyvisa
import time
import csv
import os
import pandas as pd

rm = pyvisa.ResourceManager()

# Get the current time to the second
current_time = time.strftime("%m-%d-%Y_%H-%M-%S")

# Create the filename with the current time
filename = f"C:/Users/hazellji/Documents/Code/OUTPUT/Temp_vs_Volts_{current_time}.csv"

f = open(filename, "w", newline='')

# Sets up variables to directly talk with each meter
temperature_reading = rm.open_resource('USB0::1510::8464::8016446::0::INSTR')
lockin_reading = rm.open_resource('USB0::1510::8464::8017832::0::INSTR')

# Configure each meter into desired settings, changeable
temperature_reading.write(':CONFigure:VOLTage[:DC] 10,0.00001')
lockin_reading.write(':CONFigure:VOLTage[:DC] 10,0.001')

# Write header to the CSV file
header = ['Timestamp', 'Query_Number', 'Temperature (C)', 'Voltage (V)']
csv_writer = csv.writer(f)
csv_writer.writerow(header)

# Loop is what measures the system. On one pass, it outputs the reading from
# both meters, stores it into a file then it sleeps for a time then executes
# again
query_number = 0
while True:
    timestamp = time.strftime("%H:%M:%S", time.gmtime())
    temp_C = float(temperature_reading.query(':MEASure:VOLTage:DC?').rstrip())
    volts = float(lockin_reading.query(':MEASure:VOLTage:DC?').rstrip())

    # Write data to the CSV file
    csv_writer.writerow([timestamp, query_number, temp_C, volts])
    f.flush()  # Flush the buffer to ensure data is written immediately

    # View the live data in the console without clearing
    print(f"Timestamp: {timestamp}, Query Number: {query_number}, Temperature (C): {temp_C}, Voltage (V): {volts}")

    query_number += 1
    time.sleep(1)

f.close()

# After the loop, create the Excel file from the CSV file
df = pd.read_csv(filename)
output_excel_file = filename.replace('.csv', '.xlsx')
df.to_excel(output_excel_file, index=False)
