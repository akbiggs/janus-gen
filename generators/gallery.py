import janus_gen.janus as j
import random

def generate_content(assets, current_time):
    tags = []
    for i in range(0, 10):
        offset = i * 0.5

        left_image = random.choice(assets['images'])
        tags.append(j.image(id=left_image, pos='{0} 0 -5'.format(offset)))

        right_image = random.choice(assets['images'])
        tags.append(j.image(id=right_image, pos='{0} 0 5'.format(offset)))

    return j.chain(*tags)
