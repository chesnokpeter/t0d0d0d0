def foo(foo):
    return foo

foo.__mro_entries__ = lambda bases: (str,)

class bar(foo):...

print(bar('lol'))
# lol