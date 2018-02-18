pypack2d is texture packer written on Python and based on article

A thousand ways to pack the bin -- a practical approach to two-dimensional rectangle bin packing (http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.695.2918)

It provides easy to use, one function api and a lot of different options.

Requirements :
* PILLOW
* Python 3

# Features
* Three packing algorithms with different variety of options
* Solid borders, borders with calculable size and borders with colors from image edges
* Support for image rotation
* Support for custom post made hooks, useful for writing atlas metadata

Simple usage

```
import pypack2d
# first argument is a pathname for glob.glob
# second argument is a path to directory where atlas files would be stored
stats = pypack2d.pack("test/img/test/*.png", "test/img/atlas")

# also you can use list with filenames
stats = pypack2d.pack(["test/img/test/1.png", "test/img/test/2.png"], "test/img/atlas")

#third argument is options dict
# you can either use premade dict or write keyword arguments

stats = pypack2d.pack(
            "test/img/test/*.png",
            "test/img/atlas", 
            algo=pypack2d.PackingAlgorithm.MAX_RECTANGLES,
            heuristic=pypack2d.PlaceHeuristic.WORST_LONG_SIDE_FIT,
            atlas=dict(
                file_prefix="atlas",
                file_type="png",
                texture_mode="RGBA"
            )
        )
print("Count images: %i efficiency : %4.2f " % (stats["count"], stats["efficiency"]))
```

You can tweak a lot of options for ```pypack2d.pack``` function


```
# this is list of all possible options
# for all available variants look at ```pypack2d.pack2d.settings```

                 callback=lambda x: x,
                 heuristic=PlaceHeuristic.BEST_AREA_FIT,
                 sort_key=SortKey.SIDE_RATIO,
                 sort_order=SortOrder.ASC,
                 resize_mode=ResizeMode.NONE,
                 packing_mode=PackingMode.OFFLINE,
                 rotate_mode=RotateMode.NONE,
                 max_width=1024,
                 max_height=1024,
                 border=None,
                 border_mode=BorderMode.NONE
                 ):
                 
# all values are default ones 
pack_settings = dict(
    # postwrite atlas hook, in this callback you can save atlas meta data to your specific formats
    callback=None,
    
    # type of packing algorithm
    # MAX_RECTANGLES is considered to be the best algorithm for many choices
    algo=pypack2d.PackingAlgorithm.MAX_RECTANGLES,
    
    # if algo has specific params like guillotine split rule use dict
    # algo=dict(type=pypack2d.PackingAlgorithm.GUILLOTINE, split=pypack2d.GuillotineSplitRule.MAX_AREA),
    
    # specifies attribute used when comparing images for priority
    heuristic=pypack2d.PlaceHeuristic.BEST_AREA_FIT,
    
    # initial sort
    sort_order=pypack2d.SortOrder.ASC,
    sort_key=pypack2d.SortKey.SIDE_RATIO,
    
    # specifies if atlas can be resized to smaller size than (max_with, max_height)
    resize_mode=pypack2d.ResizeMode.NONE,
    # specifies type of packing processing
    packing_mode=pypack2d.PackingMode.OFFLINE,

    # specifies possible image rotation 
    rotate_mode=pypack2d.RotateMode.NONE,
    
    # atlas size
    max_width=1024,
    max_height=1024,
    
    # image border
    border=None,
    # if border_mode is pypack2d.BorderMode.NONE previous attirbute ingored
    border_mode=pypack2d.BorderMode.NONE,
    
    # atlas file settings
    atlas=dict(
        # atlas files will have names like file_prefix[number].file_type
        # for example with this settings program will generate files
        # atlas0.png, atlas1.png, atlas2.png, atlas[n].png 
        
        file_prefix="atlas",
        file_type="png",
        texture_mode="RGBA"
    )
    
)
stats = pypack2d.pack("test/img/test/*.png", "test/img/atlas", pack_settings)

```

## Border
```
# settings for specific color and specific size
border=dict(
    rect=dict(left=1, top=1, right=1, bottom=1),
    # or just size=1,
    type=pypack2d.BorderType.SOLID,
    color="#000"
),
border_mode=pypack2d.BorderMode.STRICT,

# settings for border with specific size and color from pixels from image edge
border=dict(
    rect=dict(left=1, top=1, right=1, bottom=1),
    type=pypack2d.BorderType.PIXELS_FROM_EDGE,
),
border_mode=pypack2d.BorderMode.STRICT,

# settings for border with auto generated size 

border=dict(
    # now you can use only size attribute because rect will be generated automatically
    size=1,
    # any type
    type=pypack2d.BorderType.SOLID,
    any type
    color="#000"
),
# this means that if some image has uv(left:0, top:0, right:1, bottom:1)
# its atlas border will be (0, 0, border_size, border_size)
border_mode=pypack2d.BorderMode.AUTO,
```

