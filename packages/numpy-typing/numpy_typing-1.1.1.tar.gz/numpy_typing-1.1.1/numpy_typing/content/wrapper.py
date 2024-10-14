import numpy as np
import numpy_typing.content.axis as ax
from . import typing



def empty(shape, *argv:"list[ax.__axis__]", dtype=np.float64, order='C'):
    return typing.___init___(np.empty(shape, dtype=dtype, order=order), argv)


def zeros(shape, *argv:"list[ax.__axis__]", dtype=np.float64, order='C', like=None):
    return typing.___init___(np.zeros(shape, dtype=dtype, order=order, like=like), argv)

