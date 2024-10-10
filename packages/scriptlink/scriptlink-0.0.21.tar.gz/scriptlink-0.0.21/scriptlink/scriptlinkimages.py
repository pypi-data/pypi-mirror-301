from scriptlink import *
import numpy as np
from numpy.lib.stride_tricks import as_strided

class Operations():
    @staticmethod
    def conv3D2(var,kernel,stride=1,pad=0):
        def padArray(var,pad,method=1):
            if method==1:
                var_pad=np.zeros(tuple(2*pad+np.array(var.shape[:2]))+var.shape[2:])
                var_pad[pad:-pad,pad:-pad]=var
            else:
                var_pad=np.pad(var,([pad,pad],[pad,pad])+([0,0],)*(np.ndim(var)-2),
                        mode='constant',constant_values=0)
            return var_pad
        var_ndim=np.ndim(var)
        ny,nx=var.shape[:2]
        ky,kx=kernel.shape[:2]

        result=0

        if pad>0:
            var_pad=padArray(var,pad,1)
        else:
            var_pad=var

        for ii in range(ky*kx):
            yi,xi=divmod(ii,kx)
            slabii=var_pad[yi:2*pad+ny-ky+yi+1:1, xi:2*pad+nx-kx+xi+1:1,...]*kernel[yi,xi]
            if var_ndim==3:
                slabii=slabii.sum(axis=-1)
            result+=slabii

        if stride>1:
            result=result[::stride,::stride,...]

        return result
    def conv2ds(a, b, s=1):
        Hout = (a.shape[1] - b.shape[0]) // s + 1
        Wout = (a.shape[2] - b.shape[1]) // s + 1
        Stride = (a.strides[0], a.strides[1] * s, a.strides[2] * s, a.strides[1], a.strides[2], a.strides[3])

        a = as_strided(a, (a.shape[0], Hout, Wout, b.shape[0], b.shape[1], a.shape[3]), Stride)

        return np.tensordot(a, b, axes=3)
    def __stride_input(self, inputs):
        batch_size, channels, h, w = inputs.shape
        batch_stride, channel_stride, rows_stride, columns_stride = inputs.strides
        out_h = int((h - self.kernel_size) / self.stride + 1)
        out_w = int((w - self.kernel_size) / self.stride + 1)
        new_shape = (batch_size,
                     channels, 
                     out_h, 
                     out_w, 
                     self.kernel_size, 
                     self.kernel_size)
        new_strides = (batch_stride,
                       channel_stride,
                       self.stride * rows_stride,
                       self.stride * columns_stride,
                       rows_stride,
                       columns_stride)
        return np.lib.stride_tricks.as_strided(inputs, new_shape, new_strides)
    def forward_vectorized(self, inputs):
        """Accepts four dimensional input, with shape (Batch, Channels, Height, Width)"""
        '''number of filters, channels, kernel size, kernel width'''
        input_windows = self.__stride_input(inputs)
        self.inputs = inputs, input_windows
        output = np.einsum('bchwkt,fckt->bfhw', input_windows, self.weights) + self.bias[np.newaxis, :, np.newaxis]
        return output 
class FontHelper():
    p = ctypes.POINTER(ctypes.c_int32)()
    def __init__(self):
        pass
    def GetName(index):
        cd.getfontname.restype = ctypes.c_char_p
        return cd.getfontname(index) #GetFontName(index)
    def GetFontLetters(index,numberofletters,numberoffsets=0):
        cd.getfonts.argtypes = ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)),ctypes.c_size_t,ctypes.c_size_t
        cd.getfonts(FontHelper.p,index,numberoffsets) #GetFonts(pointer,fontindex)
        size=28*28*numberofletters*numberoffsets
        t=np.ctypeslib.as_array(FontHelper.p, shape=(size,))
        return t
class CV:
    def get_available_devices():
        import cv2
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr
    def cvputtext(img,text,x,y):
        import cv2
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (x,y)
        fontScale              = 1
        fontColor              = (255,40,255)
        thickness              = 1
        lineType               = 2
        cv2.putText(img,text,bottomLeftCornerOfText,font, fontScale,fontColor,thickness,lineType)

