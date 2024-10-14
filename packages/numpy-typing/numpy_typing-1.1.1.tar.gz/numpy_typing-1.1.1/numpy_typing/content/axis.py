class __axis__:
    tag = -1
    i = -1
    name = ""

    def __init__(self, i):
        self.i = i

    def __hash__(self) -> int:
        return self.tag

    def copy(self, i):
        return self.__class__(i)

# |====================================================================================================================
# | Axis
# |====================================================================================================================
class batch(__axis__):
    tag = 0
    name = 'batch'
class sample(__axis__):
    tag = 1
    name = 'sample'
class time(__axis__):
    tag = 2
    name = 'time'
class feature(__axis__):
    tag = 3
    name = 'feature'
class values(__axis__):
    tag = 4
    name = 'feature'


class item(__axis__):
    tag = 5
    name = 'item'

# |====================================================================================================================
# | Coordinates
# |====================================================================================================================
class x(__axis__):
    tag = 6
    name = 'x'
class y(__axis__):
    tag = 7
    name = 'y'
class z(__axis__):
    tag = 8
    name = 'z'


# |====================================================================================================================
# | Color Channels
# |====================================================================================================================
class rgb(__axis__):
    tag = 9
    name = 'rgb'

class rgba(__axis__):
    tag = 10
    name = 'rgba'

# |====================================================================================================================
# | Machine Learning
# |====================================================================================================================
class label(__axis__):
    tag = 11
    name = 'label'


# batch = _batch()
# """Axis for batch dimension."""

# sample = _sample()
# """Axis for sample dimension."""

# time = _time()
# """Axis for time dimension."""

# feature = _feature()
# """Axis for feature dimension."""

# item = _item()
# """Axis for item dimension."""

# x = _x()
# """Represents the x-axis."""

# y = _y()
# """Represents the y-axis."""

# z = _z()
# """Represents the z-axis."""

# rgb = _rgb()
# """
# Axis for red, green, and blue color channels.
# [0] is red, [1] is green, and [2] is blue.
# """
# rgba = _rgba()
# """
# Axis for red, green, blue, and alpha color channels.
# [0] is red, [1] is green, [2] is blue, and [3] is alpha.
# """

# label = _label()
# """Axis for label dimension."""

