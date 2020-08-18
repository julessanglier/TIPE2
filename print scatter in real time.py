def scatter_at_specific_time_2d(t, x, y, vx, vy, color = "red", print_arrow = True, show = True, arrow_division_rate = 8):
    x_stop = []
    y_stop = []
    vx_stop = []
    vy_stop = []
    N = len(x)
    for j in range(N):
        x_stop.append(x[j][t])
        y_stop.append(y[j][t])
        vx_stop.append(vx[j][t])
        vy_stop.append(vy[j][t])
        if print_arrow:
            plt.arrow(x[j][t], y[j][t], vx[j][t]/arrow_division_rate, vy[j][t]/arrow_division_rate, head_width=0.01, length_includes_head=True, color='b')
        
    plt.scatter(x_stop, y_stop, color=color)
    #print(x_stop)
    
def print_in_realtime(t_min, t_max, x, y, vx, vy, frame_rate_ms = 500):
    t = 0
    while t <= (t_max-t_min):
        plt.clf()
        scatter_at_specific_time_2d(t, x, y, vx, vy)
        plt.show()
        plt.title("t=" + str(t)+"s")
        plt.pause(0.01)
        t += 1
