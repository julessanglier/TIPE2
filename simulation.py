import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math
import csv

y_max = 10
y_min = -10

x_max = 10
x_min = -10

def psi(r, alpha):
    return 1/(1+r**alpha)

def psi_motsch_tadmor(r, alpha, N):
    return False

    
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
        


def cucker_smale1d_fix(N, x_pop_init, vx_pop_init, t_min, t_max, eps, force_intensity, com_rate):
    tstart_sim = time.time()
    lst_t = [t_min] #int->list int
    lst_pos = x_pop_init #[[x1_init, ... x1_finish], [x2_init, ... x2_finish], ..., [xn_init, ... xn_finish]]
    lst_v = vx_pop_init #idem
    t = t_min
    #rq : N peut être déduit de la longeur du tableau principal
    while t < t_max: #t pas nécessairement un entier selon epsilon
        for i in range(N): #entity i            
            acceleration_x_iter = 0.0
            
            i_entity_x = lst_pos[i]
            i_entity_vx = lst_v[i]
            k = len(i_entity_x)
            print(i_entity_x)
            
            i_entity_next_x = eps*i_entity_vx[k-1] + i_entity_x[k-1] 
            for j in range(N): #entity j
                if j != i:
                    j_entity_x = lst_pos[j]
                    j_entity_vx = lst_v[j]
                    
                    k2 = len(j_entity_x)
                    
                    acceleration_x_iter += psi(abs(i_entity_x[k-1] - j_entity_x[k2-1]), com_rate)*(j_entity_vx[k2-1]-i_entity_vx[k-1])
                    
            
            
            i_entity_next_vx = i_entity_vx[k-1] + (acceleration_x_iter*eps*force_intensity)/N
            lst_pos[i].append(i_entity_next_x)
            lst_v[i].append(i_entity_next_vx)
        
        print(t)
        t += eps
        lst_t.append(t)
    
   
    print("Resolved in " + str((time.time() - tstart_sim)/60) + " s")
    return (lst_t, lst_pos, lst_v)


def cucker_smale2d_fix(N, x_pop_init, y_pop_init, vx_pop_init, vy_pop_init, t_min, t_max, eps, force_intensity, com_rate, flock_step_eps=1e-4):
    tstart_sim = time.time()
    lst_t = [t_min] #int->list int
    lst_pos_x = x_pop_init #[[x1_init, ... x1_finish], [x2_init, ... x2_finish], ..., [xn_init, ... xn_finish]]
    lst_pos_y = y_pop_init
    lst_vx = vx_pop_init #idem
    lst_vy = vy_pop_init
    t = t_min
    flock_step = 0
    max_vx = 0
    max_vy = 0
    min_vx = 0
    min_vy = 0
     
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
            
            if max_vx < i_entity_next_vx:
                max_vx = i_entity_next_vx
            if max_vy < i_entity_next_vy:
                max_vy = i_entity_next_vy
            if min_vx > i_entity_next_vx:
                min_vx = i_entity_next_vx
            if min_vy > i_entity_next_vy:
                min_vy = i_entity_next_vy
            
            
            if (abs(max_vx - min_vx)<flock_step_eps and abs(max_vy - min_vy)<flock_step_eps):
                flock_step = t
            
            if entity_next_x >= 10:
                entity_next_x = -entity_next_x
            
            i_entity_next_x = i_entity_next_x % 10
            i_entity_next_y = i_entity_next_y % 10
            
            lst_pos_x[i].append(i_entity_next_x)
            lst_pos_y[i].append(i_entity_next_y)
            lst_vx[i].append(i_entity_next_vx)
            lst_vy[i].append(i_entity_next_vy)
        
            
        t += eps
        lst_t.append(t)
    
   
    print("Resolved in " + str((time.time() - tstart_sim)/60) + " s")
    return (lst_t, lst_pos_x, lst_pos_y, lst_vx, lst_vy, flock_step)

    
