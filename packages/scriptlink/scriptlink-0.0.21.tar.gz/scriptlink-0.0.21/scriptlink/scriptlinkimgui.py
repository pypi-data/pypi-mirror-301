#Modern Gui
from scriptlink import *

imguidll = ctypes.CDLL(str.lower(os.path.join(os.path.dirname(__file__), 'imguiwrapper.dll')))
class struct_ElementInfo(ctypes.Structure):
    _fields_ = [ ('type',ctypes.c_int32), ('name',ctypes.c_char * 50), ('cval',ctypes.c_char * 500),('ival',ctypes.c_int32),('option50int',ctypes.c_int32*50),('option',ctypes.c_int32)]
class ImguiSimple():
    '''
    guioptions={"callback":callback,"dimensions":[0,0,1200,900],"bgcolor":0x33222222,"alpha":1,"skipframes":0}
    guiinfo=[["Text","text1","somethings",{}],["CheckBox","Start",1,{}],["Text","somethingelse",1,{}]]
    '''
    
    def __init__(self, guioptions={}):
        self.guioptions={"title":"New Gui","dimensions":[0,0,1200,900],"bgcolor":0x33222222,"alpha":1,"skipframes":0}
        self.guioptions.update(guioptions)
        self.SetBackgroundColor(self.guioptions["bgcolor"])
        self.SetAlpha(self.guioptions["alpha"])
        self.SetTitle(self.guioptions["title"])
        self._data=(ctypes.c_char * 1500)()
        self.types={"Text" : 1,"CheckBox" : 2,"SameLine" : 3,"Button" : 4,"InputText" : 5,"Separator" : 6,"Image" : 7,"Canvas" : 8}
        self.windows=[]
        #self.loadgui()
        
    def loadwindow(self,title,guiinfo,flags=[]):
        r=self.destroywindow(title)
        if (r==1):return
        elementct=len(guiinfo)
        elems = (struct_ElementInfo * elementct)()
        array = ctypes.cast(elems,ctypes.POINTER(struct_ElementInfo))
        for i in range(elementct):
            tp=guiinfo[i][0]
            val=str(guiinfo[i][2])
            array[i].type=self.types[tp]
            array[i].name=guiinfo[i][1].encode('utf-8')
            array[i].cval=val.encode('utf-8')
            array[i].ival=Utils.atoi(val,default=0)
            #self.array[i].option1=self.guiinfo[i][3]
        #print(elems,array)
        self.windows.append({"data":array,"ct":elementct,"title":title,"flags":flags})
        print(self.windows)
    def destroywindow(self,title):
        for i,w in enumerate(self.windows):
            if (w["title"]==title):
                del(self.windows[i])
                return 1
        return 0
    def SetBackgroundColor(self,c):
        return imguidll.setclearcolorint(c)
    def SetAlpha(self,on):
        return imguidll.setalpha(on)
    def SetTitle(self,name):
        return imguidll.settitle(name.encode('utf8'))
        
    def setdatastring(self,wnum,i,val):
        #print(wnum,i,val,self.windows[wnum]["data"][i].cval)
        self.windows[wnum]["data"][i].cval=val.encode('utf-8')
    def setdataint(self,wnum,i,val):
        self.windows[wnum]["data"][i].ival=val
    def getdata(self,wnum,i):
        w=self.windows[wnum]
        return w["data"]
    def getcanvasdata(self,wnum,i):
        w=self.windows[wnum]
        ct=w["data"][i].option
        if (ct<2):return 0,0,0,0
        x=w["data"][i].option50int[ct-2]//2
        y=w["data"][i].option50int[ct-1]//2
        return ct//2,x,y,0
    def startgui(self,eventfunc,loopfunc):
        skipframes=self.guioptions["skipframes"]
        self.eventfunc=eventfunc
        self.running=1
        self.running=imguidll.startgui(self.guioptions["title"].encode('utf8'),*self.guioptions["dimensions"])
        if (self.running==0):
            print("dll failed to start")
        ct=skipframes
        ctr=0
        while(self.running):
            Sleep(10)
            ctr+=1
            loopfunc()
            ret=imguidll.msgloop()
            if (ret==0):
                print("dll error:ended msgloop")
                break
            if (ct<skipframes):
                ct+=1
                Sleep(50)
                continue
            ct=0
            ret=imguidll.beginloop()
            if (ret==0):print("guifunc ended beginloop")
            ####do windows####
            for wnum,w in enumerate(self.windows):
                data=w["data"]
                i=imguidll.doimguiwin(w["ct"],w["title"].encode('utf8'),data)
                if (i!=-1):
                    val=data[i].cval.decode('utf-8')
                    if (data[i].type==self.types["CheckBox"]):
                        val=data[i].ival
                    self.eventfunc(wnum,i,data[i].name.decode('utf-8'),val)
            #print("imguidll.doguiloop()")
            end=imguidll.endloop()
            
    