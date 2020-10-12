# *_*coding:utf-8 *_*
from  distutils.core  import  setup
from  Cython.Build  import  cythonize
setup(
    name = 'Hello world app',
    ext_modules = cythonize("test1.py"),
)
