



class RepoDependsOnRegister(type):
    registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_class = type.__new__(cls, name, bases, attrs)
        cls.registry[name] = attrs['depends_on']
        return new_class