## writing atlas meta and unpacking atlas images
```
# this function will write simple json files in the same directory as atlas images 
# with content like
"""
{
  "path": "img/atlas/atlas0.png",
  "images": [
    {
      "uv": [
        0.016129032258064516,
        0.018518518518518517,
        0.12903225806451613,
        0.037037037037037035
      ],
      "path": "img/test/16.png",
      "rotated": false
    },
    {
      "uv": [
        0.016129032258064516,
        0.07407407407407407,
        0.04838709677419355,
        0.1111111111111111
      ],
      "path": "img/test/3.png",
      "rotated": false
    },
  ]
}
"""
def callback(atlas):
    import json
    images = []
    for image in atlas:
        images.append(dict(
            uv=image.uv,
            path=image.path,
            rotated=image.is_rotated
        ))

    # special helper 
    # for atlas with path folder1/folder2/atlas3.png it
    # will generate name folder1/folder2/atlas3.json 
    data_path = atlas.get_path_with_extension("json")
    data = dict(
        path=atlas.path,
        images=images
    )
    datafile = open(data_path, "w")
    with datafile as f:
        f.write(json.dumps(data))

pypack2d.pack("test/img/test/*.png", "test/img/atlas", callback=callback)

# unpacking atlas images
from PIL import Image
for filename in glob.glob("test/img/atlas/*.json"):
    datafile = open(filename, "r")
    data = datafile.read()
    datafile.close()
    data = json.loads(data)

    atlas = Image.open(data["path"])

    unpacked_dirname = "test/img/unpacked"
    for image_data in data["images"]:
        uv = image_data["uv"]
        rotated = image_data["rotated"]
        image = pypack2d.utils.extract_image_from_atlas(atlas, uv, rotated)
        path = image_data["path"]
        _, image_filename = os.path.split(path)
        result_path = os.path.join(unpacked_dirname, image_filename)
        image.save(result_path)
```


## Enums from ```pypack2d.pack2d.settings``` 
For more information about options you can read original article

```
class PackingAlgorithm(Enum):
    MAX_RECTANGLES = "MAX_RECTANGLES"
    GUILLOTINE = "GUILLOTINE"
    SHELF = "SHELF"


class PackingMode(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    LOCAL_SEARCH = "LOCAL_SEARCH"


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class SortKey(Enum):
    AREA = "AREA"
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    SHORTER_SIDE = "SHORTER_SIDE"
    LONGER_SIDE = "LONGER_SIDE"
    PERIMETER = "PERIMETER"
    SIDE_LENGTH_DIFFERENCE = "SIDE_LENGTH_DIFFERENCE"
    SIDE_RATIO = "SIDE_RATIO"


class PlaceHeuristic(Enum):
    FIRST_FIT = "FIRST_FIT"
    BEST_WIDTH_FIT = "BEST_WIDTH_FIT"
    BEST_HEIGHT_FIT = "BEST_HEIGHT_FIT"
    WORST_WIDTH_FIT = "WORST_WIDTH_FIT"
    WORST_HEIGHT_FIT = "WORST_HEIGHT_FIT"
    BEST_AREA_FIT = "BEST_AREA_FIT"
    BEST_SHORT_SIDE_FIT = "BEST_SHORT_SIDE_FIT"
    BEST_LONG_SIDE_FIT = "BEST_LONG_SIDE_FIT"
    WORST_AREA_FIT = "WORST_AREA_FIT"
    WORST_SHORT_SIDE_FIT = "WORST_SHORT_SIDE_FIT"
    WORST_LONG_SIDE_FIT = "WORST_LONG_SIDE_FIT"
    BOTTOM_LEFT = "BOTTOM_LEFT"


class ResizeMode(Enum):
    NONE = "STRICT"
    MINIMIZE_MAXIMAL = "MINIMIZE_MAXIMAL"
    MINIMIZE_POW2 = "MINIMIZE_POW2"


class PackingAlgorithmAbility(Enum):
    RECTANGLE_MERGE = "RECTANGLE_MERGE"
    WASTE_MAP = "WASTE_MAP"
    FLOOR_CEILING = "FLOOR_CEILING"


class GuillotineSplitRule(Enum):
    SHORTER_AXIS = "SHORTER_AXIS"
    LONGER_AXIS = "LONGER_AXIS"
    SHORTER_LEFTOVER_AXIS = "SHORTER_LEFTOVER_AXIS"
    LONGER_LEFTOVER_AXIS = "LONGER_LEFTOVER_AXIS"
    MAX_AREA = "MAX_AREA"
    MIN_AREA = "MIN_AREA"
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


class BorderMode(Enum):
    NONE = "NONE"
    STRICT = "STRICT"
    AUTO = "AUTO"


class BorderType(Enum):
    PIXELS_FROM_EDGE = "PIXELS_FROM_EDGE"
    SOLID = "SOLID"


class RotateMode(Enum):
    NONE = "NONE"
    UP_RIGHT = "UP_RIGHT"
    SIDE_WAYS = "SIDE_WAYS"
    AUTO = "AUTO"
```
