import numpy as np
from abc import ABC, abstractmethod


LONGITUDE = 1
TENSION = 0.5
MASS = 0.1

AMPLITUDE = 0.5
THETA = 0


class LoadedString(ABC):
    CONTINUOUS_LIMIT = 30

    def __init__(self, N, modes):
        self.N = N
        self._modes = modes
        self._masses = range(0, N + 2)
        self._a = LONGITUDE / (N + 1)
        self._omega = self._omega()

        self.rest_position = self._get_rest_position()

    def position_at_time_t(self, t):
        X, _ = self.rest_position
        Y = self._y_position_at_time_t(t)

        return (X, Y)

    def _y_position_at_time_t(self, t):
        y_pos = [sum([
            self._standing_wave_equation(
                A=AMPLITUDE,
                k=self._wavenumber(p),
                n=n,
                a=self._a,
                phi=self._phi,
                omega=self._omega[p],
                t=t,
                theta=THETA
            )
            for p in self._modes])
            for n in self._masses]

        return y_pos

    def apply_speed(self, speed):
        self._omega = {p: o * speed for p, o in self._omega.items()}

    @property
    def modes(self):
        return "-".join([str(m) for m in self._modes])

    def _omega(self):
        return {
            p: 2 * np.sqrt(TENSION / MASS * self._a) * np.sin(self._wavenumber(p) * self._a / 2)
            for p in self._modes
        }

    def _get_rest_position(self):
        N = range(0, self.N + 2)
        X = np.array([-LONGITUDE / 2 + n * self._a for n in N])
        Y = np.array([0 for n in N])

        return (X, Y)

    def _standing_wave_equation(self, A, k, n, a, phi, omega, t, theta):
        return A * np.sin(k * n * a + phi) * np.cos((omega * t + theta))

    @abstractmethod
    def _wavenumber(self, p):
        pass


class LoadedStringFixed(LoadedString):
    def __init__(self, N, modes):
        super().__init__(N, modes)
        self._phi = 0

    def _wavenumber(self, p):
        return (p * np.pi) / ((self.N + 1) * self._a)


class LoadedStringMixed(LoadedString):
    def __init__(self, N, modes):
        super().__init__(N, modes)
        self._phi = 0

    def _wavenumber(self, p):
        return ((p - 1 / 2) * np.pi) / ((self.N + 1) * self._a)


class LoadedStringFree(LoadedString):
    def __init__(self, N, modes):
        super().__init__(N, modes)
        self._phi = np.pi / 2

    def _wavenumber(self, p):
        return (p * np.pi) / ((self.N + 1) * self._a)
