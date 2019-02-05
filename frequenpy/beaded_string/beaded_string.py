import numpy as np

LONGITUDE = 1.5
AMPLITUDE = 0.6
THETA = 0


class BeadedString(object):

    def __init__(self, number_of_beads, modes):
        self._number_of_beads = number_of_beads
        self._modes = [p - 1 for p in modes]

        self._beads = range(0, number_of_beads)
        self._spacing = LONGITUDE / (number_of_beads + 1)
        self._rest_position = self.get_rest_position()
        self._omega = self._omega()

    def get_rest_position(self):
        N = range(0, self.number_of_beads + 2)
        X = np.array([-LONGITUDE / 2 + n * self._spacing for n in N])
        Y = np.array([0 for n in N])
        return (X, Y)

    def position_at_time_t(self, t):
        X, _ = self._rest_position
        Y = self._y_position_at_time_t(t)
        return (X, Y)

    def apply_speed(self, speed):
        self._omega = self._omega * speed

    @property
    def modes(self):
        return self._modes

    @property
    def number_of_beads(self):
        return self._number_of_beads

    @property
    def rest_position(self):
        return self._rest_position

    def _y_position_at_time_t(self, t):
        y_pos = [sum([
            self._standing_wave_equation(
                AMPLITUDE,
                self._wavenumber(p + 1),
                n + 1,
                self._spacing,
                self._phi,
                self._omega[p],
                t,
                THETA)
            for p in self._modes])
            for n in self._beads]
        return self._apply_boundary_condition(y_pos)

    def _w(self, k):
        return np.sin(k * self._spacing / 2)

    def _omega(self):
        w = np.array([
            self._w(self._wavenumber(p + 1))
            for p in self._beads
        ])
        return w / w[0] / 60

    def _standing_wave_equation(self, A, k, n, a, phi, omega, t, theta):
        return A * np.sin(k * n * a + phi) * np.cos((omega * t + theta))


class BeadedStringFixed(BeadedString):

    def __init__(self, number_of_beads, modes):
        super().__init__(number_of_beads, modes)
        self._phi = 0

    def _apply_boundary_condition(self, y_pos):
        y_pos = np.insert(y_pos, 0, 0)
        y_pos = np.append(y_pos, 0)
        return y_pos

    def _wavenumber(self, p):
        return (p * np.pi) / ((self._number_of_beads + 1) * self._spacing)


class BeadedStringMixed(BeadedString):

    def __init__(self, number_of_beads, modes):
        super().__init__(number_of_beads, modes)
        self._phi = 0

    def _apply_boundary_condition(self, y_pos):
        y_pos = np.insert(y_pos, 0, 0)
        y_pos = np.append(y_pos, y_pos[-1])
        return y_pos

    def _wavenumber(self, p):
        p = p - 1
        return ((p + 1 / 2) * np.pi) / \
            ((self.number_of_beads + 1) * self._spacing)


class BeadedStringFree(BeadedString):

    def __init__(self, number_of_beads, modes):
        super().__init__(number_of_beads, modes)
        self._phi = np.pi / 2

    def _apply_boundary_condition(self, y_pos):
        y_pos = np.insert(y_pos, 0, y_pos[0])
        y_pos = np.append(y_pos, y_pos[-1])
        return y_pos

    def _wavenumber(self, p):
        return (p * np.pi) / ((self._number_of_beads + 1) * self._spacing)
