'''
Overview:
Parses as run files in a directory and adds break durations together
as Timecode objects. Returns durations with date, time and duration in CSV.

e.g. 9/26/2022,04:19:18:15,00:01:00;02

Define an ID range for commercial spots,
search directory, output filename and ignore patterns.

'''

import os
from timecode import Timecode
import re
from datetime import datetime
import csv

# Range of numbers from 20000 to 79999
id_range = range(20000, 79999)
ignore_patterns = ['LIST1', 'LIST12']
dir = 'C:\\Temp\\'
os.chdir(dir)

# Iterate over cwd and find all asrun files
# Return asrun files as list
def find_asrun_files(cwd):
    asrun_files = []
    for file in os.listdir(cwd):
        if re.match('02[0-9]{6}_kiro.txt', file):
            print(file)
            asrun_files.append(os.path.basename(file))
    return asrun_files

# Function to convert date in string to formatted date M/DD/YYYY
def convert_date(date):
    date = datetime.strptime(date, '%m%d%y')
    return date.strftime('%m/%d/%Y')

# Returns as run file lines as list of strings
def asrun_to_list(asrun_file):
    with open(asrun_file, 'r') as f:
        asrun_list = f.readlines()
    return asrun_list

# Main function to extract break durations from as run files
def find_asrun_data(asrun_files):
    durations = []

    for asrun_file in asrun_files:
        asrun_list = asrun_to_list(asrun_file)

        for index, line in enumerate(asrun_list):
            # If any house ID in id_range list is found in a line of the asrun file
            if any(f' {str(x)} ' in line for x in id_range):
                break_start = line[10:21].replace('.', ':')
                spot_duration = line[92:103].replace('.', ':')
                # If duration is not 00:00:00;00
                # or any secondary events
                # or in ignore_patterns list, add to dictionary
                if spot_duration != '00:00:00;00' and not \
                    any(f' {str(x)} ' in asrun_list[index-1] for x in id_range) and not \
                    any(x in asrun_list[index-1] for x in ignore_patterns):
                    start_of_break = break_start
                    print(f'Start of break: {start_of_break}')
                    start_date = line[2:9]
                    durations.append(spot_duration)
                
                else:
                    durations.append(spot_duration)

            elif any(x in line for x in ignore_patterns):
                pass

            else:
                try:
                    if durations:
                        # Initialize break_duration to 00:00:00:00
                        break_duration = Timecode('29.97', '00:00:00:00')
                        for duration in durations:
                            # Convert each duration string in durations list
                            # to Timecode object for addition
                            z = Timecode('29.97', duration)
                            break_duration+=z
                        print(f'Break duration: {break_duration}')
                        with open('asrun_data.csv', 'a', newline='') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow([start_date, start_of_break, break_duration])
                        # Reset durations list for next break
                        durations = []
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    find_asrun_data(find_asrun_files(dir))