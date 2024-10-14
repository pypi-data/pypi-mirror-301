
This package adds cleaner typing for numpy arrays.  It
has been designed for deep learning and data processing tasks which generally
need a lot of numpy arrays of large dimensions.


To use the library modify all your import with :
```python
from numpy_typing import np, ax
```

The modified version of numpy imported there contain sumplementary annotations in order to have smart and automatic inferred annotation.

> Remark : This import load the real Numpy library. As Numpy-Typing do not use wrapper, every Numpy functions are directly called without intermediate code. Hence Numpy-Typing is as fast as Numpy.


You can then use new annotation like:
```python
float32Array3d:np.float32_3d[ax.batch, ax.sample, ax.feature] = np.zeros((3, 3, 3))
v = float32Array3d[0, 0, 0] # v automatically inferred as float32
```
The library add new array_types annotation:
- np.float32_(***n***)d
- np.float64_(***n***)d
- np.int32_(***n***)d
- np.int64_(***n***)d
- np.int8_(***n***)d
- np.bool_(***n***)d
- np.str_(***n***)d

Where ***n*** is the number of dimension of the array. The value of ***n*** is for instance only supported between [1, 4].

Moreover, as the library dosen't support yet all the numpy types, you can also use the generic type
```np.array_(1-4)d[dtype, axis1, ...]```

Then you should specify for each dimension the role of the dimension:
- ax.batch: The axis select the nth batch
- ax.sample: The axis select the nth sample of the batch
- ax.feature: The axis contain features
- ax.time: The axis represent the time
- ax.label: the axis contain labels
- ax.x: The axis represent the x coordinate
- ax.y: The axis represent the y coordinate
- ax.z: The axis represent the z coordinate
- ax.rgb: the axis contain a rgb value [0] for red, [1] for green and [2] for blue
- ax.rgba: the axis contain a rgba value [0] for red, [1] for green, [2] for blue and [3] for alpha

Here is an example of useful smart annotation:
```python
a:np.float32_1d[ax.time] = np.zeros((64))
b:np.float32_1d[ax.time] = np.zeros((64))
c = np.concatenate([a, b])
# automatically infer the type of c as np.float32_1d[ax.time]
```

If you want the library to support more types, more numpy functions or if you have any suggestion, feel free to open an issue on our [github](https://github.com/melpiro/numpy-typing).












