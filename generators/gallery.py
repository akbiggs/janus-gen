import janus as j
import random

def generate_content(assets, current_time):
    tags = []
    for i in range(0, 10):
        offset = -15 + i * 3

        left_image = random.choice(assets['images'])
        tags.append(j.image(id=left_image, pos='{0} 1.5 -5'.format(offset)))

        right_image = random.choice(assets['images'])
        tags.append(j.image(id=right_image, pos='{0} 1.5 4.9'.format(offset)))

    return j.chain(*tags)
