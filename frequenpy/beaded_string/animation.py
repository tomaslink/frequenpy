from matplotlib import pyplot as plt
from matplotlib import animation
from os import path, makedirs


STRING_WIDTH = 0.3
STRING_MARKERTYPE = 'o'
STRING_MARKERSIZE = 5
STRING_MARKERFACECOLOR = 'white'
STRING_COLOR = 'white'

BACKGROUND_COLOR = 'black'

WALL_HEIGHT = 0.8
WALL_WIDTH = 0.5
WALL_COLOR = 'white'

FIG_SIZE = (10, 5)
FIG_DPI = 100
FIG_X_LIMIT = (-1, 1)
FIG_Y_LIMIT = (-1, 1)

ANIMATIONS_FOLDER = 'animations'


class Animation(object):

    def __init__(self, beaded_string, number_of_frames, save_animation):
        self._beaded_string = beaded_string
        self._number_of_frames = number_of_frames
        self._save_animation = save_animation
        self._line = self._build_line()
        self._frames = self._build_frames()
        self._figure = self._build_figure()

    def _build_figure(self):
        fig = plt.figure(figsize=FIG_SIZE, facecolor=BACKGROUND_COLOR)
        fig.set_dpi(FIG_DPI)
        ax = plt.axes(xlim=FIG_X_LIMIT, ylim=FIG_Y_LIMIT, frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.add_line(self._left_wall(self._beaded_string.longitude / 2))
        ax.add_line(self._ritgh_wall(self._beaded_string.longitude / 2))
        ax.add_line(self._line)
        return fig

    def _wall(self, x_coordinate):
        return plt.Line2D(
            (x_coordinate, x_coordinate),
            (-WALL_HEIGHT, WALL_HEIGHT),
            lw=WALL_WIDTH,
            color=WALL_COLOR
        )

    def _left_wall(self, x_distance_from_origin):
        return self._wall(-x_distance_from_origin)

    def _ritgh_wall(self, x_distance_from_origin):
        return self._wall(x_distance_from_origin)

    def _build_line(self):
        X, Y = self._beaded_string.initial_positions()
        return plt.Line2D(
            X, Y,
            marker=STRING_MARKERTYPE,
            lw=STRING_WIDTH,
            markersize=STRING_MARKERSIZE,
            markerfacecolor=STRING_MARKERFACECOLOR,
            color=STRING_COLOR,
            markevery=slice(1, len(X) + 1, 1)
        )

    def _build_frames(self):
        X = self._line.get_xdata()
        masses = range(0, len(X))
        frames = range(0, self._number_of_frames)
        return [
            (
                X,
                [
                    self._beaded_string.position_for_mass_n_at_time_t(n, t)
                    for n in masses
                ]
            )
            for t in frames
        ]

    def _update(self, frame_number):
        self._line.set_data(self._frames[frame_number])
        return self._line,

    def animate(self):
        anim = animation.FuncAnimation(
            self._figure,
            self._update,
            frames=self._number_of_frames,
            interval=5,
            blit=True,
            repeat=True)

        if (self._save_animation == 1):
            print('Saving animation...this could take a while...')
            name = "{}masses_{}modes.mp4".format(
                self._beaded_string.number_of_masses,
                str(self._beaded_string.normal_modes)
            )
            self._create_directory(ANIMATIONS_FOLDER)
            full_path = path.join(ANIMATIONS_FOLDER, name)
            anim.save(full_path)

        plt.show()

    def _create_directory(self, directory):
        if not path.exists(directory):
            makedirs(directory)
