from PyResilient import retry
import pytest

def test_retry_sync_success():
    attempts = 3
    calls = 0

    @retry(attempts=attempts, delay=1, exceptions=(ValueError,))
    def test_func():
        nonlocal calls
        calls += 1
        if calls < attempts:
            raise ValueError("Intentional error")
        return "Success"

    assert test_func() == "Success"
    assert calls == attempts

def test_retry_sync_fail():
    attempts = 3

    @retry(attempts=attempts, delay=1, exceptions=(ValueError,))
    def test_func():
        raise ValueError("Intentional error")

    with pytest.raises(ValueError):
        test_func()

# Asynchronous function tests
@pytest.mark.asyncio
async def test_retry_async_success():
    attempts = 3
    calls = 0

    @retry(attempts=attempts, delay=1, exceptions=(ValueError,))
    async def test_func():
        nonlocal calls
        calls += 1
        if calls < attempts:
            raise ValueError("Intentional error")
        return "Success"

    result = await test_func()
    assert result == "Success"
    assert calls == attempts

@pytest.mark.asyncio
async def test_retry_async_fail():
    attempts = 3

    @retry(attempts=attempts, delay=1, exceptions=(ValueError,))
    async def test_func():
        raise ValueError("Intentional error")

    with pytest.raises(ValueError):
        await test_func()