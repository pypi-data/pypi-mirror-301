import time
import asyncio
import pytest
from PyResilient import timeout


# Unit Tests
class CustomTimeoutError(Exception):
        pass
@pytest.mark.asyncio
async def test_async_function_timeout():
    @timeout(1, TimeoutError)
    async def long_running_task():
        await asyncio.sleep(2)
        return "Completed"
    
    with pytest.raises(TimeoutError):
        await long_running_task()

@pytest.mark.asyncio
async def test_async_function_success():
    @timeout(3, TimeoutError)
    async def short_running_task():
        await asyncio.sleep(2.9)
        return "Completed"
    
    result = await short_running_task()
    assert result == "Completed"

def test_sync_function_timeout():
    @timeout(1, TimeoutError)
    def long_running_task():
        time.sleep(2)
        return "Completed"
    
    with pytest.raises(TimeoutError):
        long_running_task()

def test_sync_function_success():
    @timeout(3, TimeoutError)
    def short_running_task():
        time.sleep(2.9)
        return "Completed"
    
    result = short_running_task()
    assert result == "Completed"

def test_sync_function_timeout_with_custom_exception():
    @timeout(1, CustomTimeoutError)
    def long_running_task():
        time.sleep(2)
        return "Completed"
    
    with pytest.raises(CustomTimeoutError):
        long_running_task()
@pytest.mark.asyncio
async def test_async_function_timeout_with_custom_exception():
    @timeout(1, CustomTimeoutError)
    async def long_running_task():
        await asyncio.sleep(2)
        return "Completed"
    
    with pytest.raises(CustomTimeoutError):
        await long_running_task()