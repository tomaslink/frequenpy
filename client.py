import logging
from frequenpy.beaded_string.beaded_string_factory import BeadedStringFactory
from frequenpy.beaded_string.animation import Animation
from settings import (
    NUMBER_OF_MASSES, NORMAL_MODES, BOUNDARY_CONDITION, SAVE_ANIMATION, SPEED
)

NUMBER_OF_FRAMES = 2000


def execute():
    try:
        beaded_string = BeadedStringFactory.create(
            BOUNDARY_CONDITION,
            NUMBER_OF_MASSES,
            NORMAL_MODES)

        animation = Animation(
            beaded_string, NUMBER_OF_FRAMES, SPEED, SAVE_ANIMATION
        )
        animation.animate()
    except Exception as e:
        logging.error(e)


def main():
    execute()


if __name__ == '__main__':
    main()
