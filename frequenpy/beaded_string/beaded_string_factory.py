from .beaded_string import (
    BeadedStringFixed, BeadedStringFree, BeadedStringMixed
)

BOUNDARY_FIXED = 0
BOUNDARY_FREE = 1
BOUNDARY_MIXED = 2

LONGITUDE = 1.5
AMPLITUDE = 0.5


class BeadedStringFactory(object):

    @staticmethod
    def create(boundary_condition, number_of_masses, normal_modes):
        if boundary_condition == BOUNDARY_FIXED:
            return BeadedStringFixed(
                number_of_masses, normal_modes, LONGITUDE, AMPLITUDE
            )
        if boundary_condition == BOUNDARY_MIXED:
            return BeadedStringMixed(
                number_of_masses, normal_modes, LONGITUDE, AMPLITUDE
            )
        if boundary_condition == BOUNDARY_FREE:
            return BeadedStringFree(
                number_of_masses, normal_modes, LONGITUDE, AMPLITUDE
            )
        else:
            not_valid_msg = "{} is not a valid boundary_condition"
            raise NotImplementedError(
                not_valid_msg.format(boundary_condition)
            )
