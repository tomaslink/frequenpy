from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

__author__      = "Tomás Link"

plt.clf() 
fig = plt.figure(figsize=(8, 5))
fig.set_dpi(50)
ax = Axes3D(fig)

#ax = plt.axes(xlim=(-0.8, 0.8), ylim=(-0.5, 0.5), frameon=False)
ax.set_xticks([])
ax.set_yticks([])



# Parámetros de entrada

N = 0;
while((N == 0) | (N>100)):
    if (N > 100):
        print("El límite de masas es 100")
    N = int(input("CANTIDAD DE MASAS: "));

modos = input("MODOS NORMALES separados por punto: ");
modos = list(map(int, modos.split('.')))
saveAnim = input("GUARDAR ANIMACION? y/n: ")

# Propiedades del sistema

K_1 = 200           # constante elástica inversa por unidad de longitud (N^(-1))
rho = 0.5           # densidad lineal masa (kg/m) 
L = 1.5             # largo total (metros)
a = L/(N + 1);      # distancia entre masas (metros)
m = rho*a           # masa (kg)
K = (K_1*a)**(-1)   # constante elástica (N/m)
A = 0.2             # amplitud máxima (metros)
w02 = K/m;          # 

def k(p):
    return (p*np.pi)/(a*(N+1))

# Limitando la amplitud máxima del movimiento en caso de superposición de modos.
# Mediante una normalización
'''
amplitudes = []
for n in range(0, N):
    ampMasa = 0
    for p in range(0, len(modos)):
        ampMasa += np.sin(k(p+1)*(n+1)*a)
    amplitudes.append(ampMasa)

ampMax = max(amplitudes);
if (ampMax > 1):
    A = A/ampMax
'''
# Determinando el radio de las masas según la cantidad que haya

radioMasas = 0;

if (N > 50):
    radioMasas = 0.05/N
elif ((N <= 50) & (N > 1)):
    radioMasas = np.e**(7/N**2)/100
else: 
    radioMasas = 0.07;


masas = []

# cálculo de matrix tridiagonal de NxN

def tridiagonalMatrix(down, middle, up):
    M = []
    for m in range(0, N):
        row = []
        for n in range(0, N):
            if m == n:
                row.append(middle)
            elif n == (m - 1):
                row.append(down)
            elif n == (m + 1):
                row.append(up)
            else:
                row.append(0)
        
        M.append(row);
    return M;

M = tridiagonalMatrix(-1*w02, 2*w02, -1*w02)

# autovalores y autovectores 

omega2, D = np.linalg.eig(M)
sort_perm = omega2.argsort()
D = D[:, sort_perm]
D = np.transpose(D)
omega2.sort()

print(omega2)

### Funciones 



def w(p):
    return omega2[p - 1]

def normalModePforMassN(p, n, t):
    #return A*D[p-1][n-1]*np.cos(w(p)*t)
    return A*np.sin(k(p)*n*a)*np.cos(t*w(p))

def equationForMassN(modes, n, t):
    sum = np.sin(0);
    for p in modes:
        sum += normalModePforMassN(p, n, t)
    return sum;

for n in range(0, N):
    posicionXY = (-a*((N-1)/2) + n*a, 0)
    masas.append(plt.Circle(posicionXY, radioMasas, fc='b'))

def init():
    ax.add_line(plt.Line2D((-L/2, -L/2), (-0.2, 0.2), lw=2.5, color='black'))
    ax.add_line(plt.Line2D((L/2, L/2), (-0.2, 0.2), lw=2.5, color='black'))
    for n in range(0, len(masas)):
        posicionXY = (-a*((N-1)/2) + n*a, 0)
        masas[n].center = posicionXY
        ax.add_patch(masas[n])
        art3d.pathpatch_2d_to_3d(masas[n], z=0, zdir=i)
    
    return []

movementArray = np.zeros((N, 360));

for i in range (0, len(movementArray)):
    for j in range(0, 360):
        movementArray[i][j] = equationForMassN(modos, i+1, j);



def animationManage(i, masas):
    for n in range(0, len(masas)):
        animateMasa(i, masas[n], n)
    return []

def animateMasa(t, patch, n): 
    x, y = patch.center
    y = movementArray[n][t];
    patch.center = (x, y)
    return patch

anim = animation.FuncAnimation(fig, animationManage, 
                               init_func=init,
                               fargs=(masas,), 
                               frames=360, 
                               interval=10,
                               blit=True)


#Imprimiendo el mensaje para guardar la animación

name = 'transversal-'+ str(N) +'masas-Modos-'

for modo in modos:
    name += str(modo) + "-"

if (saveAnim == "y"):
    print("GUARDANDO ANIMACION...ESTO PUEDE LLEVAR UN RATO")
    anim.save(name+'.mp4', fps=30, extra_args=['-vcodec', 'libx264'])


plt.show()

