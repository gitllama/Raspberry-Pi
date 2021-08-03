# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
import time
import pyopencl
from pyopencl import mem_flags

def ReadRaw(filepath, t, width, height):
    data = np.fromfile(filepath, t)
    return data.reshape((height, width))
    
def ReadRawToInt32(filepath, t, width, height):
    data = np.fromfile(filepath, t)
    data[data>2147483647] = 2147483647
    data[data<0] = 0
    dataint32 = data.astype(np.int32)
    return dataint32.reshape((height, width))
def HOB200C(src):
    w = src.shape[1]
    hob_l = src[:,12:128+12].mean(1).reshape(-1,1)
    hob_r = src[:,w-12-128:w-12].mean(1).reshape(-1,1)
    return src - ((hob_l + hob_r) / 2).astype(np.int32)
def Stagger(src, flag):
    h = src.shape[0]
    w = src.shape[1]
    
    #masking
    mask_odd = 1 - np.arange(h).reshape(h,1) % 2
    mask_even = np.arange(h).reshape(h,1) % 2
    mat_odd = src * mask_odd
    mat_even = src * mask_even
    
    #Stagger
    spacer = np.zeros(h).reshape(h,1)
    if flag in {'R', 'r'}:
        mat_even = np.hstack((spacer, mat_even))
        mat_even = np.delete(mat_even, w, 1)
    elif flag in {'L', 'l'}:
        mat_even = np.hstack((mat_even, spacer))
        mat_even = np.delete(mat_even, 0, 1)
    return mat_odd + mat_even
    
def Demosaic(src, flag, RGain, BGain):
    #Clip
    src[src>65535] = 65535
    src[src<0] = 0
    mat16 = src.astype(np.uint16)
    
    #Demosaic
    if flag in {'GR', 'gr'}:
        pic = cv2.cvtColor(mat16, cv2.COLOR_BAYER_GR2BGR)
    elif flag in {'RG', 'rg'}:
        pic = cv2.cvtColor(mat16, cv2.COLOR_BAYER_RG2BGR)
    elif flag in {'GB', 'gb'}:
        pic = cv2.cvtColor(mat16, cv2.COLOR_BAYER_GB2BGR)
    elif flag in {'BG', 'bg'}:
        pic = cv2.cvtColor(mat16, cv2.COLOR_BAYER_BG2BGR)
    
    #Gain
    gain = np.array([ BGain,  1,  RGain]).reshape(1,1,3)
    pic = pic * gain
    pic[pic>255] = 255
    return pic.astype(np.uint8)
def Mono(src):
    #Clip
    src[src>255] = 255
    src[src<0] = 0
    return src.astype(np.uint8)
def Show(pic):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def SaveBMP(pic, filepath):
    cv2.imwrite(filepath, pic)
#Set value
filepath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Documents\\001.btn"
savefilepath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Documents\\out.bmp"
savefilepath2 = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Documents\\out2.bmp"
width = 7872
height = 4348
                        
offset = -700
bitshift = 5
RGain = 1.5
BGain = 3
#read raw data
matint = ReadRaw(filepath, np.int16, 7872, 4348)
#digital processing
matint = matint + int(offset)                #offset
matint = matint >> int(bitshift)             #bitshift
matint = Stagger(matint,"R")                     #Stagger
#matint = matint[49:49+1096, 160:160+1936]                 #Trim                       
#Demosaic and Color Gain
start = time.time()
image = Demosaic(matint, 'GR', RGain, BGain)   
stop = time.time()
print( "compute with CPU : ", stop - start, " sec")
#show image
#Show(image)
#SaveBMP(image, savefilepath)
src = matint.reshape(height,width).astype(np.int32)
dst = np.random.randint(0, 256, (height*width*3)).astype(np.int32)

context = pyopencl.create_some_context(interactive=False)
queue = pyopencl.CommandQueue(context)
src_buf = pyopencl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=src)
dst_buf = pyopencl.Buffer(context, mem_flags.WRITE_ONLY, dst.nbytes)

