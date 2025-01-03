from litestar import Litestar, post
from msgspec import Struct

class DemoStruct(Struct):
    name: str

@post('/')
async def general(data: DemoStruct) -> DemoStruct:
    print(data)
    return data





app = Litestar([general])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

