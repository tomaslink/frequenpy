import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as mplstyle
from settings import FIXED_BOUNDARY, MIXED_BOUNDARY, FREE_BOUNDARY

mplstyle.use('fast')


class CoupledOscillators(object):

    def __init__(self, n_masses, modes, boundary, elastic_constant, longitude, rho, amplitude, save_anim):
        self._n_masses = n_masses
        self._modes = modes
        self._boundary = boundary
        self._elastic_constant = elastic_constant
        self._longitude = longitude
        self._rho = rho
        self._amplitude = amplitude
        self._save_anim = save_anim

        self._a = longitude / (n_masses + 1)
        m = rho * self._a
        K = (elastic_constant / self._a)
        w0_2 = K / m
        self._M = self._tridiagonal_matrix(-1 * w0_2, 2 * w0_2, -1 * w0_2)
        self._omega_squared = self._frequencies()
        self._springs = self._build_springs()
        self._frames = self._build_frames()

    def _resolve_marker_size(self):
        N = self._n_masses
        marker_size = 0
        if (N > 50):
            marker_size = 0
        elif (N > 30):
            marker_size = 2
        elif (N > 15):
            marker_size = 4
        else:
            marker_size = 8
        return marker_size

    def _build_springs(self):
        N = self._n_masses
        a = self._a
        L = self._longitude
        resortes = []
        for n in range(0, N + 1):
            X = [-L / 2 + n * a, -L / 2 + (n + 1) * a]
            Y = [0, 0]
            resorte = plt.Line2D(
                X, Y, color='black',
                marker='o',
                markersize=self._resolve_marker_size(),
                markerfacecolor='blue'
            )
            resortes.append(resorte)
        return resortes

    def get_fig(self):
        L = self._longitude
        plt.clf()
        fig = plt.figure(figsize=(10, 5))
        fig.set_dpi(100)
        ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1), frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.add_line(
            plt.Line2D((-L / 2, -L / 2), (-0.8, 0.8), lw=2.5, color='black')
        )
        ax.add_line(
            plt.Line2D((L / 2, L / 2), (-0.8, 0.8), lw=2.5, color='black')
        )

        for resorte in self.springs:
            ax.add_line(resorte)
        return fig

    def _frequencies(self):
        M = self._M
        w2, _ = np.linalg.eig(M)
        w2.sort()
        return w2

    def _tridiagonal_matrix(self, low, mid, upp):
        N = self._n_masses
        A = np.eye(N, N, k=-1) * low + \
            np.eye(N, N) * mid + \
            np.eye(N, N, k=1) * upp
        A[A == 0.] = 0.
        return A

    def _omega(self, p):
        return np.sqrt(self._omega_squared[p - 1])

    def _normal_mode_p_for_mass_n(self, p, n):
        return (p * n * np.pi) / (self._n_masses + 1)

    def _position_for_mass_n_at_time_t(self, n, t):
        A = self._amplitude
        return sum([
            A *
            np.sin(self._normal_mode_p_for_mass_n(p, n)) *
            np.cos(np.radians(self._omega(p) * t))
            for p
            in self._modes
        ])

    def _build_frames(self):
        empty_frames = [None] * 500
        frames = [empty_frames.copy() for x in self.springs]
        for i in range(0, len(frames)):
            for j in range(0, len(frames[0])):
                left_y = self._position_for_mass_n_at_time_t(i, j)
                right_y = self._position_for_mass_n_at_time_t(i + 1, j)
                frames[i][j] = (left_y, right_y)
        return frames

    @property
    def springs(self):
        return self._springs

    @property
    def frames(self):
        return self._frames


def init():
    return []


def execute():

    N = 20
    modes = (1, 2, 3, 4, 5)
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
                                   frames=len(system.frames[0]),
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
        spring = system.springs[r]
        tiempo = i
        spring.set_data(spring.get_xdata(), system.frames[r][i])
    return[]


execute()
