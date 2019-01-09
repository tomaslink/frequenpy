from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

__author__      = "Tomás Link"

plt.clf() 
fig = plt.figure(figsize=(8, 5))
fig.set_dpi(50)
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2), frameon=False)
ax.set_xticks([])
ax.set_yticks([])


# Parámetros de entrada

saveAnim = input("GUARDAR ANIMACION? y/n: ")

# Propiedades del sistema

L = 0.2             # longitud natural (metros)
K = 0.05            # constante elástica (N/m)
m = 5               # masa (kg)
A = 1             # amplitud máxima (metros)
w0 = np.sqrt(K/m);  # 

line, = ax.plot([0,1], [0,1],'o-',markersize=15)


def init():
    line.set_data([], [])
    return line,

def resorte(i):
    x = A*np.cos(5*np.radians(i))
    line.set_data([0, 1], [0, x])
    return line,

anim = animation.FuncAnimation(fig, resorte, 
                                init_func=init, 
                               frames = 360,
                               interval=30,
                               blit=True,
                               repeat=True)


#Imprimiendo el mensaje para guardar la animación

if (saveAnim == "y"):
    print("GUARDANDO ANIMACION...ESTO PUEDE LLEVAR UN RATO")
    anim.save("resorte"+'.mp4', fps=30, extra_args=['-vcodec', 'libx264'])


plt.show()

