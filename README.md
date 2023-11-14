
<h1 align="center" style="border-bottom: none;"> FrequenPy </h1>

<p align="center">
  <a>
    <img alt="Coverage" src="https://codecov.io/gh/tomaslink/frequenpy/branch/master/graph/badge.svg">
  </a>
</p>

**frequenpy** is a high-precision physics engine dedicated to the study and visualization of standing waves.

## Wave theory

In this section I will briefly explain the systems available for simulation,
according predictions of wave theory.
This results have been (and can be) demonstrated experimentally.

### String loaded with with N masses oscillating transversally. 

<p align="center">
   <img src="docs/beaded_string.gif">
</p>

<div align="justify">
  
  A flexible elastic string with tension **T** is loaded with **N** identical particles,
  each of mass **m**, equally spaced a distance **a** apart.
  Let us hold the string fixed at two points,
  one at a distance **a** to the left of the first particle
  and the other at a distance **a** to the right of the Nth particle.

  According to the theory, the movement of each of the masses in the vertical direction
  can be decomposed into a superposition of **N** **normal modes** modes of oscillation.
  That way, the $y$ position of the particle **n** as a function of time is
  ```math
    y_n(t) = \sum_{p=1}^N A_p \sin(k_p n a) \cos(\omega_p t + \theta_p).
  ```
  Where $A_p$ and $\theta_p$ depend on the initial conditions,
  $k_p$ will depend on the boundary conditions and $\omega_p$ will have the form
  ```math
    \omega_p = 2 \omega_0 \sin\left(\frac{p \pi}{2(N + 1)}\right)
    \qquad,
    \qquad
    \omega_0 = \sqrt{\frac{T}{ma}}.
  ```
  
  There are as many normal modes as there are degrees of freedom (masses) in the system.
  In each natural mode **p**,
  all masses in the system oscilate at the same frequency $\omega_p$
  and pass through the equilibrium position at the same time.
  The first mode, **p=1**, corresponds to the lowest frequency (called fundamental)
  and each subsequent mode will have a frequency higher than the previous one.
  Any movement of the string, as strange as it may be,
  can be expressed as a superposition of those **N** normal modes
  (some will contribute more than others to the final movement). 

  As the number of masses gets higher and highter ($N \rightarrow \infty$),
  we approximate to the continuous system (a vibrating string - no discrete masses).
  In this simulation, you can use **N = 30** to see a continuous effect.

</div>

## Installation

To install FrequenPy, just run:

```
pip install frequenpy
```

## Usage

Once installed, just run:

```
frequenpy
```

This will prompt the following help:
```bash
(.venv) $ frequenpy
usage: FrequenPy [-h] {loaded_string} ...

Welcome to FrequenPy! High-precision physics engine dedicated to the study of standing waves.

positional arguments:
  {loaded_string}  Choose a system to simulate
    loaded_string  Transverse oscillations on a string loaded with masses.

options:
  -h, --help       show this help message and exit

Enjoy!

```

If you pass **loaded_string** as an argument:

```bash
(.venv) $ frequenpy beaded_string
usage: FrequenPy beaded_string [-h] --masses  [--modes  [...]] [--boundary BOUNDARY] [--speed SPEED] [--save]

Transverse oscillations on a string loaded with masses.

options:
  -h, --help           show this help message and exit

required arguments:
  --masses             Number of masses.

optional arguments:
  --modes  [ ...]      Normal modes to combine. Ex: "1 2 3" (default: [1]).
  --boundary BOUNDARY  Boundary conditions: 0 (fixed), 1 (free), or 2 (mixed) (default: 0).
  --speed SPEED        Animation speed. Can be a float number (default: 1).
  --save               Save the animation in mp4 format (default: False).

Example: frequenpy loaded_string --masses 3 --modes 1 2 3 --speed 0.1 --boundary 0
```

Remember that for system of **N** masses there are **N** normal modes.
You can pass only one of them or a combination of several, e.g. "2 6 3".
The order doesn't matter. 


## TODO

- Interactive GUI to be able to play more easily with all the parameters of the system. 
- Plot each individual normal mode that is contributing to the movement.
- **Loaded String**:
  - Allow changing damping and tension as parameters.
  - Allow initial conditions to generate more arbitrary and crazy movements of the string,
  like picking the string with your mouse and realease it from some position. 


