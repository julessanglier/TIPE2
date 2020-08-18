# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:43:08 2020

@author: Jules
"""
import random
import math


def random_constant_distribution(n):
    distribution_x = []
    distribution_y = []
    cx = random.random()
    cy = random.random()
    
    for i in range(n):
        distribution_x.append([cx])
        distribution_y.append([cy])
    
    return (distribution_x,distribution_y)
        

def random_circular_distribution(radius, x, y, n):
    circle_r = radius
    circle_x = x
    circle_y = y
    distribution_x = []
    distribution_y = []
    
    for i in range(n):
        alpha = 2 * math.pi * random.random()
        r = circle_r * random.random()
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        distribution_x.append([x])
        distribution_y.append([y])
    
    return (distribution_x,distribution_y)


def gen_distrib_non_homogene():
    t_min = 0
    t_max = 100
    eps = 0.1
    
    g1_init_pos_x = []
    g1_init_pos_y = []
    g1_init_vx =  []
    g1_init_vy =  []    
    g1_N = 30
    
    g2_init_pos_x = []
    g2_init_pos_y = []
    g2_init_vx =  []
    g2_init_vy =  []    
    g2_N = 10
    force_intensity = 1
    
    if g1_N == g2_N:
        for i in range(g1_N):
            g1_init_vx.append([10*random.random()-5])
            g1_init_vy.append([10*random.random()-5])
            g2_init_vx.append([10*random.random()-5])
            g2_init_vy.append([10*random.random()-5])
    else:
         for i in range(g1_N):
            g1_init_vx.append([10*random.random()-5])
            g1_init_vy.append([10*random.random()-5])
         for i in range(g2_N):
            g2_init_vx.append([10*random.random()-5])
            g2_init_vy.append([10*random.random()-5])
    
    g1_circular_distrib = random_circular_distribution(2, 0, 0, g1_N)
    g2_circular_distrib = random_circular_distribution(2, -20, 10, g2_N)
    
    g1_init_pos_x = g1_circular_distrib[0]
    g1_init_pos_y = g1_circular_distrib[1]
    g2_init_pos_x = g2_circular_distrib[0]
    g2_init_pos_y = g2_circular_distrib[1]
    
    init_pos_x = g1_init_pos_x + g2_init_pos_x
    init_pos_y = g1_init_pos_y + g2_init_pos_y
    init_vx =  g1_init_vx +  g2_init_vx
    init_vy =  g1_init_vy +  g2_init_vy
     
    #solution = cucker_smale2d_fix(g1_N + g2_N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity, 1/2)
    positions_x = solution[1]
    positions_y = solution[2]
    vitesses_x = solution[3]
    vitesses_y = solution[4]
    #print_in_realtime(t_min, t_max, positions_x, positions_y, vitesses_x, vitesses_y, force_intensity, 1/2)