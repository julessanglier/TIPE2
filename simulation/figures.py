# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:37:11 2020

@author: Jules
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#let x = [x1, ..., xt], y = [y1, ..., yt], t=[t1, ..., t_max]
def scatter_at_specific_time_2d(t, x, y, vx, vy, color = "red", print_arrow = True, show = True, circle = True):
    x_stop = []
    y_stop = []
    vx_stop = []
    vy_stop = []
    N = len(x)
    center_of_mass_x = 0
    center_of_mass_y = 0
    center_of_mass_vx = 0
    center_of_mass_vy = 0

    for j in range(N):
        k=1
        #k=1/8
        x_stop.append(x[j][t])
        y_stop.append(y[j][t])
        vx_stop.append(vx[j][t])
        vy_stop.append(vy[j][t])

        center_of_mass_x += x_stop[j]
        center_of_mass_y += y_stop[j]
        center_of_mass_vx += vx_stop[j]
        center_of_mass_vy += vy_stop[j]
        
        plt.annotate(str(j), (x[j][t], y[j][t]))
        if print_arrow:
            if j == N-1:
                plt.arrow(x[j][t], y[j][t], vx[j][t]*k, vy[j][t]*k, head_width=0.1, length_includes_head=True, color='green')
            else:
                plt.arrow(x[j][t], y[j][t], vx[j][t]*k, vy[j][t]*k, head_width=0.1, length_includes_head=True, color='blue')

    center_of_mass_x *= 1/N
    center_of_mass_y *= 1/N
    center_of_mass_vx *= 1/N
    center_of_mass_vy *= 1/N
    #print(x_stop)
    plt.scatter(x_stop, y_stop, color=color)
    plt.scatter(center_of_mass_x, center_of_mass_y, color="green")
    plt.axis("equal")
    plt.arrow(center_of_mass_x, center_of_mass_y, center_of_mass_vx*3, center_of_mass_vy*3, head_width=0.1, length_includes_head=True, color="orange")

    if circle:
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.sqrt(0.3)
        x1 = r*np.cos(theta)
        x2 = r*np.sin(theta)
        plt.plot(x1, x2)


def print_in_realtime(t_min, t_max, tl, x, y, vx, vy, force_intensity, communication_rate, frame_rate_ms = 60, eps=0.1):
    t = 0
    test_l = len(tl)
    #print(test_l)
    while t < test_l:
        plt.clf()
        scatter_at_specific_time_2d(t, x, y, vx, vy, circle=True, print_arrow=True)
        plt.title("t=" + str(t)+" (ut), fps : " + str(1/(frame_rate_ms/1000)) + ", t=[" + str(t_min) + "," + str(t_max) + "], λ=" + str(force_intensity) + ", ε=" + str(eps) + ", α=" + str(communication_rate))
        plt.xlabel("x(t)")
        plt.ylabel("y(t)")
        plt.pause(frame_rate_ms/1000)
        t += 1
    
    plt.cla()
    plt.close()
        

def distance_max_entre_deux_individus(t, solution):
    x = solution[1]
    y = solution[2]

    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    i = 0
    j = 1
    mxtemp = max(x[i][t], x[j][t])
    mytemp = max(y[i][t], y[j][t])
    minxtemp = min(x[i][t], x[j][t])
    minytemp = min(y[i][t], y[j][t])

    if mxtemp > max_x:
        max_x = mxtemp

    if mytemp > max_y:
        max_y = mytemp

    if minxtemp > min_x:
        min_x = minxtemp

    if minytemp > min_y:
        min_y = minytemp

    return (abs(max_x - min_x), abs(max_y - min_y))


