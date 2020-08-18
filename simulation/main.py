# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:28:14 2020

@author: Jules
"""

from cucker_smale import cucker_smale2d_fix, flocking_restoration_delay, flocking_extrema_eps
from figures import graphe_distance_max_fct_t, scatter_at_specific_time_2d, print_in_realtime, graphe_diff_max_vitesse_fct_t, rapport_cohesion
from io import * # analysis:ignore
from figures import * # analysis:ignore
from misc import * # analysis:ignore
from perturbation import * # analysis:ignore
import random
import matplotlib.pyplot as plt


N = 10
eps = 0.1
t_min = 0
t_max = 50
force_intensity = 1


def __init__():
    init_pos_x = []
    init_pos_y = []
    init_vx =  []
    init_vy =  []

    for _ in range(N):
        init_pos_x.append([2*random.random()-1])
        init_pos_y.append([2*random.random()-1])
        init_vx.append([random.random()])
        init_vy.append([random.random()])

    #eloignement moyen ?
    #rapport de cohesion pour les perturbations non uniformes
    solution = cucker_smale2d_fix(N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity, 1/2, perturbation = "unif", perturbation_interval=[3,4], perturbation_origin=[0, 0])
    print_in_realtime(4, t_max, solution[0], solution[1], solution[2],solution[3],solution[4],force_intensity, 1/2)
    #scatter_at_specific_time_2d(5, solution[1], solution[2], solution[3], solution[4], circle=True, print_arrow=False)
    #scatter_at_specific_time_2d(6, solution[1], solution[2], solution[3], solution[4], circle=True, print_arrow=False)
    print("Flocking minima eps : " + str(flocking_extrema_eps(solution, 4, 0.1)))
    print("Flocking minima eps : " + str(flocking_extrema_eps(solution, 6, 0.1)))
    graphe_distance_max_fct_t(solution)
    graphe_diff_max_vitesse_fct_t(solution, superposition=True)
    #restoration_delay ne renvoie pas un temps nul pour une perturbation inexistante, problématique ...
    print("Restoration delay : " + str(flocking_restoration_delay(solution, t_max, 7, 0.001, 0.1)) + "dt")
#    cohesion = []
#    timing = []
#    for t in range(t_max):
#        timing.append(t)
#        cohesion.append(rapport_cohesion(solution, t))
#        
#    print(cohesion)
    #plt.plot(timing, cohesion)
    
__init__()