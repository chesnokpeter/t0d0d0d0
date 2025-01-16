from typing import Any

def dtcls_slots2dict(cls) -> dict[str, Any]:
    if isinstance(cls, dict):
        return cls
    return {field: getattr(cls, field) for field in cls.__annotations__}