def deltav_max_couple(t, solution):
    vx = solution[2]
    vy = solution[3]

    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    i = 0
    j = 1
    mxtemp = max(vx[i][t], vx[j][t])
    mytemp = max(vy[i][t], vy[j][t])
    minxtemp = min(vx[i][t], vx[j][t])
    minytemp = min(vy[i][t], vy[j][t])

    if mxtemp > max_x:
        max_x = mxtemp

    if mytemp > max_y:
        max_y = mytemp

    if minxtemp > min_x:
        min_x = minxtemp

    if minytemp > min_y:
        min_y = minytemp

    return (abs(max_x - min_x), abs(max_y - min_y))


def graphe_distance_max_fct_t(solution):
    eps = 0.1
    t_max = 50
    i = int(t_max / eps)

    distarray = []
    t = []
    #print(t)
    for j in range(i):
        distarray.append(distance_max_entre_deux_individus(j, solution)[0])
        if j== 30:
            plt.vlines(j, 0, distance_max_entre_deux_individus(j, solution)[0], color="red", linestyle="dashed")
        elif j == 40:
            plt.vlines(j, 0, distance_max_entre_deux_individus(j, solution)[0], color="red", linestyle="dashed")

        t.append(j)

    plt.plot(t, distarray)
    plt.hlines(0, 30, 40, color="r", lw=2)
    plt.ylabel("distance max entre les individus i et j")
    plt.xlabel("dt")
    plt.title("Perturbation uniforme")
    plt.show()
    

#projection polaire pour la perturbation non uniforme
def graphe_diff_max_vitesse_fct_t(solution, show_multiple_figures = False, superposition = False):
    eps = 0.1
    t_max = 50
    i = int(t_max / eps)
    
    if show_multiple_figures and not superposition:
        plt.subplot(211)
        
    distarray = []
    t = []
    for j in range(i):
        distarray.append(deltav_max_couple(j, solution)[0])
        if j== 30:
            plt.vlines(30, 0, deltav_max_couple(j, solution)[0], color="orange" if superposition else "red", linestyle="dashed")
        elif j == 40:
            plt.vlines(40, 0, deltav_max_couple(j, solution)[0], color="orange" if superposition else "red", linestyle="dashed")

        t.append(j)
    
    if superposition:
        plt.plot(t, distarray, color="red")
    else:
        plt.plot(t, distarray)
        
    plt.hlines(0, 30, 40, color="orange" if superposition else "red", lw=2)
    plt.ylabel("différence maximum de vitesse entre les individus i et j")
    plt.xlabel("dt")
    plt.title("Perturbation uniforme")
    plt.show()
    
    
def rapport_cohesion(solution, t):
    x = solution[1]
    y = solution[2]
    n = len(x)
    
    moy = 0
    
    for j in range(n):
        poisson_j_x = x[j][t]
        poisson_j_y = y[j][t]
        
        poisson_plus_proche = 0 if j > 0 else 1
        poisson_plus_pproche = 0 if j > 0 else 2 #second poisson le + proche
        dist_poisson_plus_proche = math.sqrt((poisson_j_x-x[poisson_plus_proche][t])**2+(poisson_j_y-y[poisson_plus_proche][t])**2)
        dist_poisson_pproche = math.sqrt((poisson_j_x-x[poisson_plus_pproche][t])**2+(poisson_j_y-y[poisson_plus_pproche][t])**2)
        for i in range(n):
            if i != j:
                poisson_temp_x = x[i][t]
                poisson_temp_y = y[i][t]
                dist_poisson_temp = math.sqrt((poisson_j_x-poisson_temp_x)**2+(poisson_j_y-poisson_temp_y)**2)
                if dist_poisson_temp < dist_poisson_plus_proche:
                    dist_poisson_plus_proche = dist_poisson_temp
                    poisson_plus_proche = i
                    
                if dist_poisson_temp > dist_poisson_plus_proche and dist_poisson_temp > dist_poisson_pproche:
                    dist_poisson_pproche = dist_poisson_temp
                    poisson_plus_pproche = i
        
        rapport_moy = (dist_poisson_plus_proche + dist_poisson_pproche)/2
        moy += rapport_moy
    
    
    return moy/n
