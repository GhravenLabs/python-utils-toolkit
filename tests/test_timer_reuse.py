import importlib
from utils.timer import Timer

def test_reused_timer_does_not_expose_previous_elapsed(monkeypatch):
    module = importlib.import_module('utils.timer')
    ticks = iter([1.0, 3.0, 4.0, 7.0])
    monkeypatch.setattr(module.time, 'perf_counter', lambda: next(ticks))
    timer = Timer(log=False)
    with timer:
        pass
    assert timer.elapsed == 2.0
    with timer:
        assert timer.elapsed == 0.0
    assert timer.elapsed == 3.0
