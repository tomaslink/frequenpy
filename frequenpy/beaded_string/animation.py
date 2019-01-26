from matplotlib import pyplot as plt
from matplotlib import animation
from os import path, makedirs


LINE_WIDTH = 0.5
LINE_MARKERTYPE = 'o'
LINE_MARKERSIZE = 8
LINE_MARKERFACECOLOR = 'white'
LINE_COLOR = 'white'

BACKGROUND_COLOR = 'black'

WALL_HEIGHT = 0.8
WALL_WIDTH = 0.5
WALL_COLOR = 'white'

FIG_SIZE = (10, 5)
FIG_DPI = 100
FIG_X_LIMIT = (-0.8, 0.8)
FIG_Y_LIMIT = (-1, 1)

MARGIN_LEFT = 0.05
MARGIN_BOTTOM = 0.05
MARGIN_RIGHT = 0.95
MARGIN_TOP = 0.95

ANIMATIONS_FOLDER = 'animations'

CONTINUOUS_LIMIT = 30


class Animation(object):

    def __init__(self, beaded_string, number_of_frames, speed, save_animation):
        self._beaded_string = beaded_string
        self._number_of_frames = number_of_frames
        self._speed = speed
        self._save_animation = save_animation
        self._line = self._build_line()
        self._frames = self._build_frames()
        self._figure = self._build_figure()

    def _build_figure(self):
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
        ax.set_yticks([])
        ax.add_line(self._left_support(self._beaded_string.longitude / 2))
        ax.add_line(self._right_support(self._beaded_string.longitude / 2))
        ax.add_line(self._line)
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
        if self._beaded_string.number_of_masses > CONTINUOUS_LIMIT:
            return self._build_line_without_markers()
        else:
            return self._build_line_with_markers()

    def _build_line_with_markers(self):
        X, Y = self._beaded_string.rest_positions()
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
        X, Y = self._beaded_string.rest_positions()
        return plt.Line2D(
            X, Y,
            lw=LINE_WIDTH,
            color=LINE_COLOR
        )

    def _build_frames(self):
        self._beaded_string.apply_speed(self._speed)
        X = self._line.get_xdata()
        masses = range(0, len(X))
        frames = range(0, self._number_of_frames)
        return [
            (
                X,
                [
                    self._beaded_string.y_position_for_mass_n_at_time_t(n, t)
                    for n in masses
                ]
            )
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
        print('Saving animation...this could take a while...')
        name = "{}masses_{}modes.mp4".format(
            self._beaded_string.number_of_masses,
            str(self._beaded_string.normal_modes)
        )
        self._create_directory(ANIMATIONS_FOLDER)
        full_path = path.join(ANIMATIONS_FOLDER, name)
        animation.save(
            full_path, savefig_kwargs={'facecolor': BACKGROUND_COLOR}
        )

    def animate(self):
        anim = self._build_animation()

        if self._save_animation:
            self._save(anim)

        plt.show()

    def _create_directory(self, directory):
        if not path.exists(directory):
            makedirs(directory)
