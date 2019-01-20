import numpy as np
from .. import math


class BeadedString(object):

    def __init__(
        self, number_of_masses, normal_modes, longitude, amplitude, speed
    ):
        self.number_of_masses = number_of_masses
        self.normal_modes = normal_modes
        self.longitude = longitude
        self._amplitude = amplitude
        self._separation = longitude / (number_of_masses + 1)
        self._speed = speed
        self._frequencies = self._frequencies()
        self._phi = self._phi()
        self._theta = 0

    def rest_positions(self):
        N = range(0, self.number_of_masses + 2)
        X = np.array([-self.longitude / 2 + n * self._separation for n in N])
        Y = np.array([0 for n in N])
        return (X, Y)

    def y_position_for_mass_n_at_time_t(self, n, t):
        return sum([
            math.standing_wave_equation(
                self._amplitude,
                self._wavenumber_for_mode_p_and_mass_n(p, n),
                n,
                self._separation,
                self._phi,
                self._frequencies[p],
                t,
                self._theta
            )
            for p
            in self.normal_modes
        ])

    def _tridiagonal_matrix(self):
        return math.tridiagonal_matrix(-1, 2, -1, self.number_of_masses)

    def _frequencies(self):
        return np.radians(
            np.sqrt(math.sorted_eigenvalues(self._tridiagonal_matrix())))

    def _phi(self):
        raise NotImplementedError("Implement in sublass")

    def _wavenumber_for_mode_p_and_mass_n(self, p, n):
        raise NotImplementedError("Implement in sublass")


class BeadedStringFixed(BeadedString):
    def _phi(self):
        return 0

    def _wavenumber_for_mode_p_and_mass_n(self, p, n):
        return (p * np.pi) / \
            ((self.number_of_masses + 1) * self._separation)


class BeadedStringFree(BeadedString):
    def _phi(self):
        return np.pi / 2

    def _wavenumber_for_mode_p_and_mass_n(self, p, n):
        return (p * np.pi) / \
            ((self.number_of_masses + 1) * self._separation)


class BeadedStringMixed(BeadedString):
    def _phi(self):
        return 0

    def _wavenumber_for_mode_p_and_mass_n(self, p, n):
        p = p - 1
        return ((p + 1 / 2) * np.pi) / \
            ((self.number_of_masses + 1) + self._separation)
