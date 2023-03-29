from typing import Any

class _AsyncGeneratorContextManager:
    gen: Any
    __doc__: Any
    def __init__(self, func, args, kwds) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, typ, value, traceback): ...

def asynccontextmanager(func): ...
