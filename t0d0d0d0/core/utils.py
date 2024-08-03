import random, string
import random
import string



def genAuthCode(length=4):
    characters = string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string
