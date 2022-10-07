from io import StringIO

from true_north import Colors, Group


def test_smoke():
    g = Group(name='gname')
    called = 0

    @g.add(loops=2, repeats=3)
    def func_name(r):
        nonlocal called
        called += 1
        assert len(list(r)) == 2

    stream = StringIO()
    colors = Colors(disabled=True)
    g.print(stream=stream, colors=colors)
    assert called == 4
    stream.seek(0)
    output = stream.read()
    assert output.startswith('gname\n')
    assert '  func_name\n' in output
    assert '█' in output
    assert 'best of 3:' in output
    assert '2    loops' in output