class ImageSorterClass:
    
    def __init__(self,h=28,w=28,sz=4096):
        np_load_old = np.load
        self.loadnew = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
        self.h=h;self.w=w;self.sz=sz
        self.arraysz=self.sz*self.h*self.w
        self.imgs=np.empty(self.arraysz, dtype=np.uint8)
        self.res=np.arange(0, self.sz, 1, dtype=int)
        self.imgsz=self.w*self.h
        self.img_arrayindex=0;self.imgno=0
        
    def loadmodel(loadname='data.npy'):
        self.wtsname=loadname
        self.img_mainct=0
        if (len(loadname)>0):
            if (os.path.exists(loadname)==0):
                print("failed to load",loadname)
            else:
                print("loaded",loadname)
                self.W=self.loadnew(loadname)
    def printweights(self):
        W = self.W
        print("len:",len(W))
        for a in W:
            print(a.shape)
        for a in W:
            print(a)
            
    def modelpredict(self,X):
        W = self.W#self.model.get_weights()#W = self.W
        #print(X.shape)
        X      = X.reshape(-1)           #Flatten   X      = X.reshape((X.shape[0],-1))
        #print(X.shape,W[0].shape,W[1].shape)
        X      = X @ W[0] + W[1]                      #Dense
        X[X<0] = 0                                    #Relu
        X      = X @ W[2] + W[3]                      #Dense
        X[X<0] = 0                                    #Relu
        X      = X @ W[4] + W[5]                      #Dense
        #print(X)
        #X      = np.exp(X)/np.exp(X).sum(1)[...,None] #SoftmaxX      = np.exp(X) / np.sum(np.exp(X));#np.exp(X)/np.exp(X).sum(1)[...,None] #Softmax
        #print(X,np.argmax(X))
        return X
    def singlepredict(self,X):
        W = self.W#self.model.get_weights()#W = self.W
        #print(X.shape)
        X      = X.reshape(-1)           #Flatten   X      = X.reshape((X.shape[0],-1))
        #print(X.shape,W[0].shape,W[1].shape)
        X      = X @ W[0] + W[1]                      #Dense
        X[X<0] = 0                                    #Relu
        X      = X @ W[2] + W[3]                      #Dense
        X[X<0] = 0                                    #Relu
        X      = X @ W[4] + W[5]                      #Dense
        #print(X)
        #X      = np.exp(X)/np.exp(X).sum(1)[...,None] #SoftmaxX      = np.exp(X) / np.sum(np.exp(X));#np.exp(X)/np.exp(X).sum(1)[...,None] #Softmax
        #print(X,np.argmax(X))
        return X
    '''def showimage(self,n):
        two_d = np.reshape(self.imgs[n*self.imgsz:n*self.imgsz+self.imgsz], (28, 28))
        plt.imshow(two_d, cmap='gray')
        plt.suptitle('imgno:'+str(n)+str(self.res[n]))
        plt.show()'''
    '''def findimgfile(self,name):
        tempfile=GetLocalFolder+name
        img = cv2.imread(tempfile,cv2.IMREAD_UNCHANGED)
        return self.find(img)'''
    '''img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dim = (self.w, self.h)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        r=resized.reshape(1,28,28)
        p=self.singlepredict(resized).argmax(0)
        return p;'''
    '''def findimg(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dim = (self.w, self.h)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        r=resized.reshape(1,28,28)
        p=self.singlepredict(resized).argmax(0)
        return p;'''


class WrapStruct(ctypes.Structure):
     _fields_ = [ ('x1',ctypes.c_int32),('y1',ctypes.c_int32),('x2',ctypes.c_int32),('y2',ctypes.c_int32),('sz',ctypes.c_int32),('area',ctypes.c_int32),('num',ctypes.c_int32), ('color',ctypes.c_int32), ('magnitude',ctypes.c_int32)]
class LineStruct(ctypes.Structure):
     _fields_ = [ ('x',ctypes.c_int32), ('y',ctypes.c_int32), ('x2',ctypes.c_int32),('y2',ctypes.c_int32),('ming',ctypes.c_int32),('leng',ctypes.c_int32) ]
class FillsStruct(ctypes.Structure):
     _fields_ = [ ('x1',ctypes.c_int32), ('y1',ctypes.c_int32), ('x2',ctypes.c_int32),('y2',ctypes.c_int32),('gd',ctypes.c_int32),('ct',ctypes.c_int32),('chroma',ctypes.c_int32),('color',ctypes.c_int32),('minarea',ctypes.c_int32),('maxarea',ctypes.c_int32),('minsz',ctypes.c_int32),('maxsz',ctypes.c_int32),('frame',ctypes.c_int32),('sort',ctypes.c_int32) ]
