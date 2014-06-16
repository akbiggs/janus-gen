def _get_supported_properties(prop_docs):
    props = prop_docs.split('\n')
    supported = [x.split(' ')[0] for x in props if x != '']
    if 'fwd' in supported:
        supported += ['xdir', 'ydir', 'zdir']
    return supported

def _get_required_properties(prop_docs):
    prop_lines = prop_docs.split('\n')
    reqs = []
    for prop_line in prop_lines:
        if not 'default' in prop_line:
            reqs.append(prop_line.split(' ')[0])

    return [req for req in reqs if req != '']

def _gen_docstring(description, prop_docs):
    return """
    {0} It has the following properties:
    {1}
    """.format(description, prop_docs)

def _inline_props(props):
    if not props:
        return ""

    inlined = ""
    for tag, value in props.iteritems():
        inlined += "{0}='{1}' ".format(tag, value)
    return inlined

def _verify_requirements(requirements, props):
    provided = props.keys()
    for req in requirements:
        if req not in provided:
            raise ValueError("Required property {0}".format(req))

def _verify_supported(supported, props):
    provided = props.keys()
    for prop in provided:
        if prop not in supported:
            raise ValueError("Unsupported property {0}".format(prop))

    if 'fwd' in provided and \
        any(dir in provided for dir in ['xdir', 'ydir', 'zdir']):
            raise ValueError("Can't use both fwd and individual direction properties")

def _make_tag_function(tag, has_body, description, prop_docs):
    required_properties = _get_required_properties(prop_docs)
    supported_properties = _get_supported_properties(prop_docs)

    if has_body:
        def fn(body, **props):
            _verify_requirements(required_properties, props)
            _verify_supported(supported_properties, props)

            return "<{0} {1}>{2}</{0}>".format(tag, _inline_props(props), body)
    else:
        def fn(**props):
            _verify_requirements(required_properties, props)
            _verify_supported(supported_properties, props)

            return "<{0} {1} />".format(tag, _inline_props(props))

    fn.__doc__ = _gen_docstring(description, prop_docs)
    return fn

def chain(*tags):
    return reduce(lambda x,y: x + '\n' + y, tags)

text = _make_tag_function("Text", True, "The Text tag allows the addition of 3D text to the room.", """
pos (default "0 0 0") - specify the position (anchor point is centered horizontally, and at the bottom vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour
scale (default "1 1 1") - scale the object along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
""")

text("Hello world", pos='0 0 0', fwd='0 0 -1', col='1 2 1', scale='1 1 1', locked='false')
paragraph = _make_tag_function("Paragraph", True, """
The Paragraph tag allows the addition a generated image which contains text,
use this instead of "Text" when you want to display a large amount of text
within the room (either this, or create your own image with text in it).
""",
"""
pos (default "0 0 0") - specify the position (anchor point is centered horizontally, and at the bottom vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour
font_size (default "16") - specify the font size for the text
text_col (default "1 1 1") - specify the colour of text
back_col (default "1 1 1") - specify the colour of the background
back_alpha (default "1") - specify the opacity (non-transparency) of the background
scale (default "1 1 1") - scale the object along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
""")

link = _make_tag_function("Link", False, """
A Link creates a portal which can be used to connect to another FireBoxRoom,
or any other webpage specified with a URL.""",
"""
url (default "") - specify the URL to link to
title (default "") - a title for the page the URL links to (shown until it is loaded)
pos (default "0 0 0") - specify the position (anchor point is centered horizontally, and at the bottom vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour, note that the colour will change once the page it links to is loaded
scale (default "1.8 2.5 1") - scale the portal, but note that scaling is only possible along x (horizontal, minimum scale 1.8), and y (vertical, minimum scale 2.5) directions
draw_glow (default "true") - whether to show the portal glow along the boundary
draw_text (default "true") - whether to show the text at the top of the portal for URL and page title
auto_load (default "false") - if true, the room that the portal links to will be loaded immediately; if false, the portal must first be clicked before it will load the room
thumb_id (default "") - if set to the id of an AssetImage, a "thumbnail image" will be displayed for the portal, useful for indicating what lies through it before it's loaded. The AssetImage content is expected to be square (width and height equal), and the portal will crop the image according to its dimensions to preserve the aspect ratio.
""")

image = _make_tag_function("Image", False, """
An Image is represented in 3D as a rectangular shape with thickness 1/10 of the
maximum width or height. The appearance is much like art done on canvas
wrapped around a wooden frame. The dimensions are such that the aspect
ratio of the image is preserved. Transparent images are supported and can
be used to interesting effect.
""",
"""
id - set to the id of an AssetImage
pos (default "0 0 0") - specify the position (anchor point is centered horizontally and vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour, this is multiplied by whatever colours the image contains
scale (default "1 1 1") - scale the object along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
""")

image3d = _make_tag_function("Image3D", False, """
An Image3D is geometrically the same as an Image, but its texture uses two different images,
where each is shown to either the left or right eye. When FireBox is used with
the Oculus Rift, this can produce a 3D effect. On a traditional display, only
the "left eye" image will be shown.
""",
"""
left_id - set to the id of the "left eye" AssetImage
right_id - set to the id of the "right eye" AssetImage
pos (default "0 0 0") - specify the position (anchor point is centered horizontally and vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour, this is multiplied by whatever colours the image contains
scale (default "1 1 1") - scale the object along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
""")

