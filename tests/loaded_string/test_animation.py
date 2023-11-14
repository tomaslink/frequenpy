import os
from matplotlib import pyplot

from frequenpy.loaded_string.animation import LoadedStringAnimation


def test_animation(monkeypatch, tmp_path):
    anim = LoadedStringAnimation.build(N=5, modes=[1, 2], boundary=0, n_frames=1, folder=tmp_path)
    monkeypatch.setattr(pyplot, "show", lambda *x, **y: 0)
    anim.start()

    filepath = anim.start(save=True)
    assert os.path.exists(filepath)

    folder = os.path.join(tmp_path, 'new')
    anim = LoadedStringAnimation.build(N=30, modes=[1], boundary=0, n_frames=1, folder=folder)
    anim.start(save=True)
