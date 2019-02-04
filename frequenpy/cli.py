import logging
import argparse
import traceback
import frequenpy.beaded_string.beaded_string_factory as factory
from frequenpy.beaded_string.animation import Animation
import sys


NUMBER_OF_FRAMES = 2000
DEFAULT_SPEED = 1.5
DEFAULT_SAVE = False


DESCRIPTION = 'Welcome to FrequenPy!'
EPILOG = "Enjoy!"
HELP = 'Choose a system to simulate'
BEADED_STRING_PARSER_NAME = 'bs'
BEADED_STRING_HELP = 'Transverse oscillations on a beaded string'
BEADED_STRING_MASSES_HELP = 'number of beads'
BEADED_STRING_MODES_HELP = 'normal modes to combine. Ex: 1 2 3'
BEADED_STRING_BOUNDARY_HELP = '0, 1, or 2, meanining fixed, free or mixed ends'
BEADED_STRING_SAVE_HELP = 'save the animation in mp4 format'
BEADED_STRING_SPEED_HELP = 'animation speed. Can be a float number'


def execute_bs(beads, modes, boundary, speed, save_animation):
    try:
        validate_bs_parameters(beads, modes)
        beaded_string = factory.create(beads, modes, boundary)

        animation = Animation(
            beaded_string, NUMBER_OF_FRAMES, speed, save_animation
        )
        animation.animate()
    except Exception as e:
        a = traceback.format_exc()
        logging.debug(a)
        logging.error(e)


def add_beaded_string_parser(subparsers):
    bs = subparsers.add_parser(
        BEADED_STRING_PARSER_NAME,
        help=BEADED_STRING_HELP
    )
    req = bs.add_argument_group("required arguments")
    req.add_argument(
        '-n',
        dest='beads',
        required=True,
        help=BEADED_STRING_MASSES_HELP
    )
    req.add_argument(
        '-m',
        dest='modes',
        required=True,
        nargs='+',
        help=BEADED_STRING_MODES_HELP
    )
    req.add_argument(
        '-b',
        dest='boundary',
        required=True,
        help=BEADED_STRING_BOUNDARY_HELP
    )
    opt = bs.add_argument_group("more optional arguments")
    opt.add_argument(
        '-s',
        dest='speed',
        required=False,
        help=BEADED_STRING_SPEED_HELP
    )
    opt.add_argument(
        '--save',
        action='store_true',
        help=BEADED_STRING_SAVE_HELP
    )
    return bs


def validate_bs_parameters(N, modes):

    if N < 1 or N > 40:
        raise ValueError(
            "Number of beads must be an integer between 1 and 40")

    if len(modes) < 1 or len(modes) > N:
        raise ValueError(
            "The number of normal modes must be an integer between"
            " 1 the number of beads!")

    for mode in modes:
        if mode > N:
            raise ValueError(
                "The max. normal mode for this system is {}!".format(N))
        if mode < 1:
            raise ValueError("The min. normal mode is 1!")


def validate_args_length(parser, subparsers):
    if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == BEADED_STRING_PARSER_NAME:
            subparsers.choices[BEADED_STRING_PARSER_NAME].print_help()
        sys.exit(1)


def main():

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    subparsers = parser.add_subparsers(help=HELP, dest='system')
    add_beaded_string_parser(subparsers)
    validate_args_length(parser, subparsers)

    args = parser.parse_args()

    if args.system == BEADED_STRING_PARSER_NAME:
        beads, modes = int(args.beads), list(map(int, args.modes))
        execute_bs(
            beads,
            modes,
            int(args.boundary),
            float(args.speed) if args.speed else DEFAULT_SPEED,
            args.save)


if __name__ == '__main__':
    main()
