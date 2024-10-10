import pytest
from PyResilient import fallback

def fallback_func(arg1, arg2=None):
    print(f"Fallback called with arg1={arg1}, arg2={arg2}")
    return f"Fallback called with arg1={arg1}, arg2={arg2}"


@pytest.mark.asyncio
async def test_async_fallback():
    @fallback(fallback_func)
    async def async_func(arg1, arg2=None):
        raise ValueError("Intentional Error")
        
    result = await async_func(1, arg2="test")
    assert result == "Fallback called with arg1=1, arg2=test"

def test_sync_no_fallback():
    @fallback(fallback_func)
    def no_error_func(arg1, arg2=None):
        return f"Success with arg1={arg1}, arg2={arg2}"

    result = no_error_func(1, arg2="test")
    assert result == "Success with arg1=1, arg2=test"

@pytest.mark.asyncio
async def test_async_no_fallback():
    @fallback(fallback_func)
    async def no_error_func(arg1, arg2=None):
        return f"Success with arg1={arg1}, arg2={arg2}"

    result = await no_error_func(1, arg2="test")
    assert result == "Success with arg1=1, arg2=test"

def test_fallback_with_missing_args():
    def fallback_with_defaults(arg1, arg2="default"):
        return f"Fallback called with arg1={arg1}, arg2={arg2}"

    @fallback(fallback_with_defaults)
    def sync_func_with_defaults(arg1):
        raise ValueError("Intentional Error")

    result = sync_func_with_defaults(1)
    assert result == "Fallback called with arg1=1, arg2=default"

@pytest.mark.asyncio
async def test_async_fallback_with_missing_args():
    async def fallback_with_defaults(arg1, arg2="default"):
        return f"Fallback called with arg1={arg1}, arg2={arg2}"

    @fallback(fallback_with_defaults)
    async def async_func_with_defaults(arg1):
        raise ValueError("Intentional Error")

    result = await async_func_with_defaults(1)
    assert result == "Fallback called with arg1=1, arg2=default"
