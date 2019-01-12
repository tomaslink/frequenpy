import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from settings import FIXED_BOUNDARY, MIXED_BOUNDARY, FREE_BOUNDARY


class CoupledOscillators(object):

    def __init__(self, N, modes, boundary, elastic_constant, longitude, rho, amplitude, save_anim):
        self._N = N
        self._modes = modes
        self._boundary = boundary
        self._elastic_constant = elastic_constant
        self._longitude = longitude
        self._rho = rho
        self._amplitude = amplitude
        self._save_anim = save_anim

        self._a = longitude / (N + 1)
        m = rho * self._a
        K = (elastic_constant / self._a)
        w0_2 = K / m
        self._M = self._tridiagonal_matrix(-1 * w0_2, 2 * w0_2, -1 * w0_2)
        self._w2 = self._frequencies()
        self.springs = self._build_springs()

    def _build_springs(self):
        N = self._N
        a = self._a
        L = self._longitude
        resortes = []
        for n in range(0, self._N + 1):

            X = [-L / 2 + n * a, -L / 2 + (n + 1) * a]
            Y = [0, 0]
            if (N > 20):
                resorte = plt.Line2D(X, Y, color='black')
            else:
                resorte = plt.Line2D(X, Y, color='black', marker='o', markersize='4', markerfacecolor='blue')
            resortes.append(resorte)
        return resortes

    def get_fig(self):
        L = self._longitude
        plt.clf()
        fig = plt.figure(figsize=(10, 5))
        fig.set_dpi(75)
        ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1), frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.add_line(plt.Line2D((-L / 2, -L / 2), (0.8, 0.8), lw=2.5, color='black'))
        # ax.add_line(plt.Line2D((L / 2, L / 2), (-0.8, 0.8), lw=2.5, color='black'))

        for resorte in self.springs:
            ax.add_line(resorte)
        return fig

    def _frequencies(self):
        M = self._M
        w2, D = np.linalg.eig(M)
        sort_perm = w2.argsort()
        D = D[:, sort_perm]
        D = np.transpose(D)
        w2.sort()
        return w2

    def _tridiagonal_matrix(self, abajo, medio, arriba):
        N = self._N
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

    def _w(self, p):
        return np.sqrt(self._w2[p - 1])

    def _normal_mode_p_for_mass_n(self, p, n):
        return (p * n * np.pi) / (self._N + 1)

    def equation_form_mass_n(self, n, t):
        A = self._amplitude
        equation = np.sin(0)
        for p in self._modes:
            equation += A * np.sin(self._normal_mode_p_for_mass_n(p, n)) * np.cos(np.radians(self._w(p) * t))
        return equation


def init():
    return []


def execute():

    N = 10
    modes = (1, 2, 3,)
    boundary = 0
    k_i = 0.2
    L = 1.5              # largo total (metros)
    rho = 0.1             # densidad lineal masa (kg/m)
    A = 0.4              # amplitud maxima (metros)
    save_anim = 0

    system = CoupledOscillators(N, modes, boundary, k_i, L, rho, A, save_anim)
    fig = system.get_fig()

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   fargs=(system,),
                                   frames=500,
                                   interval=30,
                                   blit=True,
                                   repeat=True)
    if (save_anim == 1):
        print("GUARDANDO ANIMACION...ESTO PUEDE LLEVAR UN RATO")
        anim.save('test' + '.mp4')

    plt.show()


def animate(i, system):
    global tiempo
    for r in range(0, len(system.springs)):
        resorte = system.springs[r]
        tiempo = i
        masaIzquierda = r
        masaDerecha = r + 1
        yIzq = system.equation_form_mass_n(masaIzquierda, tiempo)
        yDer = system.equation_form_mass_n(masaDerecha, tiempo)
        resorte.set_data(resorte.get_xdata(), [yIzq, yDer])
    return[]


execute()
