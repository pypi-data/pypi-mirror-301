###Main Scriptlink Library###
#Kill Driver is Control Escape#
#mss requ//ascreentestbugged//trigger hook bug//
##FileNotFoundError: Could not find module    MEANS dependency DLL not found!!
import time
import ctypes
import os
#dll_dir=os.path.dirname(__file__)
#print(dll_dir)
os.environ.setdefault('PATH', '')
os.environ['PATH'] += os.pathsep + os.path.dirname(__file__)
#print(os.environ['PATH'])
#os.add_dll_directory(os.curdir())
#os.add_dll_directory(dll_dir)
cd = ctypes.CDLL(str.lower(os.path.join(os.path.dirname(__file__), 'scriptlink.dll')))
sl_libdir=os.path.dirname(__file__)
import logging
import threading
import time
import sys
import io
import math
#import cv2
from time import perf_counter
from ._slconstants import *
import importlib
import sysconfig
from .scriptlinkbasic import *
import json
import types

#from scriptlinktk import *
#import superfastcode as sfc

#--------------InitializeSettings---------------

    
def doinitstuff():
    globals()["slconfigjson"]=Utils.loadjsonfile(os.path.join(os.path.dirname(__file__), 'config.json'))    
    if ('SL_DEBUGGER' in os.environ):
        OldGui.turndebugon()
    if (sys.version_info.major==3 and sys.version_info.minor==11):
        globals()["superfastcode"]=__import__("scriptlink.superfastcode")
        #clock=sfc.clock
#---------Globals----------
Sleep=cd.sleep#15-25ms accuracy
clock=cd.clocktime#1ms accuracy
def debugprint(*args, **kwargs):
    if ('SL_DEBUGGER' in os.environ):
        print(args,*kwargs)
def _format_time(tm):
    tmlist=["s","ms","us","ns","ps"]
    tmlist2=[1e-3,1,1e3,1e6,1e9]
    ev=math.log10(tm+1e-12)//3
    ev=1-int(ev)
    ev=max(min(ev,4),0)
    r="%.03f %s"%(tm*tmlist2[ev],tmlist[ev])
    return r
def ClockIt(s="\r\ntime",printoff=False,total=False):
    ClockIt.__dict__.setdefault("big", list())
    if not hasattr(ClockIt, "t"):
        ClockIt.t=time.time()*1000
        return '0'
    #if (test!=None):tm=test
    tm=time.time()*1000-ClockIt.t
    r="%s:%s"%(s,_format_time(tm))
    if (total==True):
        li=[_[1] for _ in ClockIt.__dict__["big"]]
        r+=" total:%dms"%(sum(li))
    ClockIt.__dict__["big"].append([s,tm])
    ClockIt.t=time.time()*1000
    if (printoff==False):
        print(r)
    return tm
def printshape(*args):
    #print(dir(obj))
    for obj in args:
        print(type(obj), end=' ')
        if (getattr(obj,"shape",None)):
            print(obj.shape)
        if (getattr(obj,"__len__",None)):
            print(obj.__len__())

def _sl_clamp(x, l, u):
    return l if x < l else u if x > u else x
GetMouseX=cd.GetMouseX #GetMouseX() 440ns vs 640ns
GetMouseY=cd.GetMouseY #GetMouseY()
def GetMouseXY():return GetMouseX(),GetMouseY();
GetScreenX=cd.GetScreenX #GetScreenX()
GetScreenY=cd.GetScreenY
ScreenX=GetScreenX();ScreenY=GetScreenY();
def GetScreenXY():return GetScreenX(),GetScreenY();
def GetKeyState(key):return Keyboard.keystate(key)
def GetKey():return Keyboard.getkeyevents()
def KeyDown(key):return Keyboard.KeyDown(key)
def KeyUp(key):return Keyboard.KeyUp(key)
def KeyPress(*keys):return Keyboard.KeyCombo(*keys)
def TypeString(s):return Keyboard.TypeString(s)
def MoveMouse(x,y):return Mouse.Move(x,y)
def MouseMove(x,y):return Mouse.Move(x,y)
def DragMouseLeft(x,y,x2,y2):return Mouse.MouseDragPixel(x,y,x2,y2,1)
def DragMouseRight(x,y,x2,y2):return Mouse.MouseDragPixel(x,y,x2,y2,2)
def DragMouse(x,y,x2,y2,button):return Mouse.MouseDragPixel(x,y,x2,y2,button)
def LeftClick(x,y):Mouse.LeftClick(x,y)
def RightClick(x,y):Mouse.RightClick(x,y)
#GetKeyState=cd.getkeystate #GetKeyState(virtualkey)
GetMouseClick=cd.getmouseclickcoords #GetMouseClick(virtualkey,x1,y1,x2,y2)
GetKeyClick=cd.getkeyclick

RGBCOLORS={"red":0xFFFF0000,"green":0xFF00CC00,"blue":0xFF0000FF,"green":0xFF00CC00,"yellow":0xFF00CCCC,"white":0xFFFFFFFF,"black":0xFF010101}
def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents
class _dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
class Mouse():
    #keycodes VK['LeftButton'] = 0x01 VK['RightButton'] = 0x02 VK['Cancel'] = 0x03 VK['MiddleButton'] = 0x04 VK['ExtraButton1'] = 0x05 VK['ExtraButton2'] = 0x06
    oldkeystate=0
    movespeed=50
    clickspeed=50
    #----------------mouse state funcs-----------------
    def isdown(key):return cd.getkeystate(key)#left=1,right=2,middle=4,extra=5,6
    def isdownleft():return cd.getkeystate(1)#left=1,right=2,middle=4,extra=5,6
    def isdownright():return cd.getkeystate(2)#left=1,right=2,middle=4,extra=5,6
    def isdownmiddle():return cd.getkeystate(4)#left=1,right=2,middle=4,extra=5,6
    def lastclicktime(key):return cd.lastclicktime(key)
    def isclicked_complete(key):
        k=GetKeyState(key)
        if (Mouse.oldkeystate==key and k==0 and Mouse.oldkeystate!=0):
            Mouse.oldkeystate=0
            return 1
        if (k!=0):
            Mouse.oldkeystate=key
        return 0;
    def isclicked(key):
        k=GetKeyState(key)
        if (Mouse.oldkeystate==0 and k!=0):
            Mouse.oldkeystate=key
            return 1
        if (k==0):Mouse.oldkeystate=0
        return 0;
    def GetMouseXY():return cd.GetMouseX(),cd.GetMouseY();
    def GetMouseMoveXY():
        xy=cd.getmousemovexy()
        #print("%x"%(xy))
        return (xy&0xFFFF)-1024,(xy>>16);
    def getXY():return cd.GetMouseX(),cd.GetMouseY();
    def getXY_percent():return GetMouseX()/GetScreenX(),GetMouseY()/GetScreenY()
    def GetMouseRoll():
        return cd.getmouseroll()
    
        
    #----------------mouse output funcs-----------------
    def LeftClick(x=-1,y=-1,waittime=20):
        if (x!=-1):cd.mousemovepixel(x,y);Sleep(waittime);
        cd.mousedown(1);Sleep(waittime); cd.mouseup(1);Sleep(waittime);
    def RightClick(x=-1,y=-1,waittime=2):
        if (x!=-1):cd.mousemovepixel(x,y);Sleep(waittime);
        cd.mousedown(2);Sleep(waittime); cd.mouseup(2);Sleep(waittime);
    def MovePixel(x,y):cd.mousemovepixel(x,y) #MoveMouse(x,y)
    def MovePercent(px,py):cd.mousemovepercent(px,py) #MoveMouse(x,y)
    def Move(x,y):cd.mousemovepixel(x,y) #MoveMouse(x,y)
    def MoveTo(x,y):cd.mousemovepixel(x,y) #MoveMouse(x,y)
    def MoveRel(offsetx,offsety):
        x=cd.GetMouseX()
        y=cd.GetMouseY()
        cd.mousemovepixel(x+offsetx,y+offsety) #MoveMouse(x,y)
    def Scroll(value):cd.ScrollMouse(value)
    #def DetectMouseMovement(status):
        #return cd.DetectMouse(status)    
    
    def MouseDown(key):cd.mousedown(key)
    def MouseUp(key):cd.mouseup(key)
    def MouseClickPercent(x1,y1,MouseButton):return cd.mouseclickpercent(x1,y1,MouseButton) #MouseClickPercent(x1,y1,MouseButton 1-2)
    def MouseDragPercent(x1,y1,x2,y2,Mousebutton): return cd.mousemovepercent(x1,y1,x2,y2,Mousebutton) #DragMouse(x1,y1,x2,y2,Mousebutton 1-2)
    def MouseDragPixel(x,y,x2,y2,Mousebutton):
        Mouse.Move(x,y)
        Sleep(Mouse.movespeed)
        Mouse.MouseDown(Mousebutton)
        Sleep(Mouse.movespeed)
        Mouse.Move(x2,y2)
        Sleep(Mouse.movespeed)
        Mouse.MouseUp(Mousebutton)
        Sleep(Mouse.movespeed)
    def SetMouseMoveSpeed(speed=10):
        Mouse.movespeed=speed
        cd.setmousespeed(speed) #SetMouseSpeed(0-100)
    def SetMouseClickSpeed(speed=10):
        Mouse.clickspeed=speed
        cd.setmousespeed(speed) #SetMouseSpeed(0-100)
    
    def MoveRelativePercent(rpx,rpy):cd.mousemoverelativepercent(rpx,rpy) #MoveMouse(x,y)
    def SlowMoveMouse(relx,rely,waittime=50):
        dy=1*rely/relx
        dy=rely/relx
        while (relx>0):
            cd.mousemoverelativepercent(1,int(dy));
            relx-=1
            Sleep(waittime)
    def move(x,y):
        if (x<1 and x>0):x=100*x;y=100*y;
        cd.mousemovepercent(int(x),int(y))
    
