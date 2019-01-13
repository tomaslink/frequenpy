from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import tkinter.ttk as ttk
import copy

# FIGURA
plt.clf()
fig = plt.figure(figsize=(6, 3), facecolor='black')
fig.set_dpi(100)
ax = plt.axes(xlim=(-1.2, 1.2), ylim=(-0.5, 0.5), frameon=False)
ax.set_xticks([])
ax.set_yticks([])

# GUI
root = Tk()
label = Label(root, text="Modos normales de una cuerda con cuentas").grid(
    column=0, row=0)
center = Frame(root)
center.grid(row=1, column=0)
canvas = FigureCanvasTkAgg(fig, master=center)
canvas.get_tk_widget().pack(side="left")
right_column = Frame(root)
right_column.grid(row=1, column=1, sticky="ew")
bottom_row = Frame(root)
bottom_row.grid(row=2, column=0)
root.grid_rowconfigure(2, weight=2)

# CONSTANTES

EXTREMOS_FIJOS = 0
EXTREMOS_MIXTOS = 1
EXTREMOS_LIBRES = 2
TRANSVERSAL = 0
LONGITUDINAL = 1

anim = []
modos = {}
tiempo = 0
contorno = 0
VELOCIDAD = 1
direccion = TRANSVERSAL


# Parametros de entrada
N = 2


def inicializarModos():
    global modos
    for m in range(0, N):
        modos[m] = 0


def actualizarModos():
    global modos
    if len(modos) > N:
        for k in modos.keys():
            if k > N - 1:
                del modos[k]
    if (len(modos) < N):
        for n in range(len(modos), N):
            modos[n] = 0


inicializarModos()
modos[0] = 1
theta = np.zeros(N)  # fase inicial
M = np.zeros((N, N))  # matriz tridiagonal
w2 = np.zeros(N)  # vector de N autovalores
D = np.zeros((N, N))  # matriz de NxN autovectores


def phi():
    phi = 0
    if (contorno == EXTREMOS_LIBRES):
        phi = np.pi / 2
    return phi


# Propiedades constantes del sistema

# constante elastica inversa por unidad de longitud (N^(-1))
K_1 = 500
rho = 2            # densidad lineal masa (kg/m)
L = 2             # largo total (metros)
A = 0.4             # amplitud maxima (metros)


def A_p(p):
    return A * modos[p]


def a():
    return L / (N + 1)        # distancia entre masas (metros)


def m():
    return rho * a()          # masa (kg)


def K():
    return (K_1 * a())**(-1)  # constante elastica (N/m)


def w02():
    return K() / m()        # frecuencia fundamental


def k(p):
    p = p + 1
    if ((contorno == EXTREMOS_FIJOS) | (contorno == EXTREMOS_LIBRES)):
        return (p * np.pi) / (a() * (N + 1))
    elif(contorno == EXTREMOS_MIXTOS):
        return ((p + 1 / 2) * np.pi) / (a() * (N + 1))


def construirResortes():
    resortes = []
    for n in range(0, N + 1):
        X = [-L / 2 + n * a(), -L / 2 + (n + 1) * a()]
        Y = [0, 0]
        if (N > 25):
            resorte = plt.Line2D(X, Y, color='white', lw=0.3)
        else:
            resorte = plt.Line2D(X, Y, color='white', lw=0.3,
                                 marker='o', markersize='5', markerfacecolor='white')
        resortes.append(resorte)
    return resortes


def dibujarResortes():
    for resorte in resortes:
        ax.add_line(resorte)


def dibujarParedes():
    ax.add_line(plt.Line2D((-L / 2, -L / 2),
                           (-0.8, 0.8), lw=0.5, color='white'))
    ax.add_line(plt.Line2D((L / 2, L / 2), (-0.8, 0.8), lw=0.5, color='white'))


resortes = construirResortes()
dibujarResortes()
dibujarParedes()

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


def iniciarMatriz():
    global M
    M = matrizTridiagonal(-1 * w02(), 2 * w02(), -1 * w02())

# autovalores y autovectores


def inicializarFrecuencias():
    global w2, D
    w2, D = np.linalg.eig(M)
    sort_perm = w2.argsort()
    D = D[:, sort_perm]
    D = np.transpose(D)
    w2.sort()


iniciarMatriz()
inicializarFrecuencias()


