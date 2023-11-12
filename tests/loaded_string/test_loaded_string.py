import pytest
import numpy as np

from frequenpy.loaded_string import loaded_string_factory


def test_loaded_string_factory():

    loaded_string_factory.create(N=5, modes=[1, 2], boundary=0)
    loaded_string_factory.create(N=5, modes=[1, 2], boundary=1)
    loaded_string_factory.create(N=5, modes=[1, 2], boundary=2)

    with pytest.raises(ValueError):
        loaded_string_factory.create(N=5, modes=[1, 2], boundary=3)

    with pytest.raises(ValueError):
        loaded_string_factory.create(N=7, modes=[1, 2], boundary=0)

    with pytest.raises(ValueError):
        loaded_string_factory.create(N=2, modes=[1, 2, 3], boundary=0)

    with pytest.raises(ValueError):
        loaded_string_factory.create(N=2, modes=[1, 3], boundary=0)

    with pytest.raises(ValueError):
        loaded_string_factory.create(N=2, modes=[0, 2], boundary=0)


def test_loaded_string():
    ls = loaded_string_factory.create(N=5, modes=[1, 2], boundary=0)

    assert len(ls) == 5
    assert ls.modes == '1-2'

    ls.position_at_time_t(1)

    ls.apply_speed(2)

    _, Y = ls.rest_position
    assert np.all(Y == 0)
