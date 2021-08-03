# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 01:27:22 2017

@author: Aki
"""

import numpy as np
import time
import pyopencl
from pyopencl import mem_flags

width = 7680
height = 4320

src = np.random.randint(0, 256, (height, width)).astype(np.float32)
dst = np.empty_like(src)
dst_np = np.empty_like(src)

start = time.time()

dst_np = src + 1

stop = time.time()
print( "compute with CPU   : ", stop - start  , " sec")

start = time.time()

context = pyopencl.create_some_context(interactive=False)
queue = pyopencl.CommandQueue(context)
src_buf = pyopencl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=src)
dst_buf = pyopencl.Buffer(context, mem_flags.WRITE_ONLY, dst.nbytes)

program = pyopencl.Program(context, '''
    __kernel void matrix_mul(
        __global const float* src,
        __global float* dst,
        const int w
    )
    {
        const int y = get_global_id(0) + 1;
        const int x = get_global_id(1) + 1;
        const int i = x + w * y;
        
        dst[i] = 0;
        dst[i] += src[i-1-w];
        dst[i] += src[i-w];
        dst[i] += src[i+1-w];
        dst[i] += src[i-1];
        dst[i] += src[i];
        dst[i] += src[i+1];
        dst[i] += src[i-1+w];
        dst[i] += src[i+w];
        dst[i] += src[i+1+w];
        dst[i] /= 9;
        //Gr
        
        //R
        
        //B
        
        //Gb

    }
    ''').build()

e = program.matrix_mul(
        queue
        , (height-2,width-2) #src.shape
        , None
        , src_buf
        , dst_buf
        , np.int32(width))
e.wait()
pyopencl.enqueue_copy(queue, dst, dst_buf)

stop = time.time()
print( "compute with GPGPU : ", stop - start, " sec")
