
# FrequenPy

_FrequenPy_ is a high-precision physics engine dedicated to the study of standing waves and visualization of its normal modes.

<p align="center">
	 <img src="docs/beaded_string.gif">
</p>

## Table of Contents

- [Motivation](#motivation)
- [Theoretical background](#theoretical-background)
- [Requirements](#requirements)
- [Documentation](#documentation)
- [Usage](#usage)
	* [Installation](#installation)
	* [Execution](#execution)
- [Ideas](#ideas)

## Theoretical background

I will improve this section later by adding a minimal mathematical derivations and important equations to understad better the systems in question. 

For now, the only system available to play with is a beaded string loaded with N masses (N degrees of freedom), oscillating transversally. The theory says that any arbitrary movement of the string can be decomposed into a superposition of natural modes of oscillation, that have the particularity that when the system is oscillating in one of this natural modes, all masses in the system move at the same frequency and pass through the equilibrium position at the same time. This natural modes of oscillation are called normal modes. There are as many normal modes as there are degrees of freedom in the system. So, a string loeaded with 10 masses, will have 10 natural frequencies, the first being the lowest (called fundamental) and each next higher than the previous one, until reaching the last and highest frequency. Any movement, as strange as it may be, can be expressed as a superposition of those 10 normal modes (some will contribute more than others to the final movement). 

As the number of masses gets higher (Ideally, N --> inf), we approximate to the continuous system, that is, a vibrating string (no discrete masses). With N = 40 you can see the effect. 

To be completed. 

## Requirements

Frequenpy was tested with python3.7.2 in ArchLinux. 

## Documentation

To be completed. 

## Usage

### Installation

To install FrequenPy, just run:

```
pip3 install frequenpy
```


### Execution

Once installed, just run:

```
frequenpy
```

This will prompt the following help output:

```bash
usage: frequenpy.py [-h] {bs} ...

positional arguments:
  {bs}        Choose a system to simulate
    bs        Transverse standing wave on a beaded string

optional arguments:
  -h, --help  show this help message and exit
```

and if you pass 'bs' as an argument:

```
python3 frequenpy.py bs
```

You'll get the help for running that particular system:

```bash
usage: frequenpy.py bs [-h] -n MASSES -m MODES [MODES ...] -b BOUNDARY
                       [-s SPEED] [--save]

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -n MASSES             number of masses
  -m MODES [MODES ...]  normal modes to combine. Ex: 1 2 3
  -b BOUNDARY           0, 1, or 2, meanining fixed, free or mixed ends

more optional arguments:
  -s SPEED              animation speed. Can be a float number
  --save                save the animation in mp4 format
```


You can play with the parameters of the system to visualize different situations. 
- Remember there is one normal mode per mass in the system, i.e: 1, 2, 3....N. You can pass only one of them, or a combination of several normal modes. The order doesn't matter. 
- Boundary condition can be 0, 1, or 2, meaning fixed ends, free ends, or mixed ends (left fixed and right free). 
- The speed parameter is important because for very high frequencies, which can appear if the number of masses is high, the appreciation of the movement can be difficult, and it is convenient to reduce the speed of the animation.
- Optionally, you can save the animation in mp4 format. 


## Ideas

-At this moment i'm working on an interactive GUI-client to be able to play more easily with all the parameters of the system. 

-Add one plot for each individual normal mode that is contributing to the movement. 

-Introduce damping and tension of the string as parameters to play with.

-Add definition of initial conditions to generate more arbitrary and crazy movements of the string, like picking the string with your mouse and realease it from some position. 

-Add other systems. 


