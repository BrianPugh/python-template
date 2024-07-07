cimport cpythontemplate  # See cpythontemplate.pxd
# Invoke PyErr_CheckSignals() occasionally if your C code runs long.
# This allows your code to be interrupted via ctrl+c.
from cpython.exc cimport PyErr_CheckSignals
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.stddef cimport size_t


cdef class Foo:
    """Pythonic interface to the C "foo" struct."""
    cdef cpythontemplate.foo_t * _object

    def __cinit__(self):
        # Automatically called before __init__.
        # All arguments passed to __init__ are also passed to __cinit__.
        #    * As a convenience, if __cinit__() takes no arguments (other than self), it will
        #      ignore arguments passed to the constructor without complaining about signature mismatch.
        # Allocate memory for C objects here.
        self._object = <cpythontemplate.foo_t *>PyMem_Malloc(sizeof(cpythontemplate.foo_t))
        if self._object is NULL:
            raise MemoryError

    def __dealloc__(self):
        # Should "undo" __cinit__
        PyMem_Free(self._object)

    def __init__(self):
        cpythontemplate.foo_init(self._object)

    def __call__(self):
        # invoke increment
        cpythontemplate.foo_increment(self._object)

# Functions declared with cpdef are visible to both cython and python.
# https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html#python-functions-vs-c-functions
# https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html#error-return-values
cpdef float divide(float x, float y) except? 1.23:
    if y == 0.0:
        raise ZeroDivisionError
    return x / y
