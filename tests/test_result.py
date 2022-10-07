import math

import pytest

from true_north import Colors, Result
from true_north._result import format_time


@pytest.mark.parametrize('timings, hist', [
    ([1, 1, 1],     '███'),
    ([1],           '█'),
    ([0],           '█'),
    ([0] * 20,      '█' * 20),
    ([13] * 20,     '█' * 20),
    ([1, 1],        '██'),
    ([.1, .1],      '██'),
    ([40.4, 40.4],  '██'),
    ([0, 0],        '██'),
    ([1, 2],        '▅█'),
    ([20, 40],      '▅█'),
    ([2, 1, 3],     '▆▃█'),
    ([1, 2, 3],     '▃▆█'),
    ([0, 3],        '▁█'),
])
def test_hisogram(timings, hist):
    r = Result(
        name='',
        total_timings=timings,
        each_timings=[],
        loops=1,
    )
    assert r.histogram == hist


@pytest.mark.parametrize('timings, stdev', [
    ([1],           0.816496580927726),
    ([1, 1],        0),
    ([3, 3, 3],     0),
    ([1, 1, 1],     0),
    ([2, 2, 2],     0),
    ([2, 4],        1),
    ([1, 2, 3],     0.816496580927726),
    ([4, 5, 6, 7],  1.118033988749895),
])
def test_stdev(timings, stdev):
    r = Result(
        name='',
        total_timings=[1, 2, 3],
        each_timings=timings,
        loops=1,
    )
    assert math.isclose(r.stdev, stdev)


def test_get_text():
    r = Result(
        name='',
        total_timings=[1, 2, 3],
        each_timings=[4, 5, 6, 7],
        loops=4,
    )
    actual = r.get_text(colors=Colors(disabled=True))
    exp = '    4    loops, best of 3:   1.000 s  ±   1.118 s                  ▃▆█'
    assert actual == exp


@pytest.mark.parametrize('given, expected', [
    (1,     '  1.000 s '),
    (.1,    '100.000 ms'),
    (.2,    '200.000 ms'),
    (1e-3,  '  1.000 ms'),
    (1e-6,  '  1.000 us'),
    (1e-9,  '  1.000 ns'),
])
def test_format_time(given, expected):
    colors = Colors(disabled=True)
    assert format_time(given, colors) == expected
