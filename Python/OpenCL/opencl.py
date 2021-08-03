# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 01:27:22 2017

http://kirin.hatenadiary.jp/entry/2014/09/15/182221

"""

import numpy
from numpy import linalg
import time
import pyopencl
from pyopencl import mem_flags

size = 1024
print("matrix : ", size, " x ", size)

a = numpy.random.randint(0, 256, (size,size)).astype(numpy.int32)
b = numpy.random.randint(0, 256, (size,size)).astype(numpy.int32)
dest = numpy.empty_like(a)
 
start = time.time()
dest1 = numpy.dot(a, b)
end = time.time()
print( "compute with CPU (numpy) : ", end - start  , " sec")
 
dest1 = numpy.empty_like(a)
 
context = pyopencl.create_some_context(interactive=False)
queue = pyopencl.CommandQueue(context)
a_buf = pyopencl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=a)
b_buf = pyopencl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=b)
dest_buf = pyopencl.Buffer(context, mem_flags.WRITE_ONLY, dest1.nbytes)
 
program = pyopencl.Program(context, '''
    __kernel void matrix_mul(
        __global const int* a,
        __global const int* b,
        __global int* dest,
        const int n
    )
    {
        const int i = get_global_id(0);
        const int j = get_global_id(1);
        const int dest_index = j * n + i;
 
        dest[dest_index] = 0;
        for(int k = 0; k < n; k++){
            dest[dest_index] += a[j * n + k] * b[k * n + i];
        }
    }
''').build()
 
n = numpy.int32(size) # カーネル関数にスカラー値を渡すにはnumpyの型を使う
start = time.time()
e = program.matrix_mul(queue, a.shape, None, a_buf, b_buf, dest_buf, n)
e.wait()
stop = time.time()
 
pyopencl.enqueue_copy(queue, dest1, dest_buf)
print( "compute with GPGPU : ", stop - start, " sec")
