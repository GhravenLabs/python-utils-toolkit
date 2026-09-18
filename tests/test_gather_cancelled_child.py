import asyncio
import pytest
from utils.async_utils import gather_safe

def test_cancelled_child_returns_none_in_original_position():
    async def cancelled():
        raise asyncio.CancelledError()
    async def success():
        return 42
    async def main():
        return await gather_safe(cancelled(), success())
    assert asyncio.run(main()) == [None, 42]

def test_parent_cancellation_still_propagates():
    async def main():
        started = asyncio.Event()
        async def child():
            started.set()
            await asyncio.Event().wait()
        parent = asyncio.create_task(gather_safe(child()))
        await started.wait()
        parent.cancel()
        with pytest.raises(asyncio.CancelledError):
            await parent
    asyncio.run(main())
