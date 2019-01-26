import logging
import argparse
import sys
import traceback
from frequenpy.beaded_string.beaded_string_factory import BeadedStringFactory
from frequenpy.beaded_string.animation import Animation

NUMBER_OF_FRAMES = 2000
DEFAULT_SPEED = 1
DEFAULT_SAVE = False

HELP = 'Choose a system to simulate'
BS_HELP = 'Transverse standing wave on a beaded string'
BS_N_HELP = 'number of masses'
BS_M_HELP = 'normal modes to combine'
BS_B_HELP = '0, 1, or 2, meanining fixed, free or mixed ends'
BS_R_HELP = 'save the animation in mp4 format'
BS_S_HELP = 'animation speed'


def execute_bs(boundary, masses, modes, speed, save_animation):
    try:
        beaded_string = BeadedStringFactory.create(boundary, masses, modes)

        animation = Animation(
            beaded_string, NUMBER_OF_FRAMES, speed, save_animation
        )
        animation.animate()
    except Exception as e:
        traceback.print_exc()
        logging.error(e)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help=HELP, dest='system')

    bs = subparsers.add_parser('bs', help=BS_HELP)
    bs.add_argument('-n', '--masses', required=True, help=BS_N_HELP)
    bs.add_argument('-m', '--modes', required=True, nargs='+', help=BS_M_HELP)
    bs.add_argument('-b', '--boundary', required=True, help=BS_B_HELP)
    bs.add_argument('-s', '--speed', required=False, help=BS_S_HELP)
    bs.add_argument('--save', required=False, action='store_true', help=BS_R_HELP)

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    print(list(map(int, args.modes)))
    if args.system == 'bs':
        execute_bs(
            int(args.boundary),
            int(args.masses),
            list(map(int, args.modes)),
            float(args.speed) if args.speed else DEFAULT_SPEED,
            args.save)


if __name__ == '__main__':
    main()
