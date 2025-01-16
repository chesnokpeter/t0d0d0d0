import base64, json

from dataclasses import dataclass, field

from litestar import Response

from ..app.presentation import ServiceReturn

from ..app.shared import dtcls_slots2dict

@dataclass(eq=False, slots=True)
class RestServiceReturn(ServiceReturn):
    cookie: dict[str, str] = field(default_factory=dict)

    @property
    def response(self) -> Response:
        def by_encode(val: bytes):
            return base64.b64encode(val).decode('utf-8')

        def process_value(val):
            if isinstance(val, bytes):
                return by_encode(val)
            elif isinstance(val, list):
                return [process_value(item) for item in val]
            elif isinstance(val, dict):
                return {k: process_value(v) for k, v in val.items()}
            else:
                return val

        def process_data(data):
            ret = []
            for o in data:
                item = {}
                for name, val in dtcls_slots2dict(o).items():
                    item[name] = process_value(val)
                ret.append(item)
            return ret
        
        data = [i for i in process_data(self.data)] if self.data else [{}]
        return Response(
            content=json.dumps({
                'type': self.type,
                'message': self.message,
                'desc': self.desc,
                'data': data,
                'encrypted': self.encrypted,
            }), 
            status_code=200, 
            cookies=self.cookie if self.cookie else None
        )

    def add_cookie(self, **data):
        self.cookie = {k: v for k, v in data.items()}
        
        