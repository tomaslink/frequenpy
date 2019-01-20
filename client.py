from frequenpy.beaded_string.beaded_string import BeadedString
from frequenpy.beaded_string.animation import Animation
from settings import (
    NUMBER_OF_MASSES, NORMAL_MODES, BOUNDARY_CONDITION, LONGITUDE,
    AMPLITUDE, NUMBER_OF_FRAMES, SAVE_ANIMATION, SPEED
)


def execute():

    beaded_string = BeadedString(
        NUMBER_OF_MASSES,
        NORMAL_MODES,
        BOUNDARY_CONDITION,
        LONGITUDE,
        AMPLITUDE,
        SPEED)

    animation = Animation(beaded_string, NUMBER_OF_FRAMES, SAVE_ANIMATION)
    animation.animate()


def main():
    execute()


if __name__ == '__main__':
    main()