def FindFills(x,y,w,h,mingradient=30,frame=1,jump=0,chroma=0,color=121,minarea=0,maxarea=4000000,minsz=0,maxsz=4000000,sort=0):#chroma weights the color portion of the color filter vs the brightness
    if not hasattr(FindFills,"sz"):FindFills.sz=0;
    if (w*h!=FindFills.sz and frame==1):
        FindFills.sz=w*h
        FindFills._data=(ctypes.c_int8 * FindFills.sz*4)()
        print("\r\nnewsz"+str(FindFills.sz)+str(FindFills._data))
        
    finfo=FillsStruct(x,y,x+w,y+h,mingradient,0,chroma,color,minarea,maxarea,minsz,maxsz,frame,sort);
    _findfills=cd.FindFills
    _findfills.restype = ctypes.POINTER(WrapStruct)
    boxes=_findfills(FindFills._data,ctypes.pointer(finfo));
    ct=finfo.ct
    #print("%d %d %d %d %d %d %d %d" %(finfo.x1,finfo.y1,finfo.x2,finfo.y2,finfo.gd,finfo.len,finfo.ct,finfo.chrom))
    if (frame!=False):
        g=bytearray(FindFills._data)
        frame = np.ctypeslib.as_array(g)
        frame=np.reshape(frame,(h,w,4))
        return frame,ct,boxes
    return ct,boxes;
def FindLineOnScreen2(x,y,maxw,maxh,maxcount=5,leng=0,dst=None):
    linfo=LineStruct(x,y,x+maxw,y+maxh,mingradient,leng);
    ret=cd.FindLineOnScreen2(ctypes.pointer(linfo));
    linfo.leng=ret
    if (ret==0):return None
    if (dst!=None):
        pointer(dst)[0] = linfo
    return linfo;
def FindLineOnScreen(x,y,maxw,maxh,mingradient=30,leng=0,dst=None):
    linfo=LineStruct(x,y,x+maxw,y+maxh,mingradient,leng);
    ret=cd.FindLineOnScreen(ctypes.pointer(linfo));
    linfo.leng=ret
    if (ret==0):return None
    if (dst!=None):
        pointer(dst)[0] = linfo
    return linfo;
#place the point to the left of the target line or region
def FindBoundingBox(x,y,maxw=50,maxh=50,mingradient=30,leng=0,dst=None):
    linfo=LineStruct(x,y,maxw,maxh,mingradient,leng);
    ret=cd.FindBoundingBoxRight(ctypes.pointer(linfo));
    linfo.leng=ret
    if (dst!=None):
        pointer(dst)[0] = linfo
    return linfo;
    
    
GetImageMag=cd.ImageMag #GetFonts(pointer,fontindex)
cd.ImageMag.argtypes = ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_int32)
def ImageMag(x,y):
    data1 = (ctypes.c_int32 * 5)()
    #p = ctypes.POINTER(ctypes.c_int32)()
    GetImageMag(x,y,ctypes.cast(data1, ctypes.POINTER(ctypes.c_int32)))
    #for i in range(4):
        #print(data1[i])
    #t=np.ctypeslib.as_array(p, shape=(4,))
    return data1


h_FindTextinImageW=cd.FindTextinImageW
def FindTextinImage(name):
    n = ctypes.create_unicode_buffer(name)
    text=ctypes.create_string_buffer(3000)
    r=h_FindTextinImageW(n,text)
    return text
    
h_FindTextinImageW=cd.FindTextinImageW
def FindTextinImage(name):
    n = ctypes.create_unicode_buffer(name)
    text=ctypes.create_string_buffer(3000)
    r=h_FindTextinImageW(n,text)
    return text

#SaveImage("textimage.bmp",res[0],res[1]+60,800,100);
h_SpliceImageW=cd.SpliceImageW
def SpliceImage(namesmall,namebig,x,y,w,h):
    n = ctypes.create_unicode_buffer(namesmall)
    n2 = ctypes.create_unicode_buffer(namebig)
    x=ctypes.c_int()
    y=ctypes.c_int()
    r=h_SpliceImageW(n,n2,x,y,w,h)

