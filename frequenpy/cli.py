import sys
import logging

import argparse

from frequenpy.loaded_string.animation import LoadedStringAnimation, DEFAULT_SPEED

from frequenpy.constants import APP_DESCRIPTION, APP_NAME

logger = logging.getLogger(__name__)


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


GREETING = F'Welcome to {APP_NAME}!\n {APP_DESCRIPTION}'
APP_EPILOG = 'Enjoy!'

BEADED_STRING = 'loaded_string'
AVAILABLE_SYSTEMS = [BEADED_STRING]

HELP_DEFAULT = '(default: %(default)s)'

HELP_LS = 'Transverse oscillations on a string loaded with masses.'
HELP_LS_MASSES = 'Number of masses.'
HELP_LS_MODES = f'Normal modes to combine. Ex: "1 2 3" {HELP_DEFAULT}.'
HELP_LS_BOUNDARY = f'Boundary conditions: 0 (fixed), 1 (free), or 2 (mixed) {HELP_DEFAULT}.'
HELP_LS_SAVE = f'Save the animation in mp4 format {HELP_DEFAULT}.'
HELP_LS_SPEED = f'Animation speed. Can be a float number {HELP_DEFAULT}.'

EXAMPLE_LS = "frequenpy loaded_string --masses 3 --modes 1 2 3 --speed 0.1 --boundary 0"
EPILOG_LS = "Example: {}".format(EXAMPLE_LS)


def setup_logger(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format=LOG_FORMAT)

    # Hide logging from external libraries
    external_libs = ['matplotlib', 'PIL']
    for lib in external_libs:
        logging.getLogger(lib).setLevel(logging.ERROR)


def add_loaded_string_parser(subparsers):
    p = subparsers.add_parser(BEADED_STRING, description=HELP_LS, help=HELP_LS, epilog=EPILOG_LS)

    r = p.add_argument_group('required arguments')
    r.add_argument('--masses', type=int, required=True, default=3, metavar='', help=HELP_LS_MASSES)

    o = p.add_argument_group('optional arguments')
    o.add_argument('--modes', type=int, default=[1], metavar='', nargs='+', help=HELP_LS_MODES)
    o.add_argument('--boundary', type=int, default=0, help=HELP_LS_BOUNDARY)
    o.add_argument('--speed', type=float, default=DEFAULT_SPEED, help=HELP_LS_SPEED)
    o.add_argument('--save', action='store_true', help=HELP_LS_SAVE)


def parse_args(parser, subparsers):
    help_arg = '--help'
    if len(sys.argv) < 2:
        return [help_arg]

    if len(sys.argv) == 2:
        system = sys.argv[1]
        if system not in AVAILABLE_SYSTEMS:
            raise ValueError(f'System {system} is not a valid option.')

        return [system, help_arg]

    return sys.argv[1:]


def main():
    parser = argparse.ArgumentParser(prog=APP_NAME, description=GREETING, epilog=APP_EPILOG)
    subparsers = parser.add_subparsers(dest='system', help='Choose a system to simulate')
    add_loaded_string_parser(subparsers)

    setup_logger()

    try:
        args = parser.parse_args(args=parse_args(parser, subparsers))

        if args.system == BEADED_STRING:
            animation = LoadedStringAnimation.build(
                args.masses, args.modes, args.boundary, args.speed)

            animation.animate(save=args.save)

    except ValueError as e:
        logger.error(e)


if __name__ == '__main__':
    main()
