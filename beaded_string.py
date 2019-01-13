import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class BeadedString(object):

    def __init__(
        self, number_of_masses, normal_modes, boundary, elastic_constant,
        longitude, rho, amplitude, n_frames, save_anim
    ):
        self._number_of_masses = number_of_masses
        self._normal_modes = normal_modes
        self._boundary = boundary
        self._elastic_constant = elastic_constant
        self._longitude = longitude
        self._rho = rho
        self._amplitude = amplitude
        self._n_frames = n_frames
        self._save_anim = save_anim

        self._separation = longitude / (number_of_masses + 1)
        self._tridiagonal_matrix = self._tridiagonal_matrix()
        self._omega_squared = self._omega_squared()
        self._beaded_string = self._build_beaded_string()
        self._frames = self._build_frames(n_frames)
        self._figure = self._build_figure()

    def _resolve_marker_size(self):
        N = self._number_of_masses
        if (N > 50):
            marker_size = 0
        elif (N > 30):
            marker_size = 2
        elif (N > 15):
            marker_size = 4
        else:
            marker_size = 8
        return marker_size

    def _beads_coordinates(self):
        N = range(0, self._number_of_masses + 2)
        X = np.array([-self._longitude / 2 + n * self._separation for n in N])
        Y = np.array([0 for n in N])
        return (X, Y)

    def _build_beaded_string(self):
        X, Y = self._beads_coordinates()
        return plt.Line2D(
            X, Y, marker='o', lw=2, markersize=self._resolve_marker_size()
        )

    def _build_figure(self):
        L = self._longitude
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
        ax.add_line(self._beaded_string)
        return fig

    def _omega_squared(self):
        M = self._tridiagonal_matrix
        w2, _ = np.linalg.eig(M)
        w2.sort()
        return w2

    def _tridiagonal_matrix(self):
        m = self._rho * self._separation
        K = (self._elastic_constant / self._separation)
        w0_2 = K / m
        low, mid, upp = (-1 * w0_2, 2 * w0_2, -1 * w0_2)
        N = self._number_of_masses
        A = np.eye(N, N, k=-1) * low + \
            np.eye(N, N) * mid + \
            np.eye(N, N, k=1) * upp
        A[A == 0.] = 0.
        return A

    def _omega(self, p):
        return np.sqrt(self._omega_squared[p - 1])

    def _normal_mode_p_for_mass_n(self, p, n):
        return (p * n * np.pi) / (self._number_of_masses + 1)

    def _position_for_mass_n_at_time_t(self, n, t):
        A = self._amplitude
        return sum([
            A *
            np.sin(self._normal_mode_p_for_mass_n(p, n)) *
            np.cos(np.radians(self._omega(p) * t))
            for p
            in self._normal_modes
        ])

    def _build_frames(self, number):
        X_0 = self._beaded_string.get_xdata()
        list_masses = range(0, len(X_0))
        list_frames = range(0, len([None] * number))
        return [(
            X_0,
            tuple([
                self._position_for_mass_n_at_time_t(n, t)
                for n in list_masses
            ]))
            for t in list_frames
        ]

    def _update(self, frame_number):
        X, Y = self._frames[frame_number]
        self._beaded_string.set_data(X, Y)
        return self._beaded_string,

    def animate(self):
        anim = animation.FuncAnimation(
            self._figure,
            self._update,
            frames=self._n_frames,
            interval=30,
            blit=True,
            repeat=True)
        if (self._save_anim == 1):
            print("GUARDANDO ANIMACION...ESTO PUEDE LLEVAR UN RATO")
            anim.save('test' + '.mp4')
        plt.show()
