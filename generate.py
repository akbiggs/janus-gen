import time
import random
import glob
import importlib
import re

def find_filenames(glob_string, extension):
    return list(map(lambda s: re.split('/', s.replace('\\', '/')
                                         .replace(extension, ''))[-1],
                      glob.glob(glob_string)))

def find_assets(*extensions):
    return reduce(lambda x,y: x+y, (find_filenames("./assets/*" + ext, ext) for ext in extensions))


def generate_asset_tags():
    tags = ""

    sound_assets = find_assets(".mp3")
    for asset in sound_assets:
        tags += "<AssetSound id='{0}_sound' src='{0}.mp3 />\n".format(asset)

    image_assets = find_assets(".png")
    for asset in image_assets:
        tags += "<AssetImage id='{0}_img' src='{0}.png' />\n".format(asset)

    material_assets = find_assets(".mtl")
    object_assets = find_assets(".obj")
    for asset in object_assets:
        tags += "<AssetObject id='{0}' src='{0}.obj' ".format(asset)
        if asset in material_assets:
            tags += "mtl='{0}.mat'".format(asset)
        elif asset in image_assets:
            tags += "tex='{0}.png'".format(asset)

        tags += " />\n"

    return tags

generators = find_filenames("./generators/*.py", ".py")
default_room_properties = {
    'base': 'room2',
    'assets': generate_asset_tags(),

    'enter_pos': '-20 0 0',
    'enter_xdir': '0 0 -1',
    'enter_ydir': '0 1 0',
    'enter_zdir': '1 0 0',

    'exit_pos': '20.0 0 0',
    'exit_xdir': '0 0 1',
    'exit_ydir': '0 1 0',
    'exit_zdir': '-1 0 0'
}

def merge(d1, d2):
    temp = d2.copy()
    temp.update(d1)
    return temp

def now():
    return round(time.time()*1000)

def get_random_generator(current_time):
    gen_name = random.choice(generators)
    return importlib.import_module('generators.' + gen_name)

def generate_color(current_time):
    phase = 360
    time_modulated = current_time % phase
    r = max(0, (time_modulated - (phase / 3)) / 360)
    b = max(0, (time_modulated - (phase / 2)) / 360)
    return "{0} {1} {2}".format(random.random(), random.random(), random.random())

def generate_properties(current_time, generator):
    generated_properties = {}
    generated_assets = ""
    if hasattr(generator, 'generate_properties'):
        generated_properties = generator.generate_properties(current_time)

    generated_properties['contents'] = generator.generate_content(current_time)
    return merge(merge(default_room_properties, {'color': generate_color(current_time)}),
                 generated_properties)

def generate_file(current_time):
    return """
<html>
<head><title>Infinity Passage</title></head>
<body>
  <FireBoxRoom>
  <Assets>
  {assets}
  </Assets>
  <Room pos='{enter_pos}' xdir='{enter_xdir}' ydir='{enter_ydir}' zdir='{enter_zdir}'
    col='{color}' use_local_asset='{base}'>
    {contents}
    <Link pos='{exit_pos}' xdir='{exit_xdir}' ydir='{exit_ydir}' zdir='{exit_zdir}'
      url='test.html' draw_text='false' />
  </Room>
  </FireBoxRoom>
</body>
</html>
    """.format(**generate_properties(current_time, get_random_generator(current_time)))

generate_file(0)
if __name__ == '__main__':
    elapsed_time = 0
    last_time = now()

    while True:
        current_time = now()
        elapsed_time += current_time - last_time
        last_time = current_time

        if elapsed_time > 1000:
            elapsed_time = 0
            with open("test.html", "w") as f:
                data = generate_file(now())
                f.write(data)
