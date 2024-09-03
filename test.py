




class A:
    def __init__(self) -> None:
        setattr(self, 'asa', 1)


a = A()
print(a.asa)