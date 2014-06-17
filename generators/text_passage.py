import random
import janus_gen.janus as j

STRINGS = [
    "HELLO WORLD",
    "I'M WATCHING YOU",
    "YOU CAN'T HIDE FROM ME",
    "INERTIA IS A PROPERTY OF MATTER"
]

def generate_content(assets, current_time):
    return j.chain(
        j.text(random.choice(STRINGS), xdir='0 0 1', ydir='0 1 0', zdir='-1 0 0')
    )
