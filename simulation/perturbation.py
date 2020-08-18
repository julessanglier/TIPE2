# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:48:16 2020

@author: Jules
"""
import random


class UniformPerturbation:
    def __init__(self, start, end, value_x, value_y, ptype):
        self.start = start
        self.end = end
        self.value_x = value_x
        self.value_y = value_y
        self.ptype = ptype



def perturbation_uniforme(liste, sigma):
    n = len(liste)
    for i in range(n):
        liste[i] += random.gauss(0, sigma)

    return liste

#les calculs doivent être faits avant la génération des solutions ... donc imbriqués dans le sys de CS
def perturbation_progressive(cs_solution, N, i, t_start, t_end, x_start, y_start, impact_radius):
    traj_x = cs_solution[1]
    traj_y = cs_solution[2]

    x_radius = x_start + impact_radius
    y_radius = y_start + impact_radius

    for j in range(N):
        for t in range(i):
            for x in traj_x: #x est une liste, x[i] aussi, x[i][t] est une coord
                for y in traj_y:
                    #check if in radius, if in then perturb with 1/cos(x)
                    if t_start<=t<=t_end and x_start<=x<=x_radius and y_start<=y<=y_radius:
                        dist_individu_perturbation = math.sqrt((x_start-x)**2+(y_start-y)**2)
                        print(dist_individu_perturbation)
                        x[j][t] += 1/math.cos(dist_individu_perturbation)
                        y[j][t] += 1/math.sin(dist_individu_perturbation)