def cucker_smale2d_modified(x_pop_init, y_pop_init, xinit_predateur, yinit_predateur, vx_pop_init, vy_pop_init, vx_init_predateur, vy_init_predateur, t_min, t_max, eps, force_intensity, com_rate, eq_x_pred, eq_y_pred, eq_vx_pred, eq_vy_pred):
    tstart_sim = time.time()
    lst_t = [t_min] #int->list int
    lst_pos_x = x_pop_init #[[x1_init, ... x1_finish], [x2_init, ... x2_finish], ..., [xn_init, ... xn_finish]]
    lst_pos_y = y_pop_init
    lst_vx = vx_pop_init#idem 
    lst_vy = vy_pop_init
    t = t_min
    lst_x_predateur = [xinit_predateur]
    lst_y_predateur = [yinit_predateur]
    lst_vx_predateur = [vx_init_predateur]
    lst_vy_predateur = [vy_init_predateur]
    
    N = len(x_pop_init)
    #print(lst_pos_x)
    #rq : N peut être déduit de la longeur du tableau principal
    while t < t_max: #t pas nécessairement un entier selon epsilon
        center_of_mass_coords = center_of_mass_coordinates(t, lst_pos_x, lst_pos_y)
        center_of_mass_speed = center_of_mass_speeds(t, lst_vx, lst_vy)
        
        x_predateur = lst_x_predateur[-1]
        y_predateur = lst_y_predateur[-1]
        vx_predateur = lst_vx_predateur[-1]
        vy_predateur = lst_vy_predateur[-1]
        
        coeff_droite = (center_of_mass_coords[1] - y_predateur)/(center_of_mass_coords[0] - x_predateur)
        
        lst_x_predateur.append(eq_x_pred(x_predateur+2))
        lst_y_predateur.append(eq_y_pred(y_predateur+2))
        lst_vx_predateur.append(eq_vx_pred(vx_predateur))
        lst_vy_predateur.append(eq_vy_pred(vy_predateur))
        
        lst_pos_x[N-1].append(x_predateur)
        lst_pos_y[N-1].append(y_predateur)
        lst_vx[N-1].append(vx_predateur)
        lst_vy[N-1].append(vy_predateur)
         
        for i in range(N-1): #entity i            
            acceleration_x_iter = 0.0
            acceleration_y_iter = 0.0
            
            i_entity_x = lst_pos_x[i]
            i_entity_y = lst_pos_y[i]
            i_entity_vx = lst_vx[i]
            i_entity_vy = lst_vy[i]
            k = len(i_entity_x)
            #print(i_entity_x)
            i_entity_next_x = eps*i_entity_vx[k-1] + i_entity_x[k-1]
            i_entity_next_y = eps*i_entity_vy[k-1] + i_entity_y[k-1]
            
            for j in range(N-1): #entity j
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
            
            lst_pos_x[i].append(i_entity_next_x)
            lst_pos_y[i].append(i_entity_next_y)
            lst_vx[i].append(i_entity_next_vx)
            lst_vy[i].append(i_entity_next_vy)
        
            
        t += eps
        lst_t.append(t)
    
   
    print("Resolved in " + str((time.time() - tstart_sim)/60) + " s")
    return (lst_t, lst_pos_x, lst_pos_y, lst_vx, lst_vy)