#res=FastFindImage("fastfingersbox.bmp", "screen.bmp") 
h_FastFindImageW=cd.FastFindImageW
def FastFindImage(needle,haystack):
    n = ctypes.create_unicode_buffer(needle)
    h = ctypes.create_unicode_buffer(haystack)
    x=ctypes.c_int()
    y=ctypes.c_int()
    r=h_FastFindImageW(n,h,ctypes.byref(x),ctypes.byref(y))
    if (r==1):
        return x,y
    else: return -1,-1

h_FindImageW=cd.FindImageW
#cd.getfonts.argtypes = ctypes.POINTER(ctypes.POINTER(ctypes.c_int32))
def FindImageonScreen(needle,haystack="screen.bmp"):
    n = ctypes.create_unicode_buffer(needle)
    h = ctypes.create_unicode_buffer(haystack)
    #x=ctypes.c_int()
    #y=ctypes.c_int()
    p=(ctypes.c_int * 100)()
    #p = ctypes.POINTER(ctypes.c_int32)()
    r=h_FindImageW(n,h,ctypes.byref(p))
    if (r==0):return 0,0,0,[]
    #print(r)
    pts=[]
    w=p[0];h=p[1];
    for i in range(1 ,r+1):
        pts.append((p[2*i],p[2*i+1]))
    return w,h,r,pts

h_SlowFindImageW=cd.SlowFindImageW
def SlowFindImage(needle,haystack):
    n = ctypes.create_unicode_buffer(needle)
    h = ctypes.create_unicode_buffer(haystack)
    x=ctypes.c_int()
    y=ctypes.c_int()
    r=h_SlowFindImageW(n,h,ctypes.byref(x),ctypes.byref(y))
    if (r==1):
        return x,y
    else: return -1,-1

h_GetBMPHistW=cd.GetBMPHistW
def GetBMPHist(name):
    n = ctypes.create_unicode_buffer(name)
    p=(ctypes.c_int * (256*3))()
    #self._data=(ctypes.c_int8 * self.sz*4)()
    r=h_GetBMPHistW(n,ctypes.byref(p))
    print(p)
    #for i in range(1 ,r+1):
    #    pts.append((p[2*i],p[2*i+1]))
    return r,p

h_TrimColorImageW=cd.TrimColorImageW
def TrimColorImage(string,Trim=0):
    p = ctypes.create_unicode_buffer(string)
    h_TrimColorImageW(p,Trim)
    
h_MaskColorImageW=cd.MaskColorImageW
def MaskColorImage(string,mask=0):
    p = ctypes.create_unicode_buffer(string)
    h_MaskColorImageW(p,mask)
    
h_ReloadSpriteW=cd.ReloadSpriteW


class _CDRAW_SPRITE_2(ctypes.Structure):
    _fields_ = [ ('a',ctypes.c_int32),('x',ctypes.c_int32),('y',ctypes.c_int32),('dx',ctypes.c_int32),('dy',ctypes.c_int32),('name',ctypes.c_char * 32)]
class _CDRAW_SPRITE_1(ctypes.Structure):
    _fields_ = [('elements', ctypes.c_short),
                ('STRUCT_ARRAY', ctypes.POINTER(_CDRAW_SPRITE_2))]
    def __init__(self,num_of_structs):
        elems = (_CDRAW_SPRITE_2 * num_of_structs)()
        self.STRUCT_ARRAY = ctypes.cast(elems,ctypes.POINTER(_CDRAW_SPRITE_2))
        self.elements = num_of_structs
        for i in num_of_structs:
            self.STRUCT_ARRAY['a']=0
class CDrawClass():
    def __init__(self,max_sprites=1000):
        self.sprites = _CDRAW_SPRITE_1(max_sprites)
        self.ind=0;
        self.maxsprites=maxsprites-1
        cd.cdraw_savesprites(self.sprites);
    def test(self):
        cd.cdraw_test();
    def window(self,x,y):
        cd.cdraw_window(x,y);
    def addsprite(self,string,x,y,dx,dy):
        if (self.ind>self.maxsprites):
            self.ind=0
        while(self.ind<self.maxsprites and self.sprites[self.ind]['a']!=0):
            self.ind+=1
        self.sprites[self.ind]=[1,x,y,dx,dy,string.decode('utf8')];
        self.ind+=1
        return self.ind-1;
    def modsprite(self,index,on,x,y,dx,dy):
        self.sprites[index]=[on,x,y,dx,dy];