import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .settings import ANIMATIONS_FOLDER
from os import path, makedirs


class BeadedString(object):

    FIXED = 0
    FREE = 1
    MIXED = 2

    def __init__(
        self, number_of_masses, normal_modes, boundary_condition,
        longitude, amplitude, number_of_frames, save_animation, speed
    ):
        self._number_of_masses = number_of_masses
        self._normal_modes = normal_modes
        self._boundary_condition = boundary_condition
        self._longitude = longitude
        self._amplitude = amplitude
        self._number_of_frames = number_of_frames
        self._save_animation = save_animation
        self._separation = longitude / (number_of_masses + 1)
        self._speed = speed
        self._prepare()

    def _prepare(self):
        self._tridiagonal_matrix = self._tridiagonal_matrix()
        self._omega_squared = self._omega_squared()
        self._beaded_string = self._build_beaded_string()
        self._frames = self._build_frames()
        self._figure = self._build_figure()

    def _tridiagonal_matrix(self):
        low, mid, upp = (-1, 2, -1)
        N = self._number_of_masses
        A = np.eye(N, N, k=-1) * low + \
            np.eye(N, N) * mid + \
            np.eye(N, N, k=1) * upp
        A[A == 0.] = 0.
        return A

    def _omega_squared(self):
        w2, _ = np.linalg.eig(self._tridiagonal_matrix)
        w2.sort()
        return w2

    def _build_beaded_string(self):
        X, Y = self._beads_coordinates()
        return plt.Line2D(
            X, Y,
            marker='o',
            lw=0.3,
            markersize=5,
            markerfacecolor='white',
            color='white',
            markevery=slice(1, self._number_of_masses + 1, 1)
        )

    def _beads_coordinates(self):
        N = range(0, self._number_of_masses + 2)
        X = np.array([-self._longitude / 2 + n * self._separation for n in N])
        Y = np.array([0 for n in N])
        return (X, Y)

    def _build_frames(self):
        X_0 = self._beaded_string.get_xdata()
        masses = range(0, len(X_0))
        frames = range(0, self._number_of_frames)
        return np.array([
            (
                X_0,
                np.array([
                    self._position_for_mass_n_at_time_t(n, t)
                    for n in masses
                ])
            )
            for t in frames
        ])

    def _build_figure(self):
        fig = plt.figure(figsize=(10, 5), facecolor='black')
        fig.set_dpi(100)
        ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1), frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.add_line(self._left_wall())
        ax.add_line(self._ritgh_wall())
        ax.add_line(self._beaded_string)
        return fig

    def _wall(self, x_coordinates):
        return plt.Line2D(
            x_coordinates,
            (-0.8, 0.8),
            lw=0.5,
            color='white'
        )

    def _left_wall(self):
        return self._wall((-self._longitude / 2, -self._longitude / 2))

    def _ritgh_wall(self):
        return self._wall((self._longitude / 2, self._longitude / 2))

    def _omega(self, p):
        return np.sqrt(self._omega_squared[p - 1])

    def _normal_mode_p_for_mass_n(self, p, n):
        if (
            self._boundary_condition == BeadedString.FIXED or
            self._boundary_condition == BeadedString.FREE
        ):
            return (p * n * np.pi) / (self._number_of_masses + 1)
        else:
            p = p - 1
            return ((p + 1 / 2) * n * np.pi) / (self._number_of_masses + 1)

    def _position_for_mass_n_at_time_t(self, n, t):
        if (
            self._boundary_condition == BeadedString.FIXED or
            self._boundary_condition == BeadedString.MIXED
        ):
            phi = 0
        else:
            phi = np.pi / 2
        return sum([
            self._amplitude *
            np.sin(self._normal_mode_p_for_mass_n(p, n) + phi) *
            np.cos(np.radians(self._omega(p) * t * self._speed))
            for p
            in self._normal_modes
        ])

    def _update(self, frame_number):
        self._beaded_string.set_data(self._frames[frame_number])
        return self._beaded_string,

    def _create_directory(self, directory):
        if not path.exists(directory):
            makedirs(directory)

    def animate(self):
        anim = animation.FuncAnimation(
            self._figure,
            self._update,
            frames=self._number_of_frames,
            interval=5,
            blit=True,
            repeat=True)

        if (self._save_animation == 1):
            print('Saving animation...this could take a while...')
            name = "{}masses_{}modes.mp4".format(
                self._number_of_masses, str(self._normal_modes)
            )
            self._create_directory(ANIMATIONS_FOLDER)
            full_path = path.join(ANIMATIONS_FOLDER, name)
            anim.save(full_path)

        plt.show()
