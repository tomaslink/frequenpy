from .beaded_string import (
    BeadedStringFixed, BeadedStringFree, BeadedStringMixed
)

BOUNDARY_FIXED = 0
BOUNDARY_FREE = 1
BOUNDARY_MIXED = 2


class BeadedStringFactory(object):

    @staticmethod
    def create(
        boundary_condition,
        number_of_masses,
        normal_modes,
        longitude,
        amplitude,
        speed
    ):
        if boundary_condition == BOUNDARY_FIXED:
            return BeadedStringFixed(
                number_of_masses, normal_modes, longitude, amplitude, speed
            )
        if boundary_condition == BOUNDARY_MIXED:
            return BeadedStringMixed(
                number_of_masses, normal_modes, longitude, amplitude, speed
            )
        if boundary_condition == BOUNDARY_FREE:
            return BeadedStringFree(
                number_of_masses, normal_modes, longitude, amplitude, speed
            )
        else:
            not_valid_msg = "{} is not a valid boundary_condition"
            raise NotImplementedError(
                not_valid_msg.format(boundary_condition)
            )
