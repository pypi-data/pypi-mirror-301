import asyncio
import functools
import time


def retry(attempts:int=0, delay:int=0, exceptions:tuple=()):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                retries = 0
                while True:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                    
                        if not isinstance(e, exceptions) and exceptions != ():
                            raise e
                        if retries < attempts:
                            retries += 1
                        
                            if delay:
                                await asyncio.sleep(delay)
                        else:
                            raise e
        else:
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                while True:

                    try:
                        return func(*args, **kwargs)
                    
                    except Exception as e:
                        
                        if not isinstance(e, exceptions) and exceptions != ():
                            raise e
                        if retries < attempts:
                            retries += 1
                        
                            if delay:
                                time.sleep(delay)
                        else:
                            raise e
                            
        return wrapper
    return decorator


