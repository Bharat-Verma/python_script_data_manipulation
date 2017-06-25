#!/usr/bin/python

import pandas as pd
import csv
import cProfile

#Importing the dataset
def read_dataset():
    #read the data and sort it with sensor name and then with timestamp
    dataset = pd.read_csv('input.csv', header=None).sort_values([1,0])
    return dataset

#Function to perform calculation and gnerate the csv as output
def calculate_fields():
    dataset = read_dataset()
    max_time_gap = 0
    total_vol = -1
    max_temp = 0
    weighted_avg_temp = 0
    avg_temp = 0
    time_gap_list = []
    max_temp_list = []
    
    num_records = len(dataset.index) - 1
    
    for i in range(0,num_records):
        if dataset.iloc[i, 1] == dataset.iloc[i+1, 1]:
            #calculating max time gap
            time_gap_1 = dataset.iloc[i+1, 0] - dataset.iloc[i, 0]
            time_gap_list.append(time_gap_1)
            #calculating total volume
            total_vol += dataset.iloc[i, 2]
            #calculating max temp
            max_temp_list.append(dataset.iloc[i, 3])
            #calculating weighted average temperature
            avg_temp += (dataset.iloc[i, 2]*dataset.iloc[i, 3])        
        else:
            total_vol += dataset.iloc[i, 2]
            avg_temp += (dataset.iloc[i, 2]*dataset.iloc[i, 3])
            if len(time_gap_list) > 1:
                max_time_gap = max(time_gap_list)
            else:
                max_time_gap = 0
            
            max_temp = max(max_temp_list)
            weighted_avg_temp = int(avg_temp/total_vol)
            #write these values in the file
            with open('output.csv', 'a', encoding='utf8', newline='') as csvfile:
                outwriter = csv.writer(csvfile, delimiter=',')
                outwriter.writerow([dataset.iloc[i, 1],str(max_time_gap),
                                    str(total_vol),str(weighted_avg_temp),
                                    str(max_temp)]) 
            #then initialize the values for next sensor
            time_gap_list = []
            max_temp_list = []
            max_time_gap = 0
            total_vol = 0
            max_temp = 0
            weighted_avg_temp = 0
            avg_temp = 0
    return 0

if __name__ == '__main__':
    ret_val = cProfile.run('calculate_fields()')
    print (ret_val)