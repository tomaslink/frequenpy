import logging
from os import path, makedirs

from matplotlib import pyplot as plt
from matplotlib import animation

from frequenpy.loaded_string import loaded_string_factory

logger = logging.getLogger(__name__)

LINE_WIDTH = 1
LINE_MARKERTYPE = 'o'
LINE_MARKERSIZE = 8
LINE_MARKERFACECOLOR = 'None'
LINE_COLOR = 'white'

BACKGROUND_COLOR = 'black'

WALL_HEIGHT = 0.8
WALL_WIDTH = 0.5
WALL_COLOR = 'white'

FIG_SIZE = (7, 2)
FIG_DPI = 100
FIG_X_LIMIT = (-0.5, 0.5)
FIG_Y_LIMIT = (-1, 1)

MARGIN_LEFT = 0.05
MARGIN_BOTTOM = 0.05
MARGIN_RIGHT = 0.95
MARGIN_TOP = 0.95

ANIMATIONS_FOLDER = 'workdir'
FILENAME_TPL = "{}masses_{}modes.mp4"

NUMBER_OF_FRAMES = 2000
DEFAULT_SPEED = 1


class LoadedStringAnimation(object):
    def __init__(self, loaded_string, number_of_frames, speed=DEFAULT_SPEED):
        self._loaded_string = loaded_string
        self._number_of_frames = number_of_frames
        self._speed = speed

        self._line = self._build_line()
        self._figure = self._build_figure()
        self._frames = self._build_frames()

    def animate(self, save=False):
        anim = self._build_animation()

        if save:
            self._save(anim)

        plt.show()

    def build(N, modes, boundary, speed):
        loaded_string = loaded_string_factory.create(N, modes, boundary)
        return LoadedStringAnimation(loaded_string, NUMBER_OF_FRAMES, speed)

    def _build_figure(self):
        x_rest_position, _ = self._loaded_string.rest_position
        support_distance_from_origin = abs(x_rest_position[0])

        fig = plt.figure(figsize=FIG_SIZE, facecolor=BACKGROUND_COLOR)

        fig.set_dpi(FIG_DPI)
        fig.subplots_adjust(
            left=MARGIN_LEFT,
            bottom=MARGIN_BOTTOM,
            right=MARGIN_RIGHT,
            top=MARGIN_TOP
        )

        ax = plt.axes(xlim=FIG_X_LIMIT, ylim=FIG_Y_LIMIT, frameon=False)
        ax.set_yticks([])
        ax.set_xticks([])

        ax.add_line(self._left_support(support_distance_from_origin))
        ax.add_line(self._right_support(support_distance_from_origin))
        ax.add_line(self._line)

        plt.get_current_fig_manager().window.resizable(False, False)

        return fig

    def _support(self, x_coordinate):
        return plt.Line2D(
            (x_coordinate, x_coordinate),
            (-WALL_HEIGHT, WALL_HEIGHT),
            lw=WALL_WIDTH,
            color=WALL_COLOR
        )

    def _left_support(self, x_distance_from_origin):
        return self._support(-x_distance_from_origin)

    def _right_support(self, x_distance_from_origin):
        return self._support(x_distance_from_origin)

    def _build_line(self):
        if self._loaded_string.N == self._loaded_string.CONTINUOUS_LIMIT:
            return self._build_line_without_markers()
        else:
            return self._build_line_with_markers()

    def _build_line_with_markers(self):
        X, Y = self._loaded_string.rest_position

        return plt.Line2D(
            X, Y,
            marker=LINE_MARKERTYPE,
            lw=LINE_WIDTH,
            markersize=LINE_MARKERSIZE,
            markerfacecolor=LINE_MARKERFACECOLOR,
            color=LINE_COLOR,
            markevery=slice(1, len(X) - 1, 1)
        )

    def _build_line_without_markers(self):
        X, Y = self._loaded_string.rest_position

        return plt.Line2D(
            X, Y,
            lw=LINE_WIDTH,
            color=LINE_COLOR
        )

    def _build_frames(self):
        self._loaded_string.apply_speed(self._speed)
        frames = range(0, self._number_of_frames)

        return [
            self._loaded_string.position_at_time_t(t)
            for t in frames
        ]

    def _update(self, frame_number):
        self._line.set_data(self._frames[frame_number])

        return self._line,

    def _build_animation(self):
        return animation.FuncAnimation(
            self._figure,
            self._update,
            frames=self._number_of_frames,
            interval=5,
            blit=True,
            repeat=True)

    def _save(self, animation):
        logger.info('Saving animation...this could take a while...')

        self._create_directory(ANIMATIONS_FOLDER)
        filename = FILENAME_TPL.format(self._loaded_string.N, self._loaded_string.modes)
        filepath = path.join(ANIMATIONS_FOLDER, filename)

        animation.save(filepath, savefig_kwargs={'facecolor': BACKGROUND_COLOR})

    def _create_directory(self, directory):
        if not path.exists(directory):
            makedirs(directory)
