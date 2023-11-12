import pytest

from frequenpy import cli
from frequenpy.loaded_string.animation import LoadedStringAnimation


class AnimationMock:
    def start(self, *args, **kwargs):
        pass


def test_cli(monkeypatch):
    monkeypatch.setattr(LoadedStringAnimation, 'build', lambda *args, **kwargs: AnimationMock())

    cli.run([
        'loaded_string', '--masses', '5', '--modes', '1', '2', '--speed', '0.1', '--boundary', '0'
    ])

    with pytest.raises(SystemExit):
        cli.run([])

    with pytest.raises(ValueError):
        cli.parse_args(['invalid'])

    with pytest.raises(AssertionError):
        cli.run(['loaded_string'])
