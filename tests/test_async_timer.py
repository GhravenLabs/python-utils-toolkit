import asyncio
import importlib
import inspect
import pytest
from utils.timer import timer

@pytest.mark.parametrize('raises', [False, True])
def test_async_timer_covers_await_and_failure(monkeypatch, raises):
    module = importlib.import_module('utils.timer')
    clock = [1.0]
    logs = []
    monkeypatch.setattr(module.time, 'perf_counter', lambda: clock[0])
    monkeypatch.setattr(module.logger, 'info', lambda *args: logs.append(args))
    @timer
    async def work():
        clock[0] = 4.0
        if raises:
            raise ValueError('expected')
        return 42
    assert inspect.iscoroutinefunction(work)
    if raises:
        with pytest.raises(ValueError):
            asyncio.run(work())
    else:
        assert asyncio.run(work()) == 42
    assert logs[-1][-1] == 3.0
