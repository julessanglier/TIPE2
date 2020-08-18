# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:45:00 2020

@author: Jules
"""

def average_velocity_dim2(v_x, v_y, particle_count, eps, delta_t):
    sum_x = 0
    sum_y = 0
    len_v_x = len(v_x)
    for i in range(len_v_x):
        sum_x += v_x[i]
        sum_y += v_y[i]
        
        sum_x *= eps/((delta_t)*particle_count)
        sum_y *= eps/((delta_t)*particle_count)
    
    return (sum_x, sum_y)

def center_of_mass_coordinates(t, x, y):
    center_of_mass_x = 0
    center_of_mass_y = 0
    n = len(x)
    for i in range(n):
         center_of_mass_x += x[i][t]
         center_of_mass_y += y[i][t]
    
    center_of_mass_x *= 1/n
    center_of_mass_y *= 1/n
    return (center_of_mass_x, center_of_mass_y)


def center_of_mass_speeds(t, vx, vy):
    center_of_mass_vx = 0
    center_of_mass_vy = 0
    n = len(vx)
    for i in range(n):
         center_of_mass_vx += vx[i][t]
         center_of_mass_vy += vy[i][t]
         
    center_of_mass_vx *= 1/n
    center_of_mass_vy *= 1/n
    return (center_of_mass_vx, center_of_mass_vy)