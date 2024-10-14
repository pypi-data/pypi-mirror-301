import random

def randsign (number:float = 1) -> int:
    return random.choice([-1, +1]) * number