def theta_p(p):
    return theta[p]


def w(p):
    return np.sqrt(w2[p])


def modoNormalPdeMasaN(p, n, t):
    return A_p(p) * np.sin(k(p) * n * a() + phi()) * np.cos(w(p) * t * VELOCIDAD + theta_p(p))


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
        izq = ecuacionDeMasaN(modos, masaIzquierda, tiempo)
        der = ecuacionDeMasaN(modos, masaDerecha, tiempo)
        if (direccion == TRANSVERSAL):
            resorte.set_ydata([izq, der])
        if (direccion == LONGITUDINAL):
            x1, x2 = resorte.get_xdata()
            resorte.set_xdata([x1 + izq, x2 + der])
    return[]


def iniciarAnimacion():
    global anim
    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   fargs=(resortes,),
                                   frames=10000,
                                   interval=5,
                                   blit=True,
                                   repeat=True)


def cambiarVelocidad(event):
    global VELOCIDAD
    global theta
    global tiempo
    vActual = VELOCIDAD
    VELOCIDAD = porcentajeVelocidad.get() / 100
    thetaActual = theta
    for p in modos:  # Ajusta la fase inicial del siguiente frame para que el cambio sea fluido
        frecActual = w(p) * vActual
        theta[p] = (frecActual - w(p) * VELOCIDAD) * \
            (tiempo + 1) + thetaActual[p]


controlesModos = []


def cambiarExtremos(event):
    global contorno
    contorno = extremos.current()


def cambiarAmplitudModo(i):
    global modos
    modos[i] = controlesModos[i].get() / 100


def ReiniciarModos():
    inicializarModos()
    for m in range(0, len(controlesModos)):
        if (m > 0):
            controlesModos[m].set(0)


def dibujarControlesModos():
    global controlesModos
    controlesModos = []
    for i in range(0, N):
        dibujarControlModo(i)


button = Button(bottom_row, command=ReiniciarModos, text="Reset")
button.pack(side="right")


def dibujarControlModo(i):
    controlModo = Scale(bottom_row, from_=100, to=0, width=10, showvalue=0,
                        orient="vertical", command=lambda _, modo=i: cambiarAmplitudModo(modo))
    controlModo.set(modos[i] * 100)
    controlesModos.append(controlModo)
    controlModo.pack(side="left", padx=1)


dibujarControlesModos()

controlesModos[0].set(100)


def reiniciarControlesModos():
    for controlModo in controlesModos:
        controlModo.destroy()
    dibujarControlesModos()


def eliminarResortes():
    for resorte in resortes:
        resorte.remove()


def reiniciarResortes():
    global resortes
    eliminarResortes()
    resortes = construirResortes()
    dibujarResortes()


def reiniciarPantalla():
    global theta
    theta = np.zeros(N)
    iniciarMatriz()
    inicializarFrecuencias()
    actualizarModos()
    reiniciarResortes()
    reiniciarControlesModos()


def cambiarCantidadMasas(event):
    global N
    anim.event_source.stop()
    N = cantidadMasas.current() + 1
    reiniciarPantalla()
    iniciarAnimacion()


porcentajeVelocidad = Scale(center, from_=0, to=200, length=100,
                            label='Velocidad', orient="horizontal", command=cambiarVelocidad)
porcentajeVelocidad.set(100)
porcentajeVelocidad.pack(pady=20, padx=1)

labelContorno = Label(center, text="Candiciones de contorno")
labelContorno.pack(pady=1)
extremos = ttk.Combobox(center, textvariable=contorno)
extremos['values'] = ('Extremos Fijos', 'Extremos Mixtoms', 'Extremos Libres')
extremos.bind('<<ComboboxSelected>>', cambiarExtremos)
extremos.current(contorno)
extremos.pack(pady=5)

labelCantMasas = Label(center, text="Cantidad  de cuentas")
labelCantMasas.pack(pady=1)
cantidadMasas = ttk.Combobox(center)
values = x = [i for i in range(1, 35)]
cantidadMasas['values'] = values
cantidadMasas.bind('<<ComboboxSelected>>', cambiarCantidadMasas)
cantidadMasas.current(N - 1)
cantidadMasas.pack(pady=5)

# Invoca la animacion
iniciarAnimacion()

# Guarda la animacion


def guardarAnimacion():
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


mainloop()

# plt.show()
