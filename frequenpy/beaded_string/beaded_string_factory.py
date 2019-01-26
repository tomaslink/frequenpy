from frequenpy.beaded_string.beaded_string import (
    BeadedStringFixed, BeadedStringFree, BeadedStringMixed
)

BOUNDARY_FIXED = 0
BOUNDARY_FREE = 1
BOUNDARY_MIXED = 2

LONGITUDE = 1.5
AMPLITUDE = 0.4


class BeadedStringFactory(object):

    @staticmethod
    def validate_parameters(N, modes):

        if N < 1 or N > 40:
            raise ValueError(
                "Number of masses must be an integer number between 1 and 40")

        if len(modes) > N:
            raise ValueError(
                ("The number of normal modes must be less "
                    "or equal than the number of masses!"))

        for mode in modes:
            if mode > N:
                raise ValueError(
                    "The max. normal mode for this system is {}".format(N))
            if mode < 1:
                raise ValueError("The min. normal mode is 1!")

    @staticmethod
    def create(boundary_condition, number_of_masses, normal_modes):
        BeadedStringFactory.validate_parameters(number_of_masses, normal_modes)
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
