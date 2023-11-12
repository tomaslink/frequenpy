
# FrequenPy

_FrequenPy_ is a high-precision physics engine dedicated to the study of standing waves and visualization of its normal modes.

This package has educational purposes. 

## Wave theory

In this section I will briefly explain the systems available for simulation,
according predictions of wave theory.
This results have been (and can be) demonstrated experimentally.

### String loaded with with N masses oscillating transversally. 

<p align="center">
   <img src="docs/beaded_string.gif">
</p>

<div align="justify">
  
  According to wave theory, any arbitrary movement of the string
  can be decomposed into a superposition of natural modes of oscillation.
  In each natural mode **m**,
  all masses in the system oscilate at the same frequency ***f(m)***
  and pass through the equilibrium position at the same time.
  This natural modes of oscillation are called **normal modes**.

  There are as many normal modes as there are degrees of freedom (masses) in the system.
  So, a string loaded with **N** masses, will have **N** **normal modes**.
  The first will corresponde to the lowest frequency (called fundamental)
  and each next will be higher than the previous one, until we reach the last and highest frequency.
  Any movement, as strange as it may be, can be expressed as a superposition of those **N** normal modes
  (some will contribute more than others to the final movement). 

  As the number of masses gets higher and highter (***N*** ---> ***∞***),
  we approximate to the continuous system (a vibrating string - no discrete masses).
  In this simulation, you can use **N = 40** to see the effect.

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
```

Remember that for system of **N** masses there are N normal modes.
You can pass only one of them or a combination of several, e.g. "2 6 3".
The order doesn't matter. 


## TODO

- Interactive GUI to be able to play more easily with all the parameters of the system. 
- Plot each individual normal mode that is contributing to the movement.
- **Loaded String**:
  - Allow changing damping and tension as parameters.
  - Allow initial conditions to generate more arbitrary and crazy movements of the string,
  like picking the string with your mouse and realease it from some position. 


