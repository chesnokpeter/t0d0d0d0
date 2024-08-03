from pydantic import BaseModel
import json

class Model(BaseModel):
    memorymodel_name: str
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.memorymodel_name = cls.__name__

class AuthCodeModel(Model):
    tgid: int
    tgusername: str

class MemoryModelManager:
    registry = {'AuthCodeModel':AuthCodeModel}
    @classmethod
    def serialize(cls, model_class: 'Model'):
        return json.dumps(model_class.model_dump())
    @classmethod
    def deserialize(cls, json_str: str) -> BaseModel:
        data = json.loads(json_str)
        memorymodel_name = data.pop("memorymodel_name", None)
        if memorymodel_name not in MemoryModelManager.registry:
            raise ValueError(f"Model '{memorymodel_name}' is not registered")
        model_class = MemoryModelManager.registry[memorymodel_name]
        return model_class(**data)