class Keyboard():
    #keycodes VK['A']=0x41   VK['Tab'] = 0x09 VK['Return'] = 0x0D VK['Shift'] = 0x10 VK['Control'] = 0x11 VK['Alt'] = 0x12 VK['Escape'] = 0x1B
    # VK['N0']= 0x30 VK['Left'] = 0x25 VK['Up'] = 0x26 VK['Right'] = 0x27 VK['Down'] = 0x28
    triggerthread=None
    triggers=[]
    oldkeystate=[0]*256
    VK={"esc":27,"`":192,"~":192,"tab":9,"caps":20,"shift":16,"ctrl":17,"control":17,"alt":18,"space":32,"enter":13,"return":13,
        "left":37,"up":38,"right":39,"down":40}
    def StopDriverAndHooks():
        cd.AllHooksOff()
    def StartDriverOrHooks():
        r=Keyboard.StartDriver()
        if (r==0):r=Keyboard.StartHooks()
        if (r==0):print("failed to start driver or hooks")
        return r
    #########DRIVER MUST RECEIEVE KEYPRESS OR MOUSECLICK FIRST BEFORE YOU CAN SEND WITH IT######
    def StartDriver():return cd.SwitchDriverOn()
    def StartHooks():return cd.SwitchHooksOn()
    def StopDriver():return cd.SwitchDriverOff()
    def StopHooks():return cd.SwitchHooksOff()
    def codefromkey(key):
        if (type(key)==type("k")):
            key=key.lower()
            try:key=Keyboard.VK[key]
            except:key=ord(key[:1])
        return key
    def keyfromcode(code):
        try:key=Keyboard.RVK[code]
        except:key="Unknown"
        return key
    def keystate(key):
        key=Keyboard.codefromkey(key)
        #print(key)
        return cd.getkeystate(key)
    def keyclicked(key):
        key=Keyboard.codefromkey(key)
        return Keyboard.isclicked_down(key)
    def makevks():
        Keyboard.VK.update({i.name.lower(): i.value for i in VK})
        Keyboard.RVK={i.value:i.name.lower() for i in VK}
    def CreateVKCodes():
        for i in range(1,256):
            text=WindowsUtils.vkcodetotext(i)
            Keyboard.VK[text]=i
    def getkeyevents():
        _data=Keyboard.getkeyqueue()
        print(_data)
        eventlist=[]
        states={0:"keydown",1:"keyup"}
        i=0
        while(i<len(_data)):
            tp=states[_data[i+1]]
            k=Keyboard.keyfromcode(_data[i])
            eventlist.append(_dotdict({"type":tp,"key":k}))
            i+=2
        return eventlist
            
    def getkeyqueue():
        _data=(ctypes.c_int32 * 1500)()
        ct=cd.getkeyque(_data)
        data=list(_data)[:ct*2]
        return data;
    def getcurrentkeysdown():
        _data=(ctypes.c_int32 * 500)()
        ct=cd.getcurrentkeysdown(_data)
        data=list(_data)[:ct]
        return data;
    def geteventcount():return cd.getkeyboardeventcounter()
    def gettotaleventcount():return cd.getinputeventcounter()
    def lastclicktime(key):return cd.lastclicktime(key)
    def isclicked_complete(key):#keydown and keyup only triggers once
        k=GetKeyState(key)
        if (Keyboard.oldkeystate[key]!=0 and k==0):
            Keyboard.oldkeystate[key]=0
            return 1
        Keyboard.oldkeystate[key]=k
            #Keyboard.oldkeystate[key]=1
        return 0;
    def isclicked_down(key):#keydown only triggers once
        k=GetKeyState(key)
        if (Keyboard.oldkeystate[key]==0 and k!=0):
            Keyboard.oldkeystate[key]=1
            return 1
        Keyboard.oldkeystate[key]=k
        return 0;
    def isdown(key):return GetKeyState(key);  #while not Keyboard.isdown(VK['Escape'])
    def lastkey():return cd.getlastkey(249)
    def WaitKey(key):
        k=GetKeyState(key)
        while(1):
            k=GetKeyState(key)
            if (k!=0): break
            Sleep(50)
    def WaitAnyKey():
        k=cd.getlastkey(3)
        while(k==0):
            k=cd.getlastkey(3)
            Sleep(50)
        return k
    
    #----------------other keyinput funcs-----------------
    def TriggerThread():
        #print("triggerthreadon",Keyboard.triggers)
        for t in Keyboard.triggers:
            for k in t["keys"]:
                print(k,Keyboard.codefromkey(k))
        while(1):
            for t in Keyboard.triggers:
                for k in t["keys"]:
                    if (GetKeyState(k)==0):
                        if (t["ctr"]==1 and t["once"]=="onceup"):
                            t["func"]()
                        t["ctr"]=0
                        break
                    #print(k,Keyboard.codefromkey(k))
                else:
                    if (t["once"]=="alwaysdown"):
                        t["func"]()
                    elif(t["once"]=="oncedown"):
                        print(t["once"])
                        if (t["ctr"]==0):
                            print("odown")
                            t["ctr"]=1
                            t["func"]()
                    elif(t["once"]=="onceup"):
                        if (t["ctr"]==0):
                            t["ctr"]=1
            Sleep(10)
    def SetTrigger(func,*keys,once="onceup"):
        #print("trigger added",func,once,*keys)
        Keyboard.triggers.append({"func":func,"keys":list(keys),"once":once,"ctr":0})
        if (Keyboard.triggerthread==None):
            Keyboard.triggerthread=True
            x = threading.Thread(target=Keyboard.TriggerThread, args=[])
            x.daemon = True
            x.start()
            
    def KeyCombo(*args):
        keylist=[Keyboard.codefromkey(k) for k in args]#list(args)
        #print(keylist)
        for key in keylist:
            #key=Keyboard.codefromkey(key)
            #print(key)
            Keyboard.KeyDownVK(key)
        keylist.reverse()
        for key in keylist:
            #key=Keyboard.codefromkey(key)
            Keyboard.KeyUpVK(key)
            
    def TypeString(s,delay=5):cd.typestring(s.encode('utf8'),delay);
    def Write(s,delay=5):cd.typestring(s,delay);
    def KeyClickScanCode(scancode): return cd.keyclickdx(scancode)   #DirectX Scan Code
    def KeyDownScanCode(scancode): return cd.keydowndx(scancode)   #DirectX Scan Code
    def KeyUpScanCode(scancode): return cd.keyupdx(code)   #DirectX Scan Code
    def KeyDownVK(VkCode): return cd.keydownvk(VkCode)   #VkCode
    def KeyUpVK(VkCode): return cd.keyupvk(VkCode)   #VkCode
    def KeyDown(key):
        key=Keyboard.codefromkey(key)
        cd.keydownvk(key)
    def KeyUp(key):
        key=Keyboard.codefromkey(key)
        cd.keyupvk(key)
    def KeyClick(key):
        key=Keyboard.codefromkey(key)
        cd.keyclickvk(key)
        
    def DetectKeys(status):
        return cd.DetectKeys(status)
    
    def BlockAllKeyboardInput(time=2000):
        BlockMenuInput=cd.blockallkeyboardinput(time)#(0 or 1)
    def BlockAllMouseInput(time=2000):
        BlockMenuInput=cd.blockallmouseinput(time)#(0 or 1)
    def BlockMenuInput(on,time=2000):
        BlockMenuInput=cd.blockinput(on,time)#(0 or 1, all keyboard and left mouse)
    def BlockKeyInput(key,on,time=10000):
        cd.blockkeyinput(key,on,time)#specific key block BlockKeyInput(key,0 or 1)
    def BlockMouseInput(mousekey,on,time=3000):
        cd.blockmouseinput(mousekey,on,time)#specific mouse block BlockMouseInput(mouseval,0 or 1)
Keyboard.makevks()

