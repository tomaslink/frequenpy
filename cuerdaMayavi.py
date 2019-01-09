import numpy as np
import mayavi.mlab as mlab
import  moviepy.editor as mpy

fig = mlab.figure(size=(500, 500), bgcolor=(1,1,1))

N = 100;

'''
while((N == 0) | (N>100)):
    if (N > 100):
        print("El límite de masas es 100")
    N = int(input("CANTIDAD DE MASAS: "));

modos = input("MODOS NORMALES separados por punto: ");
modos = list(map(int, modos.split('.')))
saveAnim = input("GUARDAR ANIMACION? y/n: ")
'''
modos = [1]


# Propiedades del sistema

K_1 = 0.5          # constante elástica inversa por unidad de longitud (N^(-1))
rho = 0.5           # densidad lineal masa (kg/m) 
L = 1.5             # largo total (metros)
a = L/(N + 1);      # distancia entre masas (metros)
m = rho*a           # masa (kg)
K = (K_1**(-1))/a   # constante elástica (N/m)
A = 0.2             # amplitud máxima (metros)
w02 = K/m;          # 

def k(p):
    return (p*np.pi)/(a*(N+1))

# Determinando el radio de las masas según la cantidad que haya

radioMasas = 0;

if (N > 50):
    radioMasas = 0.05/N
elif ((N <= 50) & (N > 1)):
    radioMasas = np.e**(7/N**2)/100
else: 
    radioMasas = 0.07;


masas = []

# cálculo de matrix tridiagonal de NxN

def tridiagonalMatrix(down, middle, up):
    M = []
    for m in range(0, N):
        row = []
        for n in range(0, N):
            if m == n:
                row.append(middle)
            elif n == (m - 1):
                row.append(down)
            elif n == (m + 1):
                row.append(up)
            else:
                row.append(0)
        
        M.append(row);
    return M;

M = tridiagonalMatrix(-1*w02, 2*w02, -1*w02)

# autovalores y autovectores 

omega2, D = np.linalg.eig(M)
sort_perm = omega2.argsort()
D = D[:, sort_perm]
D = np.transpose(D)
omega2.sort()

print(omega2)

### Funciones 



def w(p):
    return omega2[p - 1]

def normalModePforMassN(p, n, t):
    #return A*D[p-1][n-1]*np.cos(w(p)*t)
    return A*np.sin(k(p)*n*a)*np.cos(t*w(p))

def equationForMassN(modes, n, t):
    sum = np.sin(0);
    for p in modes:
        sum += normalModePforMassN(p, n, t)
    return sum;

X = []
Y = []
Z = []
for n in range(0, N):
    posicionX = [-a*((N-1)/2) + n*a]
    posicionY = [0]
    posicionZ = [0]
    X.add(posicionX)
    Y.add(posicionY)
    Z.add(posicionZ)

l = mlab.points3d(posicionX,posicionY,posicionZ, scale_factor=.05))


movementArray = np.zeros((N, 360));

for i in range (0, len(movementArray)):
    for j in range(0, 360):
        movementArray[i][j] = equationForMassN(modos, i+1, j);



def animationManage(i, masas):
    for n in range(0, len(masas)):
        animateMasa(i, masas[n], n)
    return []

def animateMasa(t, patch, n): 
    x, y = patch.center
    y = movementArray[n][t];
    patch.center = (x, y)
    return patch




@mlab.animate(delay=10)
def anim():
	t = 0
	while True:
		for n in range(0, len(masas)):
			masas[n].mlab_source.set(y = equationForMassN(modos, n+1, t))
			#mlab.view(0,0)
		yield
		t += 0.01

anim()
mlab.show()

