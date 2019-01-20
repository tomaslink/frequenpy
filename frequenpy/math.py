import numpy as np


def tridiagonal_matrix(low, mid, upp, size):
    M = np.eye(size, size, k=-1) * low + \
        np.eye(size, size) * mid + \
        np.eye(size, size, k=1) * upp
    M[M == 0.] = 0.
    return M


def sorted_eigenvalues(M):
    w2, _ = np.linalg.eig(M)
    w2.sort()
    return w2


def standing_wave_equation(A_p, k_p, n, a, phi, w, t, theta_p):
    return A_p * np.sin(k_p * n * a + phi) * np.cos((w * t + theta_p))