program = pyopencl.Program(context, '''
    __kernel void matrix_mul(
        __global const int* src,
        __global int* dst,
        const int w,
        const float RGain,
        const float BGain
    )
    {
        const int y = get_global_id(0)*2 + 1;
        const int x = get_global_id(1)*2 + 1;
        const int i = x + w * y;
        
        int aG1 = i*3+1;
        int aG2 = (i+1)*3+1;
        int aG3 = (i+w)*3+1;
        int aG4 = (i+w+1)*3+1;
        int aB1 = i*3;
        int aB2 = (i+1)*3;
        int aB3 = (i+w)*3;
        int aB4 = (i+w+1)*3;
        int aR1 = i*3+2;
        int aR2 = (i+1)*3+2;
        int aR3 = (i+w)*3+2;
        int aR4 = (i+w+1)*3+2;
        
        int G11 = src[i-1-w];
        int B12 = src[i-w];
        int G13 = src[i+1-w];
        int B14 = src[i+2-w];
        int R21 = src[i-1];
        int G22 = src[i];
        int R23 = src[i+1];
        int G24 = src[i+2];
        int G31 = src[i-1+w];
        int B32 = src[i+w];
        int G33 = src[i+1+w];
        int B34 = src[i+2+w];
        int R41 = src[i-1+w+w];
        int G42 = src[i+w+w];
        int R43 = src[i+1+w+w];
        int G44 = src[i+2+w+w];
        
        int G1 = (G11 + G13 + G22 + G31 + G33)/5;
        int G2 = (G13 + G22 + G24 + G33)/4;
        int G3 = (G22 + G31 + G33 + G42)/4;
        int G4 = (G22 + G24 + G33 + G42 + G44)/5;
        
        int B1 = BGain * (B12 + B32)/2;
        int B2 = BGain * (B12 + B14 + B32 + B34)/4;
        int B3 = BGain * (B32)/1;
        int B4 = BGain * (B32 +B34)/2;
        int R1 = RGain * (R21 + R23)/2;
        int R2 = RGain * (R23)/1;
        int R3 = RGain * (R21 + R23 + R41 + R43)/4;
        int R4 = RGain * (R23 + R43)/2;
        
        if(G1 > 255) dst[aG1] = 255;
        else if(G1 < 0) dst[aG1] = 0;
        else dst[aG1] = G1;
        if(G2 > 255) dst[aG2] = 255;
        else if(G2 < 0) dst[aG2] = 0;
        else dst[aG2] = G2;
        if(G3 > 255) dst[aG3] = 255;
        else if(G3 < 0) dst[aG3] = 0;
        else dst[aG3] = G3;
        if(G4 > 255) dst[aG4] = 255;
        else if(G4 < 0) dst[aG4] = 0;
        else dst[aG4] = G4;
        
        if(B1 > 255) dst[aB1] = 255;
        else if(B1 < 0) dst[aB1] = 0;
        else dst[aB1] = B1;
        if(B2 > 255) dst[aB2] = 255;
        else if(B2 < 0) dst[aB2] = 0;
        else dst[aB2] = B2;
        if(B3 > 255) dst[aB3] = 255;
        else if(B3 < 0) dst[aB3] = 0;
        else dst[aB3] = B3;
        if(B4 > 255) dst[aB4] = 255;
        else if(B4 < 0) dst[aB4] = 0;
        else dst[aB4] = B4;
        
        if(R1 > 255) dst[aR1] = 255;
        else if(R1 < 0) dst[aR1] = 0;
        else dst[aR1] = R1;
        if(R2 > 255) dst[aR2] = 255;
        else if(R2 < 0) dst[aR2] = 0;
        else dst[aR2] = R2;
        if(R3 > 255) dst[aR3] = 255;
        else if(R3 < 0) dst[aR3] = 0;
        else dst[aR3] = R3;
        if(R4 > 255) dst[aR4] = 255;
        else if(R4 < 0) dst[aR4] = 0;
        else dst[aR4] = R4;
    }
    ''').build()
start = time.time()
e = program.matrix_mul(
        queue
        , (int(height/2)-6,int(width/2)-6) #src.shape
        , None
        , src_buf
        , dst_buf
        , np.int32(width)
        , np.float32(1.5)
        , np.float32(3.0))
e.wait()
pyopencl.enqueue_copy(queue, dst, dst_buf)
dst = dst.reshape(height,width,3).astype(np.uint8)

stop = time.time()
print( "compute with GPGPU : ", stop - start, " sec")
#dst2 = np.dstack((dstB,dstG,dstR)).astype(np.uint8)
Show(dst)
#SaveBMP(dst, savefilepath2)
