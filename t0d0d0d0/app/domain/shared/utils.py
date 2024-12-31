from typing import Any

def dtcls_slots2dict(cls) -> dict[str, Any]:
    return {field: getattr(cls, field) for field in cls.__annotations__}