def cucker_smale2d_for_flock_time_range(N, x_pop_init, y_pop_init, vx_pop_init, vy_pop_init, t_min, t_max, eps, force_intensity, com_rate):
    solution = cucker_smale2d_fix(N, x_pop_init, y_pop_init, vx_pop_init, vy_pop_init, 0, t_max, eps, force_intensity, com_rate)
    t = solution[0]
    nt = t[int(t_min//eps):int(t_max//eps)]
    x = solution[1]
    print("len t = " + str(len(t)))
    print("len x = " + str(len(x)))
    nx = x[int(t_min//eps):int(t_max//eps)]
    y = solution[2]
    ny = y[int(t_min//eps):int(t_max//eps)]
    vx = solution[3]
    nvx = vx[int(t_min//eps):int(t_max//eps)]
    vy = solution[4]
    nvy = vy[int(t_min//eps):int(t_max//eps)]
    
    return [nt, nx, ny, nvx, nvy] 
   

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


def center_of_mass_speeds(vx, vy):
    center_of_mass_vx = 0
    center_of_mass_vy = 0
    n = len(x)
    for i in range(n):
         center_of_mass_vx += vx[i][t]
         center_of_mass_vy += vy[i][t]
         
    center_of_mass_vx *= 1/n
    center_of_mass_vy *= 1/n
    return (center_of_mass_vx, center_of_mass_vy)


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
        k=1.5
        #k=1/8
        x_stop.append(x[j][t])
        y_stop.append(y[j][t])
        vx_stop.append(vx[j][t])
        vy_stop.append(vy[j][t])
        
        center_of_mass_x += x_stop[j]
        center_of_mass_y += y_stop[j]
        center_of_mass_vx += vx_stop[j]
        center_of_mass_vy += vy_stop[j]
        
        if print_arrow:
            if j == N-1:
                plt.arrow(x[j][t], y[j][t], vx[j][t]*k, vy[j][t]*k, head_width=0.1, length_includes_head=True, color='green')
            else:
                plt.arrow(x[j][t], y[j][t], vx[j][t]*k, vy[j][t]*k, head_width=0.1, length_includes_head=True, color='blue')

    center_of_mass_x *= 1/N
    center_of_mass_y *= 1/N
    center_of_mass_vx *= 1/N
    center_of_mass_vy *= 1/N
    plt.scatter(x_stop, y_stop, color=color)
    plt.scatter(center_of_mass_x, center_of_mass_y, color="green")
    plt.arrow(center_of_mass_x, center_of_mass_y, center_of_mass_vx*3, center_of_mass_vy*3, head_width=0.1, length_includes_head=True, color="orange")
    
    if circle:
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.sqrt(4)
        x1 = r*np.cos(theta) + center_of_mass_x
        x2 = r*np.sin(theta) + center_of_mass_y
        plt.plot(x1, x2)
  
    
def print_in_realtime(t_min, t_max, x, y, vx, vy, force_intensity, communication_rate, frame_rate_ms = 30, eps=0.1):
    t = 0
    while t <= (t_max-t_min):
        plt.clf()
        scatter_at_specific_time_2d(t, x, y, vx, vy, circle=False)
        plt.title("t=" + str(t)+" (ut), fps : " + str(1/(frame_rate_ms/1000)) + ", t=[" + str(t_min) + "," + str(t_max) + "], λ=" + str(force_intensity) + ", ε=" + str(eps) + ", α=" + str(communication_rate))
        plt.pause(frame_rate_ms/1000)
        t += 1

    plt.cla()
    plt.xlabel("x(t)")
    plt.ylabel("y(t)")

        
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
    a = [[eps],[force_intensity], [communication_rate]]
    with open(str(time.time()) + "_modified_data.csv","w+") as my_csv:            # writing the file as my_csv
        csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
        csvWriter.writerows(a)
    
    
def init_cm2dfix():
        init_pos_x = []
        init_pos_y = []
        init_vx =  []
        init_vy =  []
        
        N = 100
        t_min = 0
        t_max = 100
        eps = 0.1
        force_intensity = 4
        
        for i in range(N):
            init_vx.append([10*random.random()-5])
            init_vy.append([10*random.random()-5])
        
        circular_distrib = random_circular_distribution(2, 0, 0, N)
        init_pos_x = circular_distrib[0]
        init_pos_y = circular_distrib[1]
        

        solution = cucker_smale2d_fix(N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity, 1/2)
        positions_x = solution[1]
        positions_y = solution[2]
        vitesses_x = solution[3]
        vitesses_y = solution[4]
  
        print_in_realtime(0, 100, positions_x, positions_y, vitesses_x, vitesses_y, force_intensity, 1/2)
            

def simulation_comparison_crusade():
    init_pos_x = []
    init_pos_y = []
    init_vx =  []
    init_vy =  []
    
    N = 4
    t_min = 0
    t_max = 4
    eps = 0.1
    force_intensity = 1
    
    for i in range(N):
        init_pos_x.append([random.random()])
        init_pos_y.append([random.random()])
        init_vx.append([random.random()])
        init_vy.append([random.random()])
    
    export_initial_conditions(N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity)
    
    com_rate_exp_array = [3/4, 1/2, 1/3, 1/4, 1/5, 1/6]
    iterations = len(com_rate_exp_array)
    
    for i in range(iterations):
        #print(init_pos_x)
        solution = cucker_smale2d_fix(N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity, com_rate_exp_array[i])
        positions_x = solution[1]
        positions_y = solution[2]
        vitesses_x = solution[3]
        vitesses_y = solution[4]
        plt.subplot(330 + (i+1))
        plt.title(com_rate_exp_array[i])
        scatter_at_specific_time_2d(60, positions_x, positions_y, vitesses_x, vitesses_y)
#        #print_in_realtime(0,t_max, positions_x, positions_y, vitesses_x, vitesses_y, force_intensity_array[i], communication_rate_exp)
#         flock(i, eps, 1e-3, init_pos_x, init_pos_y, init_vx, init_vy, force_intensity, com_rate_exp_array[i])
    
    plt.savefig ("./final.png")
    
    
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
     
    solution = cucker_smale2d_fix(g1_N + g2_N, init_pos_x, init_pos_y, init_vx, init_vy, t_min, t_max, eps, force_intensity, 1/2)
    positions_x = solution[1]
    positions_y = solution[2]
    vitesses_x = solution[3]
    vitesses_y = solution[4]
    print_in_realtime(t_min, t_max, positions_x, positions_y, vitesses_x, vitesses_y, force_intensity, 1/2)
    
    
def gen_trajectoire_predateur(t_min, t_max, xinit, yinit, vxinit, vyinit, eq_traj_x, eq_traj_y, eq_vx, eq_vy, eps):
    liste_t = [t_min]
    liste_x = [xinit]
    liste_y = [yinit]
    liste_vx = [vxinit]
    liste_vy = [vyinit]
    t = t_min
    while t < t_max:
        x = liste_x[-1]
        y = liste_y[-1]
        vx = liste_vx[-1]
        vy = liste_vy[-1]
        
        liste_x.append(eq_traj_x(x+2*eps))
        liste_y.append(eq_traj_y(y+2*eps))
        liste_vx.append(eq_vx(vx+eps))
        liste_vy.append(eq_vy(vy+eps))
        
        t += eps
        liste_t.append(t)
        
    return (liste_t, liste_x, liste_y, liste_vx, liste_vx, liste_vy)


def lancement_sim_avec_predateur():
    init_pos_x = []
    init_pos_y = []
    init_vx =  [] + [[2.0]]
    init_vy =  [] + [[2.0]]
    
    N = 10
    t_min = 0
    t_max = 100
    eps = 0.1
    force_intensity = 1
    
    for i in range(N):
        init_vx.append([10*random.random()-5])
        init_vy.append([10*random.random()-5])
    
    circular_distrib = random_circular_distribution(2, 0, 0, N)
    init_pos_x = circular_distrib[0] + [[-10.0]]
    init_pos_y = circular_distrib[1] + [[-10.0]]

    solution = cucker_smale2d_modified(init_pos_x, init_pos_y, 10, 10, init_vx, init_vy, 2, 2, t_min, t_max, eps, force_intensity, 1/2, parab, parab, cst, cst)
    positions_x = solution[1]
    positions_y = solution[2]
    vitesses_x = solution[3]
    vitesses_y = solution[4]
    print_in_realtime(t_min, t_max, positions_x, positions_y, vitesses_x, vitesses_y, force_intensity, 1/2)


#lancement_sim_avec_predateur()
#simulation_comparison_crusade()      
init_cm2dfix()
#gen_distrib_non_homogene()