sound = _make_tag_function("Sound", False, """
A Sound plays a specific AssetSound when the player enters a
rectangle defined on the XZ plane, which is used to "trigger"
the sound. One can also specify whether the sound should loop
once triggered, or only play back once. To get ambient sound or
music to play for the room upon entry, use a very large rectangle
to trigger the sound (or at least contains the room's entrance portal),
and set the sound to loop.
""",
"""
id - set to the id of an AssetSound
rect (default "0 0 0 0") - presently, defines two opposite 2D corners of a rectangle which triggers the sound to play, the format is "X1 Z1 X2 Z2" (note that since the rectangle is 2D, the player's Y-position does not matter for triggering the sound, note also pressing "C" will toggle showing coordinates for your position and direction which is useful to determine the rectangle's bounds)
loop (default "false") - normally the sound plays only one time, but when this attribute is set to true, the sound will play indefinitely until the player leaves the room
play_once (default "false") - when set to true, the given Sound will only play one time for the duration of the visit. If set to "false" (the default), the sound will play once each time the player enters the room.
"""
)

video = _make_tag_function("Video", False, """
A Video plays a specific AssetVideo. The video can be controlled
by left clicking on it (stop and play). You can specify whether
the video should loop once playing, and whether the video should
start playing automatically when the room is entered. Multiple Video's
can be associated with one AssetVideo without any extra performance penalty
(useful if you want the same video to appear at multiple locations in the room).
The video will appear in the room as a rectangle, and the ratio of the
height and width dimensions will match that of the video itself,
preserving aspect ratio. All videos in a room are stopped automatically
when the user leaves the room.)
""",
"""
id - set to the id of an AssetVideo
pos (default "0 0 0") - specify the position (anchor point is centered horizontally and vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour, this is multiplied by whatever colours the frames of video contain
scale (default "1 1 1") - scale the video along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
""")

object = _make_tag_function("Object", False, """
An Object refers to an instance of 3D geometry placed in the room.
Objects can be used to define both the geometry of the room,
as well as the boundary for the room, by using the collision_id
attribute, detailed below.
""",
"""
id - set to the id of an AssetObject
pos (default "0 0 0") - specify the position (anchor point is centered horizontally, and at the bottom vertically)
fwd (default "0 0 -1") - specify the orientation (or use xdir, ydir, zdir, defaults "1 0 0", "0 1 0", "0 0 -1")
col (default "1 1 1") - specify the colour, this is multiplied by whatever colours the image contains
scale (default "1 1 1") - scale the object along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
cull_face (default "back") - options are "back", "front", "none" which specify what polygons are culled when the Object is rendered
collision_id (default "") - when set to the id of an AssetObject, collision testing is performed with that AssetObject. This makes it possible to define the boundary for the room using one's own custom geometry. (Note that the id and collision_id attributes can be set differently - the collision_id may refer to an AssetObject which is a low-polygon count version of a more detailed model, such as a bounding cube or sphere. Note also that collision tests are not performed if the player is not within the bounding volume of the AssetObject.)
collision_radius (default "0") - when set to a value greater than zero, an invisible cylinder at the specified radius prevents the player from passing through this Object (note that presently, this ignores the vertical or Y-position of the player, the cylinder extends in both directions along the Y-axis infinitely)
rotate_axis (default "0 1 0") - defines an axis of rotation
rotate_deg_per_sec (default "0") - specifies the number of degrees to rotate per second about the axis defined by rotate_axis (note use of this feature is discouraged, as presently it breaks other interactions with FireBox - use at your own risk)
video_id (default "") - set to the id of an AssetVideo to shade the Object using frames of the video as a texture (see the section on AssetVideos for more information on defining an AssetVideo). Also note that the Object if clicked will serve as a control to start/stop the AssetVideo.
shader_id (default "") - set to the id of an AssetShader to shade the Object with a GLSL fragment shader (see the section on AssetShaders for more information on defining an AssetShader)
""")

ghost = _make_tag_function("Ghost", False, """
A Ghost refers to an instance of a recorded avatar
within the room. Properties for the ghost invariant
to the recording, such as scale, colour, and custom
geometry used to represent the ghost can all be specified.
When no geometry is specified for the "head" and "body"
parts of the ghost, a default boxy appearance is used.
Since a Ghost is a recording, there are options to set
the recording to loop and to auto_play on room entry.
""",
"""
id - set to the id of an AssetGhost
cull_face (default "back") - options are "back", "front", "none" which specify what polygons are culled when the Object is rendered (may be useful when using custom geometry for ghost's body and head)
col (default "1 1 1") - specify the colour
scale (default "1 1 1") - scale the ghost along each of its x (horizontal), y (vertical) and z (forward) axes
locked (default "false") - if "true", prevents modification of attributes
head_id (default "") - the id of an AssetObject which will be used to define the geometry for the head of the ghost
head_pos (default "0 1 0") - specify the relative position of the head in the model (the point of articulation for the head relative to the body, where the centre point between the feet should be at "0 0 0")
body_id (default "") - the id of an AssetObject which will be used to define the geometry for the body of the ghost
shader_id (default "") - set to the id of an AssetShader to shade the Ghost with a GLSL fragment shader (see the section on AssetShaders for more information on defining an AssetShader)
""")