#print(Keyboard.VK)
class MemoryClass:
    def __init__(self,windowname="",windowclassname="",exename="",maxdatasz=10000):
        self.proc=cd.GetProcess(windowname.encode('utf8'),windowclassname.encode('utf8'),exename.encode('utf8'))
        self.sz=maxdatasz
        self.makedatabuf()
    def makedatabuf(self):
        self._data=(ctypes.c_int8 * self.sz)()
    def changeprocess(self,windowtitle="",windowclassname="",exename=""):
        self.proc=cd.GetProcess(windowtitle.encode('utf8'),windowclassname.encode('utf8'),exename.encode('utf8'))
    def LoadLibraryIntoProcess(self,filename):
        cd.LoadLibraryIntoProcess(filename.encode('utf8'))
    def findint(self,intval,bytecount,MAXCOUNT=1000):
        self._add=(ctypes.c_int64 * MAXCOUNT)()
        res=cd.findinteger(intval,bytecount,self._add)
        return list(self._add)
    def getsegs(self,MAXCOUNT=1000):
        self._add=(ctypes.c_int64 * MAXCOUNT)()
        res=cd.getsegs(self._add)
        return list(self._add)
    def readint64(self,address):
        return cd.rBint64(address)
    def readint32(address):
        return cd.rBint32(address)
    def readint16(self,address):
        return cd.rBint16(address)
    def readint8(self,address):
        return cd.rBint8(address)
    def readstring(self,address):
        cd.rBs(address,self._data)
        return self._data.decode("utf-8")
    def readbytes(self,address):
        cd.rBs(address,self._data)
        return self._data
    def writebytes(self,address,data,numwrite):
        cd.wBs(address,data,numwrite)
    def writestring(self,address,string):
        cd.wBs(address,string.encode('utf8'),len(string)+1)



class ScreenClass:#screenargb to bytearray or to disk
    imageshowon=0
    def __init__(self, x=0,y=0,w=0,h=0,colors=4):
        
        self._data=None
        self.w=w
        self.h=h
        self.x=x;self.y=y
        self.sz=self.w*self.h
        self.colors=colors
        if (self.sz==0):
            self.w=GetScreenX()
            self.h=GetScreenY()
            self.sz=self.w*self.h
        self._data=(ctypes.c_int8 * self.sz*colors)()
        self.ar8x8=(ctypes.c_int32 * 2*int(self.sz/64))()
        #print("ScreenClass (%d,%d,%d) tp:%s sz:%d"%(w,h,colors,type(self.ar8x8),2*int(self.sz/64)))
        debugprint("ScreenClass (%d,%d,%d) tp:%s sz:%d"%(w,h,colors,type(self.ar8x8),2*int(self.sz/64)))
        cd.ForceNewCapture(1)
    def changemode(self,d3dmode=0,backgroundmode=0):
        self.mode=d3dmode
        self.backgroundmode=backgroundmode
        cd.ChangeCaptureMode(self.mode,self.backgroundmode)
        return self.mode
    def changedims(self,x=0,y=0,w=0,h=0):
        x=_sl_clamp(x,0,ScreenX)
        y=_sl_clamp(y,0,ScreenY)
        if (x+w>ScreenX):w=ScreenX-x
        if (y+h>ScreenY):h=ScreenY-y
        self.w=w
        self.h=h
        self.x=x;self.y=y
        if (w*h!=self.sz):
            self.sz=w*h
            self._data=(ctypes.c_int8 * self.sz*self.colors)()
            self.ar8x8=(ctypes.c_int32 * 2*int(self.sz/64))()
        
    def savexywh(self,name,x,y,w,h):
        cd.ScreenCapturetoFileW(name.encode('utf8'),x,y,w,h)
    def savexywh_raw(self,name,x,y,w,h):
        cd.ScreenCapturetoFileRaw(name.encode('utf8'),x,y,w,h)
    def grabxywh(self,x,y,w,h):
        self.changedims(x,y,w,h)
        cd.ScreenCapturetoArray(self._data,self.x,self.y,self.w,self.h)
        return bytearray(self._data)
    def frame(self,forcenew=1):
        import numpy as np#50ns
        cd.ForceNewCapture(forcenew)
        if (self.colors==3):
            cd.ScreenCapturetoArray3Color(self._data,self.x,self.y,self.w,self.h)
        if (self.colors==4):
            cd.ScreenCapturetoArray(self._data,self.x,self.y,self.w,self.h)#12ms
        g=bytearray(self._data)#.4ms
        frame = np.ctypeslib.as_array(g)#300ns
        #print(type(self._data),type(g),type(frame),frame.dtype)
        frame=np.reshape(frame,(self.h,self.w,self.colors))
        #print(frame[100][100][1])
        return frame
    def framexywh(self,x,y,w,h):
        self.changedims(x,y,w,h)
        return self.frame()
    def imshowclose(self):
        cd.CloseDisplayWindow()
    def imshow(self,title,nparray):#takes numpy array 4 COLOR ex:(1920x1080x4)
        import numpy as np
        #nparray=np.reshape(nparray,(nparray.shape[0]*))
        if ScreenClass.imageshowon==0:
            x,y=0,0
            if (nparray.shape[2]!=4):
                print("Error:ScreenClass.imageshowtakes numpy array 4 COLOR ex:(1920x1080x4)")
                return 0
            if ("imageshowwindow" in slconfigjson):
                x,y=slconfigjson["imageshowwindow"]
                ret=cd.DisplayImageInWindowSetXY(x,y)
                ScreenClass.imageshowon=1
        cd.DisplayImageInWindow.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C_CONTIGUOUS'),ctypes.c_size_t,ctypes.c_size_t,ctypes.c_char_p]
        arrayflat=nparray.ravel()#100ns
        ret=cd.DisplayImageInWindow(arrayflat,nparray.shape[1],nparray.shape[0],title.encode('utf8'))#.8ms
        if (ret==0):
            slconfigjson["imageshowwindow"]=[cd.DisplayImageInWindowGetX(),cd.DisplayImageInWindowGetY()]
            Utils.savejsonfile(os.path.join(os.path.dirname(__file__), 'config.json'),slconfigjson)
            ScreenClass.imageshowon=0
        Sleep(1)
        return ret
    def GetScreenChanges(self,x,y,w,h):
        import numpy as np
        #print("GetScreenChanges",self.sz/64);
        ct=cd.GetScreenChanges(self.ar8x8,self.x,self.y,self.w,self.h)
        
        #ArrayType = ctypes.c_int16*DataLength.value
        #addr = ctypes.addressof(Data.contents)
        a = np.frombuffer(self.ar8x8, dtype=np.uint32)
        return ct,a
        '''res=[]
        for i in range(ct):
            x1,y1=(int(self.ar8x8[i])*8,int(self.ar8x8[i+1])*8)
            #if (x1<x or x1>x+w or y1<y or y1>y+h):continue
            res.append((x1,y1))'''
        return res
    def changecountstart(self):
        cd.ScreenChangeCount(self.x,self.y,self.w,self.h)
    def changecountstop(self):
        ret=cd.ScreenChangeCount(self.x,self.y,self.w,self.h)
        return ret
    def FindImages(self,needle,haystack="screen.bmp"):
        MAXCOUNT=200
        self._img_x=(ctypes.c_int32 * MAXCOUNT)()
        self._img_y=(ctypes.c_int32 * MAXCOUNT)()
        ct=cd.NewFindImages(needle.encode('utf8'),haystack.encode('utf8'),self._img_x,self._img_y,MAXCOUNT)
        ret=[[ai, bi] for ai, bi in zip(list(self._img_x)[:ct],list(self._img_y)[:ct])]
        return ret
    def GetImageDimensions(self,needle):
        self._img_x=(ctypes.c_int32 )()
        self._img_y=(ctypes.c_int32)()
        ct=cd.GetImageDimensions(needle.encode('utf8'),self._img_x,self._img_y)
        return [self._img_x,self._img_y]
    def FindImagesOnScreen(self,needle,x1=0,y1=0,x2=0,y2=0, MAXCOUNT=200):
        self._img_x=(ctypes.c_int32 * MAXCOUNT)()
        self._img_y=(ctypes.c_int32 * MAXCOUNT)()
        ct=cd.NewFindImagesOnScreen(needle.encode('utf8'),self._img_x,self._img_y,MAXCOUNT,x1,y1,x2,y2)
        ret=[[ai, bi] for ai, bi in zip(list(self._img_x)[:ct],list(self._img_y)[:ct])]
        return ret
    def FindImageOnScreen(self,needle,x1=0,y1=0,x2=0,y2=0):
        ret=self.FindImagesOnScreen(needle,x1=x1,y1=y1,x2=x2,y2=y2, MAXCOUNT=1)
        return ret
    def FindColorsOnScreen(self,RGB=None,HSL=None,x1=0,y1=0,x2=0,y2=0):
        self._img_x=(ctypes.c_int32 * MAXCOUNT)()
        self._img_y=(ctypes.c_int32 * MAXCOUNT)()
        ct=0
        if (RGB!=None):
            ct=cd.FindRGBOnScreen(RGB,self._img_x,self._img_y,MAXCOUNT,x1,y1,x2,y2)
        elif(HSL!=None):
            ct=cd.FindHSLOnScreen(HSL,self._img_x,self._img_y,MAXCOUNT,x1,y1,x2,y2)
        ret=[[ai, bi] for ai, bi in zip(list(self._img_x)[:ct],list(self._img_y)[:ct])]
        return ret
    def printimagedata(self,needle):
        xy=cd.PrintImageData(needle.encode('utf8'))
        return [(xy>>16),xy&0xFFFF]
    def clampscreenx(v):
        return max(0, min(GetScreenX(), v))
    def clampscreeny(v):
        return max(0, min(cd.GetScreenY(), v))
