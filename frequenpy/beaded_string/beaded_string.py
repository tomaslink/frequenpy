import numpy as np

BOUNDARY_FIXED = 0
BOUNDARY_FREE = 1
BOUNDARY_MIXED = 2


class BeadedString(object):

    def __init__(
        self, number_of_masses, normal_modes, boundary_condition,
        longitude, amplitude, speed
    ):
        self.number_of_masses = number_of_masses
        self.normal_modes = normal_modes
        self.longitude = longitude
        self._boundary_condition = boundary_condition
        self._amplitude = amplitude
        self._separation = longitude / (number_of_masses + 1)
        self._speed = speed
        self._omega_squared = self._omega_squared()

    def _tridiagonal_matrix(self):
        low, mid, upp = (-1, 2, -1)
        N = self.number_of_masses
        A = np.eye(N, N, k=-1) * low + \
            np.eye(N, N) * mid + \
            np.eye(N, N, k=1) * upp
        A[A == 0.] = 0.
        return A

    def _omega_squared(self):
        w2, _ = np.linalg.eig(self._tridiagonal_matrix())
        w2.sort()
        return w2

    def initial_positions(self):
        N = range(0, self.number_of_masses + 2)
        X = np.array([-self.longitude / 2 + n * self._separation for n in N])
        Y = np.array([0 for n in N])
        return (X, Y)

    def _omega(self, p):
        return np.sqrt(self._omega_squared[p - 1])

    def _normal_mode_p_for_mass_n(self, p, n):
        if (
            self._boundary_condition == BOUNDARY_FIXED or
            self._boundary_condition == BOUNDARY_FREE
        ):
            return (p * n * np.pi) / (self.number_of_masses + 1)
        else:
            p = p - 1
            return ((p + 1 / 2) * n * np.pi) / (self.number_of_masses + 1)

    def position_for_mass_n_at_time_t(self, n, t):
        if (
            self._boundary_condition == BOUNDARY_FIXED or
            self._boundary_condition == BOUNDARY_MIXED
        ):
            phi = 0
        else:
            phi = np.pi / 2
        return sum([
            self._amplitude *
            np.sin(self._normal_mode_p_for_mass_n(p, n) + phi) *
            np.cos(np.radians(self._omega(p) * t * self._speed))
            for p
            in self.normal_modes
        ])
