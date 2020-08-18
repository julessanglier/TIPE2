# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:37:05 2020

@author: Jules
"""
import csv
import time
import main

def export_initial_conditions(N, x, y, vx, vy, t_min, t_max, eps, force_intensity):
    xcleaned = []
    ycleaned = []
    vxcleaned = []
    vycleaned = []
    n = len(x)
    for i in range(n):
        xcleaned.append(x[i][0])
        ycleaned.append(y[i][0])
        vxcleaned.append(vx[i][0])
        vycleaned.append(vy[i][0])
        
    a = [[N,t_min, t_max, eps,force_intensity, xcleaned, ycleaned, vxcleaned, vycleaned]]        
    with open(str(time.time()) + "_initial_conditions.csv","w+") as my_csv:            # writing the file as my_csv
        csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
        csvWriter.writerows(a)
    

def export_modified_data(force_intensity, communication_rate):
    a = [[main.eps],[force_intensity], [communication_rate]]
    with open(str(time.time()) + "_modified_data.csv","w+") as my_csv:            # writing the file as my_csv
        csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
        csvWriter.writerows(a)