from oscillators.beaded_string import BeadedString
from settings import (
    NUMBER_OF_MASSES, NORMAL_MODES, BOUNDARY_CONDITION, ELASTIC_CONSTANT,
    LONGITUDE, LINEAR_DENSITY, AMPLITUDE, NUMBER_OF_FRAMES, SAVE_ANIMATION,
    SPEED
)


def execute():

    beaded_string = BeadedString(
        NUMBER_OF_MASSES,
        NORMAL_MODES,
        BOUNDARY_CONDITION,
        ELASTIC_CONSTANT,
        LONGITUDE,
        LINEAR_DENSITY,
        AMPLITUDE,
        NUMBER_OF_FRAMES,
        SAVE_ANIMATION,
        SPEED)

    beaded_string.animate()


def main():
    execute()


if __name__ == '__main__':
    main()
