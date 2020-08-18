# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:30:28 2020

@author: Jules
"""
import time
import random
import math
from scipy.spatial import distance

def psi(r, alpha):
    return 1/(1+r**alpha)


def cucker_smale2d_fix(N, x_pop_init, y_pop_init, vx_pop_init, vy_pop_init, t_min, t_max, eps, force_intensity, com_rate, perturbation = None, perturbation_origin = None, perturbation_interval = None):
    tstart_sim = time.time()
    lst_t = [t_min] #int->list int
    lst_pos_x = x_pop_init #[[x1_init, ... x1_finish], [x2_init, ... x2_finish], ..., [xn_init, ... xn_finish]]
    lst_pos_y = y_pop_init
    lst_vx = vx_pop_init #idem
    lst_vy = vy_pop_init
    t = t_min
    #perturbation_garbage_data = []
    
    #rq : N peut être déduit de la longeur du tableau principal
    while t < t_max: #t pas nécessairement un entier selon epsilon
        for i in range(N): #entity i
            acceleration_x_iter = 0.0
            acceleration_y_iter = 0.0

            i_entity_x = lst_pos_x[i]
            i_entity_y = lst_pos_y[i]
            i_entity_vx = lst_vx[i]
            i_entity_vy = lst_vy[i]
            k = len(i_entity_x)

            i_entity_next_x = eps*i_entity_vx[k-1] + i_entity_x[k-1]
            i_entity_next_y = eps*i_entity_vy[k-1] + i_entity_y[k-1]


                #definir le rapport de cohesion et le tracer en fct de t
                #calculer le temps de rétablissement du flocking
            
            
            for j in range(N): #entity j
                if j != i:
                    j_entity_x = lst_pos_x[j]
                    j_entity_y = lst_pos_y[j]
                    j_entity_vx = lst_vx[j]
                    j_entity_vy = lst_vy[j]

                    k2 = len(j_entity_x)

                    acceleration_x_iter += psi(abs(i_entity_x[k-1] - j_entity_x[k2-1]), com_rate)*(j_entity_vx[k2-1]-i_entity_vx[k-1])
                    acceleration_y_iter += psi(abs(i_entity_y[k-1] - j_entity_y[k2-1]), com_rate)*(j_entity_vy[k2-1]-i_entity_vy[k-1])

            i_entity_next_vx = i_entity_vx[k-1] + (acceleration_x_iter*eps*force_intensity)/N
            i_entity_next_vy = i_entity_vy[k-1] + (acceleration_y_iter*eps*force_intensity)/N                        

            #à appliquer sur les vitesses
            if perturbation != None:
                perturbation_t_start = perturbation_interval[0]
                perturbation_t_stop = perturbation_interval[1]
                perturbation_origin_x = perturbation_origin[0]
                perturbation_origin_y = perturbation_origin[1]
                impact_radius = 1 #recuperer les poissons qui subissent les perturbations à t fixé sous le forme d'un tableau [t][i]
                if perturbation_t_start<=t<=perturbation_t_stop:
                   if perturbation == "loc":
                        dist_individu_perturbation = math.sqrt((perturbation_origin_x-i_entity_next_x)**2+(perturbation_origin_y-i_entity_next_y)**2)
                        print(dist_individu_perturbation)
                        if dist_individu_perturbation <= impact_radius:
                            print("fish labelled " + str(i) + " is seeing a predator")
                            i_entity_next_vx += random.gauss(0, 2)
                            i_entity_next_vy += random.gauss(0, 1)
                            #print(get_direction_angle(i_entity_next_vx, 1))
                            #perturbation_garbage_data.append([])
                            #perturbation_garbage_data.append()
                            


                   elif perturbation == "unif":
                        i_entity_next_vx += random.gauss(0, 2)
                        i_entity_next_vy += random.gauss(0, 2)
                        
                        
                        
            lst_pos_x[i].append(i_entity_next_x)
            lst_pos_y[i].append(i_entity_next_y)
            lst_vx[i].append(i_entity_next_vx)
            lst_vy[i].append(i_entity_next_vy)


        t += eps
        lst_t.append(t)
        step = math.floor((t/t_max)*100)
        if step % 10 == 0:
            print(str(step) + "%")


    print("Resolved in " + str(math.ceil((time.time() - tstart_sim)/60)) + " s")
    return (lst_t, lst_pos_x, lst_pos_y, lst_vx, lst_vy)


#noise_x : time (int)
def flocking_restoration_delay(solutions, t_max_simulation, noise_end, eps_flocking, eps):
    vx = solutions[3]
    vy = solutions[4]

    #difference entre les extremes en vitesses > eps, eps à déterminer par l'expérience
    t_start = noise_end
    t = t_start
    extrema_max_vx = list_retrieve_max_at_t(vx, t)
    extrema_min_vx = list_retrieve_min_at_t(vx, t)
    extrema_max_vy = list_retrieve_max_at_t(vy, t)
    extrema_min_vy = list_retrieve_min_at_t(vy, t)
    while (abs(extrema_max_vx - extrema_min_vx) > eps_flocking) and (abs(extrema_max_vy - extrema_min_vy) > eps_flocking) and t < t_max_simulation:
        extrema_max_vx = list_retrieve_max_at_t(vx, t)
        extrema_min_vx = list_retrieve_min_at_t(vx, t)
        extrema_max_vy = list_retrieve_max_at_t(vy, t)
        extrema_min_vy = list_retrieve_min_at_t(vy, t)
        t += 1
    

    return (t-t_start)


def flocking_extrema_eps(solutions, t, eps):
    vx = solutions[3]
    vy = solutions[4]

    #difference entre les extremes en vitesses > eps, eps à déterminer par l'expérience
    extrema_max_vx = list_retrieve_max_at_t(vx, t)
    extrema_min_vx = list_retrieve_min_at_t(vx, t)
    extrema_max_vy = list_retrieve_max_at_t(vy, t)
    extrema_min_vy = list_retrieve_min_at_t(vy, t)
    
    return (abs(extrema_max_vx - extrema_min_vx), (abs(extrema_max_vy - extrema_min_vy)))


def get_direction_angle(dx, r):
    return math.acos(dx/r)



def list_retrieve_max_at_t(lst, t):
    max_value = lst[0][t]
    iterations = len(lst)
    for j in range(iterations):
        if lst[j][t] > max_value:
            max_value = lst[j][t]
    return max_value


def list_retrieve_min_at_t(lst, t):
    min_value = lst[0][t]
    iterations = len(lst)
    for j in range(iterations):
        if lst[j][t] < min_value:
            min_value = lst[j][t]
    return min_value