class WindowsInfo(ctypes.Structure):
     _fields_ = [ ('x',ctypes.c_int32), ('y',ctypes.c_int32), ('w',ctypes.c_int32),('h',ctypes.c_int32),('name', ctypes.c_char * 200),('exename', ctypes.c_char * 200) ]
class WindowsUtils():
    triggers=[]
    clickarray=[0]*1024
    triggerthreadbool=0
    eventloopclose=0
    songs=[]
    def MessageBox(caption,title):
        return cd.WinMessageBox(caption.encode('utf8'),title.encode('utf8'))
    def DeleteFile(filename):
        return cd.DeleteSelectedFile(filename.encode('utf8'))
    def DeleteAllFilesInDirectory(directory,name=""):
        r=Utils.GetAllFilesInDirectory(directory,name)
        #ok=WindowsUtils.MessageBox("DeleteAll:%d"%(len(r)),str(r))
        #print(ok)
        #if (ok!=1): return
        start_path=directory
        res=[]
        ct=0
        for f in os.listdir(start_path):
            if (len(name)==0 or name in f):
                if (os.path.isfile(start_path+"\\"+f)==True):
                    WindowsUtils.DeleteFile(start_path+"\\"+f)
                    ct+=1
        return ct
    def _MP3Thread(filename):
        filename=os.path.join(os.path.dirname(__file__), 'filename')
        WindowsUtils.playmp3(filename)
        while(clock()<5000):
            WindowsUtils.DoEvents()
    def PlayMp3(mp3):
        Utils.DoThread(lambda x=mp3:WindowsUtils._MP3Thread(x))
    def Beep(frequency,duration):
        cd.sysbeep(frequency,duration)
    def DownloadFile(url,newfilename):
        cd.DownloadFileSite(url.encode('utf8'),newfilename.encode('utf8'))
    def clearwindow():
        print("__SLCLEARWINDOW")
    def printclear():
        print("__SLCLEARWINDOW")
    def vkcodetotext(i):
        out=(ctypes.c_char * 256)()
        cd.vkkeytotext(i,out)
        out=out.value.decode("utf-8")
        return out
    
    def _triggerthread():
        while(1):
            Sleep(10)
            for t in WindowsUtils.triggers:
                if (Keyboard.isclicked_complete(t[0])):
                    print("clicked",t[0])
                    if (t[1]):t[1]()
    def SetTrigger(key,func):
        if (WindowsUtils.triggerthreadbool==0):
            WindowsUtils.triggerthreadbool=1
            Utils.DoThread(WindowsUtils._triggerthread)
        WindowsUtils.triggers.append([key,func])
    def EventLoopClose():
        WindowsUtils.eventloopclose=1
    def EventLoop(closekey=0,func=None):
        while(GetKeyState(closekey)==0 and WindowsUtils.eventloopclose==0):
            cd.DoEvents()
            Sleep(10)
            if (func!=None):func()
    def DoEvents():
        cd.DoEvents()
        Sleep(1)
    def GetActiveWindowNum():
        return cd.GetActiveWindowNum()
    def ResizeWindow(windownum,w,h):
        return cd.ResizeWindowP(windownum,w,h)#ResizeWindow(windownum,w,h)
    def MoveWindow(windownum,x,y,w,h):
        return cd.MoveWindowP(windownum,x,y,w,h)#MoveWindow(windownum,x,y,w,h)
    def GetWindowInfo(windownum):
        winfo=WindowsInfo(0,0,0,0,b'kk')
        cd.GetWindowInfoPy(windownum,ctypes.pointer(winfo));
        return winfo
    def GetWindowXY(windownum):
        winfo=WindowsInfo(0,0,0,0,b'kk')
        cd.GetWindowInfoPy(windownum,ctypes.pointer(winfo));
        return winfo.x,winfo.y;
    def GetWindowXYWH(windownum):
        winfo=WindowsInfo(0,0,0,0,b'kk')
        cd.GetWindowInfoPy(windownum,ctypes.pointer(winfo));
        return winfo.x,winfo.y,winfo.w,winfo.h;
    def GetWindowExeAndTitle(windownum):
        winfo=WindowsInfo(0,0,0,0,b'kk')
        cd.GetWindowInfoPy(windownum,ctypes.pointer(winfo));
        return winfo.exename.decode('utf-8'),winfo.name.decode('utf-8');
    def OpenFolderExplorer(name):
        debugprint("explorer:",name)
        import subprocess
        name=os.path.normpath(name)
        print("explorer:",name)
        subprocess.Popen('explorer "%s"' %(name))
    def get_drives():
        drives = []
        letters_str=[]
        for x in range(65,91):
            letters_str.append(chr(x))
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in letters_str:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1

        return drives
    def MakeDir(path):
        return cd.MakeDirIfNotExist(path.encode('utf8'))
    def RecentFiles(path):
        filelist=[]
        for f in os.listdir(path):
            if (os.path.isfile(path+"\\"+f)):
                filelist.append([f,os.path.getmtime(path+"\\"+f)])
        rsort=sorted(filelist,key=lambda x:x[1],reverse = True)
        return rsort
    def FileExists(string):
        return cd.FileExistsW(string.encode('utf8'))
    def getdirectorysize(fullpath,clearcache=False,ext="*.*"):
        cache=Utils.cache
        if fullpath not in cache or clearcache==True:
            #p = ctypes.create_unicode_buffer(fullpath)
            cd.getdirectorysize.restype = ctypes.c_float
            sz = cd.getdirectorysize(fullpath.encode('utf8'),ext.encode('utf8'))
            ct= cd.getcurrentfilecount()
            ct_ext= cd.getcurrentextensioncount()
            value=(sz,ct,ct_ext)
            cache[fullpath] = value
        else:
            value=cache[fullpath]
        return value
    def ProcessHelpString(helpstr):
        _data=(ctypes.c_int8 * 50000*250)()
        cd.ProcessHelpDataLibW(helpstr.encode('utf8'),_data)
        return _data
    def randomstring():
        cd.RandomString.restype = ctypes.c_char_p
        string=cd.RandomString().decode('utf-8')
        return string
    def GetWindowsVersion():
        import winreg as reg
        from datetime import datetime
        date=""
        try:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            secs = reg.QueryValueEx(key, 'InstallDate')[0]
            date = datetime.fromtimestamp(secs)
        except:
            pass
        return date
    def loadcsvsl(filename, shape=(0,0),delimiter=ord(','), skiprows=0, dtype=int):
        import numpy as np
        if (shape==(0,0)):
            _datashape=(ctypes.c_int32 * 2)()
            rows=cd.GetLinesCsv(filename.encode('utf8'),_datashape,delimiter,skiprows)
            shape=(_datashape[0],_datashape[1])
        c_dtype=np.ctypeslib.as_ctypes_type(dtype)
        sz=np.prod(shape[0]*shape[1])
        print(shape,c_dtype,sz)
        _data=(c_dtype * sz)()
        #LoadCsv(char* str, int* returnbuf, int delimiter, int rows,int columns,int dtype, int skiprows)
        dtypename=ord('i')
        if (dtype==float):dtypename=ord('f')
        rows=cd.LoadCsv(filename.encode('utf8'),_data,delimiter,shape[1],dtypename,1)
        frame = np.ctypeslib.as_array(_data)
        frame=np.reshape(frame,shape)
        return frame
    def playmp3(mp3):
        WindowsUtils.songs.append(mp3)
        cd.play_mp3(mp3.encode('utf8'),len(WindowsUtils.songs)-1)
    def stopmp3(mp3):
        ind=WindowsUtils.songs.index(mp3)
        cd.stop_play_mp3(mp3,ind)




###########################Windows Utils#######################################


def BlockMenuInput(on,time=2000):
    BlockMenuInput=cd.blockinput(on,time)#(0 or 1, all keyboard and left mouse)
def BlockKeyInput(key,on,time=10000):
    cd.blockkeyinput(key,on,time)#specific key block BlockKeyInput(key,0 or 1)
def BlockMouseInput(mousekey,on,time=3000):
    cd.blockmouseinput(mousekey,on,time)#specific mouse block BlockMouseInput(mouseval,0 or 1)

def KillPython():
    cd.BotExit();
    return;
    print(os.getpid())
    PROCESS_TERMINATE = 1
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, os.getpid())
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.CloseHandle(handle)


#######################################################################Drawing##############################

