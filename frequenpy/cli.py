import sys
sys.path.append('../')
import logging
import argparse
import traceback
from frequenpy.beaded_string.beaded_string_factory import BeadedStringFactory
from frequenpy.beaded_string.animation import Animation


NUMBER_OF_FRAMES = 2000
DEFAULT_SPEED = 1.5
DEFAULT_SAVE = False


DESCRIPTION = 'Welcome to FrequenPy!'
EPILOG = "Enjoy!"
HELP = 'Choose a system to simulate'
BEADED_STRING_PARSER_NAME = 'bs'
BEADED_STRING_HELP = 'Transverse standing wave on a beaded string'
BEADED_STRING_MASSES_HELP = 'number of masses'
BEADED_STRING_MODES_HELP = 'normal modes to combine. Ex: 1 2 3'
BEADED_STRING_BOUNDARY_HELP = '0, 1, or 2, meanining fixed, free or mixed ends'
BEADED_STRING_SAVE_HELP = 'save the animation in mp4 format'
BEADED_STRING_SPEED_HELP = 'animation speed. Can be a float number'


def execute_bs(boundary, masses, modes, speed, save_animation):
    try:
        beaded_string = BeadedStringFactory.create(boundary, masses, modes)

        animation = Animation(
            beaded_string, NUMBER_OF_FRAMES, speed, save_animation
        )
        animation.animate()
    except Exception as e:
        tpl = "An exception of type {} occured: {}"
        a = traceback.format_exc()
        logging.debug(a)
        logging.error(tpl.format(type(e), e))


def add_beaded_string_parser(subparsers):
    bs = subparsers.add_parser(
        BEADED_STRING_PARSER_NAME,
        help=BEADED_STRING_HELP
    )
    req = bs.add_argument_group("required arguments")
    req.add_argument(
        '-n',
        dest='masses',
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
        execute_bs(
            int(args.boundary),
            int(args.masses),
            list(map(int, args.modes)),
            float(args.speed) if args.speed else DEFAULT_SPEED,
            args.save)


if __name__ == '__main__':
    main()
