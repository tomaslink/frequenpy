from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
import os

plt.clf()
fig = plt.figure(figsize=(10, 5))
fig.set_dpi(75)
ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1), frameon=False)
ax.set_xticks([])
ax.set_yticks([])

# CONSTANTES

EXTREMOS_FIJOS = 0
EXTREMOS_MIXTOS = 1
EXTREMOS_LIBRES = 2

# Parametros de entrada

N = 0
while((N == 0) | (N > 100)):
    if (N > 50):
        print("El limite de masas es 100")
    N = int(input("CANTIDAD DE MASAS: "))

modos = str(input("MODOS NORMALES separados por punto: "))
modos = list(map(int, modos.split('.')))
contorno = int(input(
    "CONDICIONES DE CONTORNO (extremos fijos(0), extremos mixtos(1), extremos libres(2) :"))
VELOCIDAD = float(input("VELOCIDAD: "))
saveAnim = str(input("GUARDAR ANIMACION? y/n: "))

contorno = 0
VELOCIDAD = 1
phi = 0
if (contorno == EXTREMOS_LIBRES):
    phi = np.pi / 2


# Propiedades del sistema

# constante elastica inversa por unidad de longitud (N^(-1))
K_1 = 0.2
rho = 2               # densidad lineal masa (kg/m)
L = 1.5             # largo total (metros)
a = L / (N + 1)      # distancia entre masas (metros)
m = rho * a           # masa (kg)
K = (K_1 * a)**(-1)   # constante elastica (N/m)
A = 0.4             # amplitud maxima (metros)
w02 = K / m
#


def k(p):
    if ((contorno == EXTREMOS_FIJOS) | (contorno == EXTREMOS_LIBRES)):
        return (p * np.pi) / (a * (N + 1))
    elif(contorno == EXTREMOS_MIXTOS):
        return ((p + 1 / 2) * np.pi) / (a * (N + 1))


resortes = []

for n in range(0, N + 1):
    X = [-L / 2 + n * a, -L / 2 + (n + 1) * a]
    Y = [0, 0]
    if (N > 20):
        resorte = plt.Line2D(X, Y, color='black')
    else:
        resorte = plt.Line2D(X, Y, color='black', marker='o',
                             markersize='4', markerfacecolor='blue')
    resortes.append(resorte)

for resorte in resortes:
    ax.add_line(resorte)
    ax.add_line(plt.Line2D((-L / 2, -L / 2),
                           (-0.8, 0.8), lw=2.5, color='black'))
    ax.add_line(plt.Line2D((L / 2, L / 2), (-0.8, 0.8), lw=2.5, color='black'))

# calculo de matrix tridiagonal de NxN


def matrizTridiagonal(abajo, medio, arriba):
    M = []
    for m in range(0, N):
        fila = []
        for n in range(0, N):
            if m == n:
                fila.append(medio)
            elif n == (m - 1):
                fila.append(abajo)
            elif n == (m + 1):
                fila.append(arriba)
            else:
                fila.append(0)
        M.append(fila)
    return M


M = matrizTridiagonal(-1 * w02, 2 * w02, -1 * w02)

# autovalores y autovectores

w2, D = np.linalg.eig(M)
sort_perm = w2.argsort()
D = D[:, sort_perm]
D = np.transpose(D)
w2.sort()

# Funciones


def theta_p(p):
    return theta[p - 1]


def w(p):
    return np.sqrt(w2[p - 1])


def modoNormalPdeMasaN(p, n, t):
    return A * np.sin(k(p) * n * a + phi) * np.cos(np.radians(w(p) * t * VELOCIDAD))


def ecuacionDeMasaN(modes, n, t):
    sum = np.sin(0)
    for p in modes:
        sum += modoNormalPdeMasaN(p, n, t)
    return sum


def init():
    return []


def animate(i, resortes):
    global tiempo
    for r in range(0, len(resortes)):
        resorte = resortes[r]
        tiempo = i
        masaIzquierda = r
        masaDerecha = r + 1
        yIzq = ecuacionDeMasaN(modos, masaIzquierda, tiempo)
        yDer = ecuacionDeMasaN(modos, masaDerecha, tiempo)
        resorte.set_data(resorte.get_xdata(), [yIzq, yDer])
    return[]


# Invoca la animacion
anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               fargs=(resortes,),
                               frames=500,
                               interval=30,
                               blit=True,
                               repeat=True)


# Guarda la animacion

if (saveAnim == "y"):
    name = 'transversal-' + str(N) + 'masas-Modos-'
    for m in range(0, len(modos)):
        if (m == len(modos) - 1):
            extremos = ''
            if (contorno == EXTREMOS_FIJOS):
                extremos += "-EXTREMOS-FIJOS"
            elif (contorno == EXTREMOS_MIXTOS):
                extremos += "-EXTREMOS-MIXTOS"
            elif (contorno == EXTREMOS_LIBRES):
                extremos += "-EXTREOMS-LIBRES"
            name += str(modos[m]) + extremos + '-version-'
        else:
            name += str(modos[m]) + "-"
    version = 1
    name += str(version)
    path = os.path.dirname(os.path.abspath(__file__))
    while (Path(path + '/' + name + '.mp4').is_file()):
        name = name[:-1]
        version += 1
        if (version > 10):
            version -= 10
        name += str(version)

    print("GUARDANDO ANIMACION...ESTO PUEDE LLEVAR UN RATO")
    anim.save(name + '.mp4')


plt.show()