def ScreenCaptureToFile(name,x=0,y=0,w=-1,h=-1):
    cd.ScreenCapturetoFileW(name.encode('utf8'),x,y,w,h)

def DrawString(string,x,y,color=0xFF000000,fontnum=0):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawStringW(p,x,y,color,fontnum)

def DrawStringBox(string,x,y,w,h,color,fontnum=0):#drawstring inside box
    p = ctypes.create_unicode_buffer(string)
    cd.DrawStringBoxW(p,x,y,w,h,color,fontnum)

DrawSolidColor=cd.DrawSolidColor#int DrawSolidColor(int x, int y, int w, int h,int color)
DrawLineColor=cd.DrawLineColor#int DrawLineColor(int x, int y, int x2, int y2, int color,int thick)
DrawBox=cd.DrawBox  #int DrawBox(int x, int y, int w, int h, int color,int thick)





############################################################Image/Sprite Utilities##############################


def GetScreenBGRA(x,y):#(b,g,r,a)
    target=cd.GetScreenBGRA(x,y)
    lc=(0x000000FF & target,(0x0000FF00 & target)>>8,(0x00FF0000 & target)>>16,(0xFF000000 & target)>>24)
    #lc=((0xFF000000 & target)>>24,(0x00FF0000 & target)>>16,(0x00FF0000 & target)>>8,(0xFF000000 & target))
    return lc
def GetScreenYUV(x,y):
    target=cd.GetScreenYUV(x,y)
    lc=((0x0000FF00 & target)>>8,(0x00FF0000 & target)>>16,(0xFF000000 & target)>>24)
    return lc
def GetScreenHSL(x,y):
    target=cd.GetScreenHSL(x,y)
    lc=((0x0000FF00 & target)>>8,(0x00FF0000 & target)>>16,(0xFF000000 & target)>>24)
    return lc

def ReloadSprite(string):
    p = ctypes.create_unicode_buffer(string)
    cd.ReloadSpriteW(p)

def CreateFont(name,size,number):
    #print(name,size,number)
    p = ctypes.create_unicode_buffer(name)
    cd.HoloCreateFontW(p,size,number)

def DrawSpriteNaked(string,x,y):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawSpriteNakedW(p,ctypes.c_float(x),ctypes.c_float(y))
  
def DrawSprite(string,x,y,srcx,srcy,w,h):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawSpriteWA(p,ctypes.c_float(x),ctypes.c_float(y),srcx,srcy,w,h)

def DrawSpriteIndex(string,x,y,w,h,index):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawSpriteWI(p,ctypes.c_float(x),ctypes.c_float(y),w,h,index)

def DrawSpriteIndexMouseOver(string,x,y,w,h,index):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawSpriteWIMouse(p,ctypes.c_float(x),ctypes.c_float(y),w,h,index)

def DrawSpriteIndexMouseOverL(string,x,y,w,h,index):
    p = ctypes.create_unicode_buffer(string)
    cd.DrawSpriteWIMouseL(p,ctypes.c_float(x),ctypes.c_float(y),w,h,index)

class ScreenGrabClass():
    
    def __init__(self):
        self.x=-100
        self.y=-1;self.on=0
        self.dx=0;self.ax=0
        self.dy=0;self.ay=0
        self.on=0
    def start(self):
        if (self.on==0):
            self.on=1
            self.x=GetMouseX();
            self.y=GetMouseY()
            self.ax=self.x;self.ay=self.y;
        self.dx=GetMouseX()-self.x
        self.dy=GetMouseY()-self.y
        if (self.dx<0): 
            self.ax=self.x+self.dx;self.dx*=-1
        if (self.dy<0): self.ay=self.y+self.dy;self.dy*=-1;
        
        DrawBox(self.ax,self.ay,self.dx,self.dy,0xFF00CC55,2)  
    def stop(self):
        if (self.on==0): return None
        data=[self.ax+2,self.ay+1,self.dx-2,self.dy-2]
        self.on=0
        return data
    def isrunning(self):
        return (self.on==1)

