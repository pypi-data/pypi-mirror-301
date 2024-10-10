#New Project:
from scriptlink import *
import numpy as np
cudadll = ctypes.CDLL(str.lower(os.path.join(os.path.dirname(__file__), 'CudaRuntime1.dll')))
opencldll = ctypes.CDLL(str.lower(os.path.join(os.path.dirname(__file__), 'opencldll.dll')))
class Numps():
    @staticmethod
    def convdllfloat(img,filt):
        #print(img.shape,img.dtype,filt.shape,filt.dtype)
        y,x=filt.shape
        newx=img.shape[1]-x+1
        newy=img.shape[0]-y+1
        #padx=x-1
        #pady=y-1
        #res=np.zeros((newy)*(newx),dtype=np.float64)
        res=np.zeros((newy,newx),dtype=np.float64)
        #print(res.shape,res.dtype)
        cd.ConvDllFloat.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS'),
                            ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t]
        cd.ConvDllFloat(res,img,filt,img.shape[1],img.shape[0],x,y,1)
        
        return res        
    def convdll3d(img,filt):
        #print(img.shape,img.dtype,filt.shape,filt.dtype)
        z,y,x=filt.shape
        newx=img.shape[1]-x+1
        newy=img.shape[0]-y+1
        newz=img.shape[2]
        res=np.zeros((newy,newx,newz),dtype=np.uint8)
        #res+=img[:-2][:-2][:]
        #res+=img[:-2,:-2,:]
        #return res
        #print(res.shape,res.dtype)
        cd.ConvDll3d.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint8, ndim=3, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.uint8, ndim=3, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.uint8, ndim=len(filt.shape), flags='C_CONTIGUOUS'),
                            ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t]
        cd.ConvDll3d(res,img,filt,img.shape[1],img.shape[0],img.shape[2],x,y,z)
        
        return res        
    
    def conv2d(img,filt):
        y,x=filt.shape
        newx=img.shape[1]-x+1
        newy=img.shape[0]-y+1
        #padx=x-1
        #pady=y-1
        res=np.zeros((img.shape[0]-y+1,img.shape[1]-x+1),dtype=np.uint8)
        for j in range(y):
            for i in range(x):
                res+=filt[j][i]*img[j:j+newy,i:i+newx]
        return res        
    def conv3d(img,filt):
        y,x=filt.shape
        #print(img.shape,img.dtype,filt.shape,filt.dtype)
        newx=img.shape[1]-x+1
        newy=img.shape[0]-y+1
        #padx=x-1
        #pady=y-1
        res=np.zeros((img.shape[0]-y+1,img.shape[1]-x+1,4),dtype=np.uint8)
        #print(res.shape,res.dtype)
        for j in range(y):
            for i in range(x):
                res+=filt[j][i]*img[j:j+newy,i:i+newx]
        return res  
    
class OpenCL():
    def alldeviceprops():
        opencldll.cl_devicepropsbig()
class Cuda():
    def deviceprops(devicenum=0):
        cudadll.cuda_deviceprops.restype = ctypes.c_char_p
        string=cudadll.cuda_deviceprops(devicenum).decode('utf-8')
        return string
    def alldeviceprops():
        cudadll.cuda_devicepropsbig()
    def devicename(devicenum=0):
        cudadll.cuda_devicename.restype = ctypes.c_char_p
        string=cudadll.cuda_devicename(devicenum).decode('utf-8')
        return string
    def devicequery():
        import subprocess
        d=r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin\__nvcc_device_query.exe"
        subprocess.run([d, ""]) 
        
        
    def devicecount():
        return cudadll.cuda_devicecount()
    def testcuda(blocks,threads,devicenum=0):
        res=cudadll.testcuda(blocks,threads,devicenum)
        print("blocks:%d threads:%d res:%d"%(blocks,threads,res))
        return res
    def addsquares(a,b,sz,devicenum=0):
        import numpy as np
        dt=np.int32
        arr_to = np.empty(shape=(sz), dtype=dt)
        cudadll.testcudaaddsquare.argtypes = [
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            ctypes.c_size_t,ctypes.c_size_t]
        cudadll.testcudaaddsquare(a,b,arr_to,sz,devicenum)
        #res = np.frombuffer(arr_to, dtype=np.uint64)
        return arr_to
    def MM(M1,M2,M3,b,m,r,devicenum=0):
        import numpy as np
        dt=np.int32
        #arr_to = np.empty(shape=(b*r), dtype=dt)
        cudadll.cudaMM.argtypes = [
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            np.ctypeslib.ndpointer(dtype=dt, ndim=1, flags='C_CONTIGUOUS'),
            ctypes.c_size_t,ctypes.c_size_t, ctypes.c_size_t,ctypes.c_size_t]
        cudadll.cudaMM(M1.ravel(),M2.ravel(),M3.ravel(),b,m,r,devicenum)
        #res = np.frombuffer(arr_to, dtype=np.uint64)
        return M3
    