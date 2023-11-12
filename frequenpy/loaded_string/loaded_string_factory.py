from frequenpy.loaded_string.loaded_string import (
    LoadedStringFixed, LoadedStringFree, LoadedStringMixed
)

BOUNDARY_FIXED = 0
BOUNDARY_MIXED = 1
BOUNDARY_FREE = 2

VALID_NUMBER_OF_MASSES = [1, 2, 3, 4, 5, 30]


def create(N, modes, boundary):
    validate_parameters(N, modes)
    if boundary == BOUNDARY_FIXED:
        return LoadedStringFixed(N, modes)
    if boundary == BOUNDARY_MIXED:
        return LoadedStringMixed(N, modes)
    if boundary == BOUNDARY_FREE:
        return LoadedStringFree(N, modes)
    else:
        raise ValueError(
            "{} is not a valid boundary condition".format(boundary)
        )


def validate_parameters(N, modes):
    if N not in VALID_NUMBER_OF_MASSES:
        raise ValueError(f'Number of masses must be one of: {VALID_NUMBER_OF_MASSES}')

    if len(modes) < 1 or len(modes) > N:
        raise ValueError(
            'The number of normal modes must be an integer between 1 and N!')

    for mode in modes:
        if mode > N:
            raise ValueError(
                'The max. normal mode for this system is {}!'.format(N))

        if mode < 1:
            raise ValueError('The min. normal mode is 1!')