class ConsoleClass:
    instances = []
    def print_to_string(*args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        return contents
    def __init__(self,basew=400,baseh=400,fontsize=10,textcolor=0xFF00FF00,clickthru=1,trans=20,xclosesapp=0,background="console.bmp",title="none"):
        self.basew=basew
        self.baseh=baseh
        self.basex=GetScreenX()-self.basew
        self.basey=140
        #self.box=[self.basex,self.basey,663,663]
        self.basecolor=0x000000
        self.text=[]
        self.textcolors=[]
        self.drawtext=""
        self.intro=-1
        self.fontsize=fontsize
        self.background=background
        ConsoleClass.instances.append(self)
        self.fontnum=OldGui.GetNextFont()
        self.menuon=1
        self.movelocked=0
        self.movex=0
        self.movey=0
        self.mblocked=0;
        self.lastks=0
        self.consoleon=1
        self.drawsprite=None
        self.textsz=0
        self.adlocked=0
        self.clickthru=clickthru
        self.textcolor=textcolor
        self.trans=(int(((100-trans)*255)/100))%256
        self.drawtextsep="+"
        self.xclosesapp=xclosesapp
        self.lastr=0
        self.maxsz=int(self.baseh/(self.fontsize+4))
        self.scrollpos=self.maxsz+1
        self.scrolllock=1
        self.realmaxsz=0;
        self.fontname="Arial"
    def destroy(self):
        BlockMouseInput(1,0);
        ConsoleClass.instances.remove(self)
    def getmouseroll(self):
        r=cd.getmouseroll()
        dr=r-self.lastr
        #dr=(dr/abs(dr))
        self.lastr=r
        if (dr!=0):
            dr=Utils.CLAMP(dr,-2,2)
            #print("mouseroll:"+str(dr)+":"+str(self.scrollpos))
            self.scrolllock=0
            self.scrollpos-=dr
            self.scrollpos=min(self.textsz+1,self.scrollpos)
            #self.scrollpos=max(self.scrollpos,self.realmaxsz)
        return dr
    '''def calcscroll(self):
        self.maxsz=int(self.baseh/(self.fontsize+4))
        if (self.scrollpos==self.textsz):
            #self.scrollpos=self.textsz-self.maxsz
            self.scrolllock=1
        self.scrollpos=max(self.scrollpos,self.maxsz)
        print(self.scrollpos)'''
    def calctextsize(self):
        sz=0
        self.textsz=0
        self.maxsz=int(self.baseh/(self.fontsize+4))
        i=0
        for sentence in self.text[-1:0:-1]:
            sz+=int(len(sentence)*self.fontsize/self.basew)+1
            self.textsz+=1
            m=int(len(sentence)*self.fontsize/self.basew)
            if ((self.fontsize+4)*i<self.baseh+30):i+=m+1;
            self.realmaxsz=i;
        #print("realmax"+str(self.realmaxsz)+"cur"+str(self.textsz))
    def clear(self):
        self.text=[]
    def printx(self,t,color=None,sep=None):
        #self.scrollpos=max(self.scrollpos,self.realmaxsz)
        
        if (self.scrollpos>=self.textsz):
            self.scrolllock=1
        t=ConsoleClass.print_to_string(t)
        sz=0
        if (sep!=None):
            s=t.split(sep)
            for a in s:
                self.text.append(a)
                if (color!=None):self.textcolors.append(color);
                else:self.textcolors.append(self.textcolor);
        else :
            self.text.append(t)
            if (color!=None):self.textcolors.append(color);
            else:self.textcolors.append(self.textcolor);
        
        self.calctextsize()
        if (self.scrolllock==1):
            if (self.textsz>=self.scrollpos):self.scrollpos=self.textsz+1;
    def out(self,*args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        self.printx(contents)
    def printf(self,*args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        self.printx(contents)
    def drawx(self,t):
        if (self.consoleon==1 and self.menuon==1):
            self.drawsprite=t
            ReloadSprite(t)
    def settextcolor(self,t):
        self.textcolor=t
    def setxclosesapp(self,t):
        self.xclosesapp=t
    def setclickthru(self,t):
        self.clickthru=t
    def settransparency(self,t):
        self.trans=(int(((100-t)*256)/100))%256
        #print(t)
    def bar(self,t,sep="+"):
        self.drawtext=t
        self.drawtextsep=sep
    def barx(self,t):
        self.drawtext=t
    def barf(self,*args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        self.barx(contents)
    def switchonoff(self,t):
        self.consoleon=t#(self.consoleon+1)%2
    def switchon(self):
        self.consoleon=1#(self.consoleon+1)%2
    def switchoff(self):
        self.consoleon=0#(self.consoleon+1)%2
    def Move(self,dx,dy):
        self.basex+=dx;self.basey+=dy;
        self.basex=max(self.basex,0);self.basey=max(self.basey,0);
    def MoveXY(self,x,y):
        dx=x-self.basex;dy=y-self.basey;
        self.Move(dx,dy)
    def draw(self):
        if (self.consoleon==0): return
        keystate=GetKeyState(1)
        keyclick=0
        keyfinishclick=0
        if (keystate==1 and self.lastks==0):
            keyclick=1
        if (keystate==0 and self.lastks==1):
            keyfinishclick=1
        self.lastks=keystate
        
        w=min(568-120,max(self.basew-90,0))
        DrawSprite("consolemenumin.bmp",self.basex,self.basey-30,0,0,w,30);
        w=min(568,self.basew-30)#max(self.basew-570,0)
        if (self.menuon==0): DrawSprite("consolemenumin.bmp",self.basex+self.basew-90,self.basey-30,600-90,0,90,30);
        else : DrawSprite("consolemenumax.bmp",self.basex+self.basew-90,self.basey-30,600-90,0,90,30);
        x=GetMouseX()
        y=GetMouseY()
        if (self.adlocked==1):
            if (keystate==0):
                self.adlocked=0
                self.basew=max(120,self.basew);self.baseh=max(0,self.baseh)
                self.calctextsize()
            else:
                dx=x-self.movex;dy=y-self.movey;
                self.basew+=dx;self.baseh+=dy;
                self.movex=x;self.movey=y
                self.movex=x
        if (self.movelocked==1):
            if (keystate==0):
                self.movelocked=0
            else:
                dx=x-self.movex;dy=y-self.movey;
                self.Move(dx,dy)
                self.movey=y
                self.movex=x
        if (x<self.basex+self.basew and x>self.basex and y<self.basey+self.baseh and y>self.basey-31):#all window
            dr=self.getmouseroll()
                
            if (self.trans>64 and self.clickthru==0):
                if (self.menuon==1):
                    BlockMouseInput(1,1);
                    self.mblocked=1;
                else :
                    BlockMouseInput(1,0);
                    self.mblocked=0;
            if (x<self.basex+self.basew and y>self.basey+self.baseh-30 and y<self.basey+self.baseh and x>self.basex+self.basew-30):#bottom left drag resize
                BlockMouseInput(1,1);
                self.mblocked=1;
                if (keystate!=0):
                    if (self.adlocked==0 and keyclick==1):
                        self.adlocked=1
                        self.movey=y
                        self.movex=x
            else:
                if (x<self.basex+self.basew and x>self.basex and y<self.basey and y>self.basey-31):#top bar
                    BlockMouseInput(1,1);
                    self.mblocked=1;
                    '''if (x<self.basex+30 or x> self.basex+self.basew-89):                   #middle of top bar is click thru
                        BlockMouseInput(1,1);
                        self.mblocked=1;
                    else :
                        BlockMouseInput(1,0);'''
                    if (x<self.basex+self.basew-29 and x> self.basex+self.basew-59):       #minimize/maximize of top bar
                        if (keyfinishclick==1):
                            if (self.menuon==1):
                                self.minbasex=self.basex;self.minbasey=self.basey;
                                self.MoveXY(GetScreenX()-self.basew-70,GetScreenY()-70)
                            if (self.menuon==0):
                                self.MoveXY(self.minbasex,self.minbasey)
                            self.menuon=(self.menuon+1)%2
                            return
                        #if (keystate!=0 and keyclick==1):
                            #self.menuon=(self.menuon+1)%2
                    if (x<self.basex+self.basew-59 and x> self.basex+self.basew-89):       #transparent of top bar
                        if (keystate!=0 and keyclick==1):
                            #if (keystate==0 and self.clicked==1):
                            self.trans=(self.trans-64)%256
                    if (x>self.basex+self.basew-29):                                        #close(x) of top bar
                        if (keystate!=0 and keyclick==1):
                            self.consoleon=0
                            if (self.xclosesapp==1):
                                print("ending")
                                KillPython()
                            BlockMouseInput(1,0);
                    if (x<self.basex+self.basew-89 and x>self.basex):                                  #move of top bar
                        if (keystate!=0):
                            if (self.movelocked==0 and keyclick==1):
                                self.movelocked=1
                                self.movey=y
                                self.movex=x
                else :
                    if (self.clickthru==1):
                        BlockMouseInput(1,0);
                        self.mblocked=0;
        else :
            if (self.mblocked==1):
                BlockMouseInput(1,0);
                self.mblocked=0;
          
        if (self.intro==-1):
            if (OldGui.HoloGraphicsCallback==None): return
            CreateFont( self.fontname,self.fontsize,self.fontnum)
            self.intro=0
        if (self.intro==0 and self.menuon==1):
            DrawSolidColor(self.basex,self.basey,self.basew,self.baseh,self.basecolor +self.trans*16777216)
            DrawSprite("consolemenumin.bmp",self.basex+self.basew-30,self.basey+self.baseh-30,0,0,30,30)
            if (self.drawsprite!=None):
                DrawSpriteNaked(self.drawsprite,self.basex+100,self.basey+100)
            i=0;sz=0;ct=0
            end=min(self.textsz+1,self.scrollpos);#min(self.textsz+1,self.maxsz+self.scrollpos)
            for sentence in self.text[end:0:-1]:
                ct+=1
                m=int(len(sentence)*self.fontsize/self.basew)
                i+=m+1
                if ((self.fontsize+4)*i>self.baseh-60):break;
            start=max(end-ct-1,0)
            #print(start,end,self.scrollpos)+-`
            i=0
            #for sentence in self.text[-1-self.textsz-self.scrollpos:end:]:
            #print(start,end)
            b=start
            for sentence in self.text[start:end:]:
                m=int(len(sentence)*self.fontsize/self.basew)
                DrawStringBox(sentence,self.basex,self.basey+(self.fontsize+4)*i,self.basew,100,self.textcolors[b],self.fontnum)
                i+=m+1
                b+=1
                #if ((self.fontsize+4)*i>self.baseh):break;
            sep=self.drawtextsep
            if (sep!=None):
                s=self.drawtext.split(sep)
                i=len(s)
                for a in s:
                    DrawStringBox(a,self.basex+30,self.basey+self.baseh-(self.fontsize+4)*i,self.basew,100,self.textcolor,self.fontnum)
                    i-=1
            else :
                DrawStringBox(self.drawtext,self.basex+30,self.basey+self.baseh-(self.fontsize+4),self.basew,100,self.textcolor,self.fontnum)
class IntroSheet:
    def __init__(self,background="scrollbg.bmp",text="Intro Text separated by +",fontsize=30):
        self.text=text.split('+')
        self.intro=-1
        self.fontsize=fontsize
        self.background=background
        self.fontname="Arial"
        
    def draw(self):
        if (self.intro==-1):
            if (OldGui.HoloGraphicsCallback==None): return
            
            k=GetKeyState(VK["LeftButton"])
            self.fontnum=OldGui.GetNextFont()
            CreateFont( self.fontname,self.fontsize,self.fontnum)
            self.introsprite=Sprite(self.background,200,200,663,378)
            self.intro=0
        if (self.intro==0):
            self.introsprite.draw()
            i=0
            for sentence in self.text:
                DrawStringBox(sentence,200,200+(self.fontsize+20)*i,700,300,0xFF000000,self.fontnum)
                i+=1
            
            DrawStringBox("[x]",450,500,600,300,0xFF000000,self.fontnum)
            k=GetKeyState(VK["LeftButton"])
            if (k!=0):self.intro=1




   


class Sprite:
    def __init__(self, filename, x,y,w,h,index=0,dx=0,dy=0,di=0):
        self.filename = filename
        self.dx = dx
        self.dy = dy
        self.di = di
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.index=index
    def outdata(self):
        print(self.x,self.y,self.w,self.h,self.index,self.filename);
    def draw(self):
        self.index+=self.di
        DrawSpriteIndex(self.filename,self.x,self.y,self.w,self.h,self.index);
class BounceSprite(Sprite):
    def updateanddraw(self):
        if (self.x>GetScreenX() or self.x<0): self.dx*=-1;
        if (self.y>GetScreenY() or self.y<0): self.dy*=-1;
        self.x+=self.dx
        self.y+=self.dy
        self.index+=self.di
        DrawSpriteIndex(self.filename,self.x,self.y,self.w,self.h,self.index);
    def changespeed(self,dx,dy,di):
        self.dx = dx*Utils.signedcmp(self.dx,0)
        self.dy = dy*Utils.signedcmp(self.dy,0)
        self.di = di
class TextSprite:
    def __init__(self,text,x,y,c,w=200,h=40,text2="",base="whitebackground.bmp"):
        self.text = text
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color=c
        self.base=base
        self.text2=text2
    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy
    def updateanddraw(self,status,mtype,extradata):
        if (self.text.find(".bmp")==-1):
            DrawSpriteIndexMouseOverL(self.base,self.x,self.y,self.w,self.h,0);
        else:
            DrawSpriteIndexMouseOver(self.text,self.x,self.y,self.w,self.h,0);
        if (mtype==4):
            if (self.text.find(".bmp")==-1):
                DrawString(self.text,self.x,self.y,self.color)
        if (mtype==0):
            DrawString(self.text,self.x,self.y,self.color)
            DrawSpriteIndexMouseOverL("menudropdown.bmp",self.x+180,self.y,20,40,0);
        if (mtype==1):
            DrawString(self.text,self.x+40,self.y+10,self.color)
            if (status==0):
                DrawSpriteIndexMouseOverL("checkboxempty.bmp",self.x,self.y,40,40,0);
            else:
                DrawSpriteIndexMouseOverL("checkboxfull.bmp",self.x,self.y,40,40,0);
        if (mtype==2):
            DrawString(self.text,self.x,self.y,self.color)
            DrawSpriteIndexMouseOverL("sliderback.bmp",self.x+100,self.y+20,100,20,0);
            DrawSpriteIndexMouseOverL("slidergrip.bmp",self.x+status+90,self.y+20,20,20,0);
            DrawString(self.text2,self.x+98,self.y,self.color)
        if (mtype==3):
            DrawString(self.text,self.x,self.y,self.color)
            if (extradata==1):
                DrawSpriteIndexMouseOverL("textboxfocus.bmp",self.x+100,self.y+10,100,20,0);
            else: DrawSpriteIndexMouseOverL("textbox.bmp",self.x+100,self.y+10,100,20,0);
            DrawString(str(status),self.x+100,self.y+10,self.color)
        if (mtype==5):
            if (status!=1):
                DrawSpriteIndexMouseOverL("button2.bmp",self.x+90,self.y,94,30,0);
            else:
                DrawSpriteNaked("button3.bmp",self.x+90,self.y)
            DrawString(self.text,self.x,self.y,self.color)
            DrawString(self.text2,self.x+98,self.y+8,self.color)
           
    def changetext(self,text):
        self.text = text
    def changetext2(self,text2):
        self.text2 = text2
    def changexy(self,text,x,y):
        self.x = x
        self.y = y

class BoxClass:
    #instances = []
    def __init__(self,x,y,w,h,color,num,label=""):
        self.x=x; self.y=y; self.w=w; self.h=h; self.color=color; self.num=num;self.label=label
        #BoxClass.instances.append(self)
    def draw(self):
        DrawBox(self.x,self.y,self.w,self.h,self.color,self.num)
        if (len(self.label)>0):
            DrawString(self.label,self.x+10,self.y-10,self.color)
class TimerClass:
    instances = []
    def __init__(self,timer,callback):
        self.timer=timer
        self.callback=callback
        self.clock=cd.clocktime()-self.timer+500
        TimerClass.instances.append(self)
        self.enabled=False
    def dotimer(self):
        if (self.enabled==True):
            if (cd.clocktime()-self.clock>self.timer):
                self.callback()
                self.clock=cd.clocktime()

    def enable(self):
        self.enabled=True
    def disable(self):
        self.enabled=False


class MenuClass:
    instances = []
    
    def __init__(self,timer,callback):
        self.d=dictio
        self.callback=callback
        MenuClass.instances.append(self)
    #Menu Format{id:["type","display text or image",parentid,status]}
    def __init__(self,dictio,callback,menubmp="defaultmenu.bmp",activatebutton=0x0,hardblockinput=0,basex=50,basey=120,width=200,height=40,splitstring="#"):
        self.menubmp=menubmp
        self.d=dictio
        self.callback=callback
        self.sl=[]
        self.rects=[]
        self.oldstatus=[]
        self.chain=[0]*10
        self.active=0
        self.activeparent=0
        self.activatebutton=activatebutton
        #BlockKeyInput(activatebutton,1)
        self.hardblockinput=hardblockinput
        self.h=[0]*100
        #self.h[0]=1
        self.splitstring=splitstring
        self.basex=basex
        self.basey=basey
        self.basew=200
        defaultw=width
        defaulth=height
        self.accepttext=-1
        self.menuon=1
        self.textbox=""
        self.blockinput=0
        self.mouseonmenu=0
        self.hardblockinput=0
        self.movelocked=0
        self.movex=0
        self.movey=0
        self.mblocked=0;
        self.clicked=0
        self.close=0
        self.lastks=0
        self.mouseonmenuck=0
        self.minbasex=10
        self.minbasey=GetScreenY()-100
        
        #x = threading.Thread(target=self.mousethread, args=[self,])
        #x.start()
        #hk=Hotkey()
        #hk.SetClickTrigger(key,self.retfunc,x,y,w,h)
        for key, value in self.d.items():
            if (value[2]==0):
                self.d[key].append(0)
            else:
                try:
                    par=value[2]
                    depth=self.d[par][4]+1
                    self.d[key].append(depth)
                except IndexError:
                    print("Menu Initializer fail, key %d has parent %d which doesnt exist yet" %(key,par))
                    raise
        i=0
        for key, value in self.d.items():
            parent=value[2]
            depth=value[4]
            status=value[3]
            h=self.h[parent]
            mtype=0
            text2=""
            if ("Check" in value[0]):
                mtype=1
            if ("Slider" in value[0]):
                mtype=2
            if ("Text" in value[0]):
                mtype=3
                status=str(value[3])
            if ("Display" in value[0]):
                mtype=4
            if ("Button" in value[0]):
                mtype=5
                text2="clickme"
            controltext=str(value[1]).split(self.splitstring)
            controltext.append(text2)
            #self.sl.append(TextSprite(str(i)+" "+str(depth)+" "+str(parent)+value[1],basex+depth*defaultw,h*defaulth+basey,0xFF000000,defaultw,defaulth))
            self.sl.append(TextSprite(controltext[0],basex+depth*defaultw,h*defaulth+basey,0xFF000000,defaultw,defaulth,controltext[1]))
            #RECTS(0x,1y,2x2,3y2,4parent,5depth,6key,7mtype,8status)
            self.rects.append([basex+depth*defaultw,h*defaulth+basey,basex+defaultw+depth*defaultw,h*defaulth+basey+defaulth,parent,depth,i,mtype,status])
            self.oldstatus.append(status)
            #hk.SetClickTrigger(1,self.retfunc,basex,self.h*defaulth+basey,defaultw,defaulth,{'key':key})
            self.h[parent]+=1
            if (i!=0):
                self.h[i]=h
            i+=1
        MenuClass.instances.append(self)
    def Move(self,dx,dy):
        self.basex+=dx;self.basey+=dy;
        for t in self.sl:
            t.move(dx,dy)
        for t in self.rects:
            t[0]+=dx;t[2]+=dx;
            t[1]+=dy;t[3]+=dy
    def MoveXY(self,x,y):
        dx=x-self.basex;dy=y-self.basey;
        self.Move(dx,dy)
    def draw(self):
    
        
        leftmousestate=GetKeyState(1)
        keyclick=0;leftmousefinishclick=0
        if (leftmousestate==1 and self.lastks==0):
            keyclick=1
        if (leftmousestate==0 and self.lastks==1):
            leftmousefinishclick=1
        self.lastks=leftmousestate
        if (self.menuon==0):
            DrawSpriteNaked("defaultmenumin.bmp",self.basex,self.basey-30);
        else : DrawSpriteIndexMouseOverL("defaultmenumax.bmp",self.basex,self.basey-30,200,30,0);
        x=GetMouseX()
        y=GetMouseY()
        self.mouseonmenu=0
        if (self.movelocked==1):
            if (leftmousestate==0):
                self.movelocked=0
            else:
                dx=x-self.movex;dy=y-self.movey;
                self.movey=y
                self.movex=x
                self.Move(dx,dy)
        if (x<self.basex+self.basew and x>self.basex and y<self.basey and y>self.basey-31):
            BlockMouseInput(1,1);
            self.mblocked=1;
            if (x<self.basex+self.basew-29 and x> self.basex+self.basew-59):
                if (leftmousefinishclick==1):
                    '''if (self.menuon==1):
                        self.minbasex=self.basex;self.minbasey=self.basey;
                        self.MoveXY(10,GetScreenY()-70)
                    if (self.menuon==0):
                        self.MoveXY(self.minbasex,self.minbasey)'''
                    self.menuon=(self.menuon+1)%2
                    return
                    #self.movelocked=1
            if (x>self.basex+self.basew-29):
                if (leftmousefinishclick==1):
                    self.close=1
                    KillPython()
                    #cd.BotExit()
                    #sys.exit();
            if (x<self.basex+self.basew-59):
                if (leftmousestate!=0):
                    if (self.movelocked==0 and keyclick==1):
                        self.movelocked=1
                        self.movey=y
                        self.movex=x
        else :
            if (self.mblocked==1):
                BlockMouseInput(1,0);
                self.mblocked=0;            
        '''if (x<self.basex+200 and x>self.basex and y<self.basey and y>self.basey-31):
            BlockMouseInput(1,1);
            self.mblocked=1;
            if (x<self.basex+171 and x> self.basex+141):
                if (leftmousestate!=0 and keyclick==1):
                    #if (leftmousestate==0 and self.clicked==1):
                    self.menuon=(self.menuon+1)%2
            if (x<self.basex+141):
                if (leftmousestate!=0):
                    if (self.movelocked==0 and keyclick==1):
                        self.movelocked=1
                        self.movey=y
                        self.movex=x
            if (x>self.basex+171):
                if (leftmousestate!=0):
                    sys.exit();
        else :
            if (self.mblocked==1):
                BlockMouseInput(1,0);
                self.mblocked=0;'''
        while(1):####KEY PROCESSING##
            k=cd.getlastkey(250)
            
            if (k==0): break
            if (k==self.activatebutton):   #Ctrl Shift scancode
                self.menuon=(self.menuon+1)%2
                Sleep(20)
                if (self.hardblockinput==1):
                    BlockMenuInput(self.menuon)
                self.accepttext=-1
            if (self.accepttext!=-1 and self.menuon==1):
                tx=self.rects[self.accepttext][8]
                if (k==VK["Back"]):
                    tx=tx[:-1]
                elif (k==VK["Delete"]):
                    tx=""
                else:
                    if (k==187):tx+='=';
                    if (k==189):tx+='-';
                    if (k==190):tx+='.';
                    if (k==188):tx+=",";
                    if (k==0x2E):tx="";
                    if (k==0x09):tx+="   ";
                    if (k==0x2E):tx="";
                    if (k==0x2E):tx="";
                    if (k>=0x30 and k<=0x5A):
                        shiftstate=GetKeyState(16)#Shift
                        if (shiftstate==0):
                            tx=tx+chr(k).lower()
                        else:tx=tx+chr(k)
                #print(self.textbox)
                self.rects[self.accepttext][8]=tx
                if (self.callback!=0):
                    self.callback(self.rects[self.accepttext][6],tx)
        if (self.menuon==0):
            BlockMenuInput(0)
            self.blockinput=0
            return
       
       
        self.mouseonmenu=0
        
        if (keyclick!=0 and self.accepttext!=-1):self.accepttext=-1

        ####FOR ALL GUI ELEMENT##
        for index in range(len(self.rects)):
            g=self.rects[index]
            par=g[4]
            depth=g[5]
            key=g[6]
            mtype=g[7]
            status=g[8]
            #g=self.rects[i]
            ####MOUSE PROCESSING####
            if (x<g[2] and x>g[0] and y<g[3] and y>g[1] and (g[4] in self.chain)):
                #if (mtype==5 and leftmousestate==0 and status==1):status=2
                if (leftmousestate!=0):
                    if (mtype==5):
                        status=1
                        g[8]=status
                        self.rects[index]=g
                        self.oldstatus[index]=1
                    if (mtype==2):
                        status=x-(g[0]+100)
                        #ClampVal = lambda value, minv, maxv: max(min(value, maxv), minv)
                        status=Utils.CLAMP(status,0,100)
                        if (g[8]!=status):
                            g[8]=status
                            self.rects[index]=g
                            ar={"args":status}
                            self.callback(key,status)
                if (leftmousefinishclick!=0):
                    self.accepttext=-1
                    if (mtype==5):
                        status=2
                        if (g[8]!=status):
                            g[8]=status
                            self.rects[index]=g
                        self.callback(key,status)
                        
                    if (mtype==1):
                        status=(status+1)%2
                        if (g[8]!=status):
                            g[8]=status
                            self.rects[index]=g
                            ar={"args":status}
                            self.callback(key,status)
                    if (mtype==3):
                        self.accepttext=index
                        
                        
                    #margs={'index':self.active}
                    #x = threading.Thread(target=f.func, kwargs=margs)
                    #x.start()
                self.mouseonmenuck=cd.clocktime()
                self.mouseonmenu=1
                self.active=index
                self.chain[depth]=index
                self.chain[depth+1:]=[0]*(len(self.chain)-(depth+1))
                #self.chain[depth+2]=0
                #self.chain[(g[5])
                
            ########DRAW ALL #########
            extradata=0
            if (self.accepttext==index):
                extradata=1
            if (par in self.chain):
                self.sl[index].updateanddraw(status,mtype,extradata)
        if (cd.clocktime()-self.mouseonmenuck>2000):
            self.active=0
            self.chain[depth]=0
            self.chain[1:]=[0]*(len(self.chain)-(1))
        if (self.hardblockinput==0):
            if (self.mouseonmenu==1 and self.menuon==1):
                BlockMenuInput(1)
                self.blockinput=1
            else:
                if (self.blockinput==1):
                    BlockMenuInput(0)
                    self.blockinput=0
    def destroy(self):
        BlockMenuInput(0)
        MenuClass.instances.remove(self)
    def changestatus(self,key,status):
        #key=key-1
        c=self.rects[key]
        c[8]=status
        self.rects[key]=c
        return status
    def changetext(self,id,text):
        self.sl[id].changetext(text)
    def changetext2(self,id,text2):
        self.sl[id].changetext2(text2)
    def getstatus(self,key):
        #key=key-1
        return self.rects[key][8]
    def isstatuschanged(self,key):
        #key=key-1
        res=0
        if (self.rects[key][8]!=self.oldstatus[key]):
            res=1
        self.oldstatus[key]=self.rects[key][8]
        return res
    def retfunc(self,key):
        x=GetMouseX()
        y=GetMouseY()
        print("key",key,x,y)
        self.callback(key)
        return

class OldGui:
    defaultfont=100
    HoloGraphicsCallback=None
    currentglobals=set()
    def __init__(self):
        pass
    def SetFont(fontname):
        cd.SetSLFont(fontname.encode('utf8'))
    def GetNextFont():
        OldGui.defaultfont-=1
        return OldGui.defaultfont
    def SetKillKey(a,b):
        cd.SetKillKey(a,b)
    def HoloGraphicsCallbackThread():
        try:
            while(1):
               
                ret=cd.initoverlay()
                if (ret==1):
                    #if (HoloConsoleFunc is not None): return;
                    #r=HoloGraphicsCallback()
                    for a in TimerClass.instances:
                        a.dotimer()
                    for a in ConsoleClass.instances:
                        a.draw()
                    for a in MenuClass.instances:
                        a.draw()
                    r=OldGui.HoloGraphicsCallback()
                    #if (r==0): break
                    cd.presentoverlay()
                    cd.sleep(15);
                #Sleep(20)
        except Exception:
            print("exception graphics thread")
            for a in ConsoleClass.instances:
                a.destroy()
            for a in MenuClass.instances:
                a.destroy()
            raise
    def ScriptLinkLoopFunc():
        if (GetKeyState(VK["Escape"])!=0):
            KillPython()
            pass
    def loop(func=ScriptLinkLoopFunc):
        while(1):
            func()
            Sleep(10)
            cd.DoEvents();
    def turnfpsoff():
        cd.turnfpsoff()
    def startgui(func,name="overlay",w=0,h=0,hook="driver"):
        if (OldGui.HoloGraphicsCallback is not None): return;
        r=0
        if (hook=="driver"):r=Keyboard.StartDriver()
        elif (hook=="keyboard"):r=Keyboard.StartHooks()
        if (r==0):print("failed to hook keyboard")
        OldGui.HoloGraphicsCallback=func
        cd.SpawnWindow(name.encode('utf8'),w,h)
        x = threading.Thread(target=OldGui.HoloGraphicsCallbackThread, args=[])
        x.daemon = True
        x.start()
    def printdictvars(dic,tabbed=0):
        modulect=0;functionct=0;res=""
        for k,v in dic.items():
            if (not isinstance(v, types.ModuleType)):
                if (not isinstance(v, types.FunctionType)):
                    if (k not in OldGui.currentglobals):
                        if (k is not "__annotations__"):
                            try:
                                res+=" "*tabbed+print_to_string(k,"=",v)
                            except:
                                res+=" "*tabbed+"(*Error*):%s"%(str(k))
                else:functionct+=1
            else:modulect+=1
        return res
        #print("totalglobals:%d modules:%d functions:%d"%(len(dic),modulect,functionct))
    def printexception(type, value, traceback):
        print("Exception:",type, value)
        
        i=0
        d=""
        while(traceback!=None):
            res=OldGui.printdictvars(traceback.tb_frame.f_locals,i*3)
            d+=" "*i*3+print_to_string(traceback.tb_lineno,traceback.tb_frame)
            d+=res
            i+=1
            traceback=traceback.tb_next
        print("Funcs:%d"%(i),d)
    def threadexcepthook(args):
        tp, value, traceback,thread=tuple([*args])
        print("exception in thread")
        OldGui.printexception(tp, value, traceback)
        print("done")
    def newexcepthook(type, value, traceback):
        OldGui.printexception(type, value, traceback)
        OldGui.oldexcepthook(type, value, traceback)
    def turndebugon():
        print("debugger on!");
        OldGui.debugon=1
        OldGui.oldexcepthook=sys.excepthook
        sys.excepthook=OldGui.newexcepthook
        OldGui.currentglobals=set(globals().keys())
        #print(threading.__excepthook__)
        OldGui.oldthreadexcepthook=threading.excepthook
        threading.excepthook=OldGui.threadexcepthook
doinitstuff()












