import random
import string


def random_string(x):
    return "".join(random.choice(string.ascii_letters) for i in range(x))
