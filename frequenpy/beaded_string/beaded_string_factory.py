from frequenpy.beaded_string.beaded_string import (
    BeadedStringFixed, BeadedStringFree, BeadedStringMixed
)

BOUNDARY_FIXED = 0
BOUNDARY_MIXED = 1
BOUNDARY_FREE = 2


def create(number_of_beads, modes, boundary):
    if boundary == BOUNDARY_FIXED:
        return BeadedStringFixed(number_of_beads, modes)
    if boundary == BOUNDARY_MIXED:
        return BeadedStringMixed(number_of_beads, modes)
    if boundary == BOUNDARY_FREE:
        return BeadedStringFree(number_of_beads, modes)
    else:
        raise NotImplementedError(
            "{} is not a valid boundary condition".format(boundary)
        )
