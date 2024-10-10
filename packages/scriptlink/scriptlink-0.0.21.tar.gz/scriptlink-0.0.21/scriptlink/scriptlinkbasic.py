#New Project:

import os
import logging
import threading
import time
import sys
import io
import math
#import cv2
from time import perf_counter
import importlib
import sysconfig
import importlib.util
from datetime import datetime
import re
import platform
import subprocess
import traceback 
import json
import time
import random
import functools
def printobj(obj):
    primitives = (bool, str, int, float, type(None))
    isprim=isinstance(obj, primitives)
    diro=dir(obj)
    print('type:',type(obj))#a_list.__len__()==len()
    print('\r\ndir:',diro)
    try:print('len:',len(obj))
    except:pass
    if (isprim==True):
        print('val:',obj)
        return
    if ('shape' in diro):
        print('shape:',obj.shape)
    if ('__repr__' in diro):
        print("__repr__:",str(obj))
    if ('__dict__' in diro):
        print('\r\n__dict__:',obj.__dict__)
    #print('help:',help(obj))
    '''if (Utils.is_primitive(obj)==True):
        print("is primitive:",Utils.is_primitive(obj))
    if (Utils.is_subscriptable(obj)==True):
        print("is subscriptable:",Utils.is_subscriptable(obj))'''
    #Utils.printobject(obj)

class Utils():
    cache={}
    togglethreads={}
    triggers={}
    def printhexstring(s):
        print(s,len(s),type(s))
        '''try:print(s.decode('utf-8'))
        except:print("decode('utf-8')(FAIL)")
        try:print(s.decode('ascii'))
        except:print("decode('ascii')(FAIL)")'''
        print(":".join("{:02x}".format(ord(c)) for c in s))
    def format_time(seconds):
        seconds*=1000
        tmlist=["s","ms","us","ns","ps"]
        tmlist2=[1e-3,1,1e3,1e6,1e9]
        ev=math.log10(seconds+1e-12)//3
        ev=1-int(ev)
        ev=max(min(ev,4),0)
        r="%.03f %s"%(seconds*tmlist2[ev],tmlist[ev])
        return r
    def timeunit(st=0):
        if (st!=0):
            Utils.timeunit.ck=time.time()*1000
            Utils.timeunit.st=st
            Utils.timeunit.ct=0
        else:
            Utils.timeunit.ct+=1
            if (time.time()*1000-Utils.timeunit.ck>Utils.timeunit.st):
                import inspect
                print("%s ct:%d tm:%s"%(inspect.stack()[1].function,Utils.timeunit.ct,Utils.format_time(Utils.timeunit.st/(1000*Utils.timeunit.ct))))
                return 0
        return 1
    def rand(MAX=1000):
        
        if hasattr(Utils, 'randseeded'):
            return random.randint(1,1000)
        
        t = int( time.time() * 1000.0 )
        Utils.randseeded=random.seed( ((t & 0xff000000) >> 24) +
                     ((t & 0x00ff0000) >>  8) +
                     ((t & 0x0000ff00) <<  8) +
                     ((t & 0x000000ff) << 24)   )
        return random.randint(1,1000)
    def removenonalphanum(s):
        import re
        r=re.sub('[\W_]+', '',s)
        return r
    def tryfunc(func,*args):
        try:
            func(*args)
        except:
            print("Unexpected error:"+str( sys.exc_info()[0]))
            traceback.print_exc()
    def atof(s):
        s,_,_=s.partition(' ') # eg. this helps by trimming off at the first space
        while s:
            try:
                return float(s)
            except:
                s=s[:-1]
        return None
    def atoi(s,default=None):
        s,_,_=s.partition(' ') # eg. this helps by trimming off at the first space
        while s:
            try:
                return int(s)
            except:
                s=s[:-1]
        return default
    def mkdir(directory):
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
    def loadjson(filename):
        Utils.loadjsonfile(filename)
    def savejson(filename,jsondata):
        Utils.savejsonfile(filename,jsondata)
    def loadjsonfile(filename):
        js={}
        try:
            with open(filename,'r',encoding="utf-8") as f:
                js = json.load(f);
        except:
            print("loadjsonfile Unexpected error:"+str( sys.exc_info()[0]))
            traceback.print_exc() 
        return js
    def savejsonfile(filename,jsondata):
        try:
            with open(filename,"w") as f:
                json.dump(jsondata, f)
        except:
            print("savejsonfile Unexpected error:"+str( sys.exc_info()[0]))
            traceback.print_exc() 
    def savestringfile(filename,string):
        with open(filename, "w",encoding="utf-8") as f:
            f.write(string)
    def loadstringfile(filename):
        with open(filename, "r",encoding="utf-8") as f:
            string=f.read()
            return string
    def fgetlines(filename,linestart=0,linect=1):
        res=[]
        with open(filename, "rb") as f:
            if (linestart>0):
                f.seek(linestart)
            while(linect>0):
                res.append(f.readline())
                linect-=1
        return res
    def fgetlist(filename):
        with open(filename, "rb") as f:
            string=f.read().decode(errors='replace')
            a=string.find('\n')
            spl='\n'
            if (string[a-1]=='\r'):spl='\r\n'
            return string.split(spl)
    def fput(filename,string):
        with open(filename, "w",encoding="utf-8") as f:
            f.write(string)
    def fgets(filename):
        with open(filename, "rb") as f:
            binary=f.read()
            string=binary.decode(errors='replace')
            return string
    def fgetb(filename):
        with open(filename, "rb") as f:
            binary=f.read()
            return binary
    def fputb(filename,data):
        with open(filename, "wb") as f:
            binary=f.write(data)
    def fputs(filename,string):
        with open(filename, "wb") as f:
            f.write(string.encode())
    def fappend(filename,string):
        with open(filename, "a",encoding="utf-8") as f:
            f.write(string)
    def savecsvfile(filename,data):
        import csv
        writer = csv.writer(open("/path/to/my/csv/file", 'w'))
        for row in data:
            writer.writerow(row)
    def loadcsvfile(filename):
        import csv
        with open(filename, "r",encoding="utf-8") as f:
            csvFile = csv.DictReader(f)
            
            return list(csvFile)
    def savenumpyfile(filename,data,fmt='%s'):
        import numpy as np
        np.savetxt(filename, data, delimiter=',', fmt=fmt)
    def loadnumpyfile(filename,dtype=str):
        import numpy as np
        data=np.loadtxt(filename,delimiter=",", dtype=dtype)
        return data
    def savenumpyfile(filename,data,fmt='%s'):
        import numpy as np
        np.savetxt(filename, data, delimiter=',', fmt=fmt)
    def loadnumpyfile(filename,dtype=str):
        import numpy as np
        data=np.loadtxt(filename,delimiter=",", dtype=dtype)
        return data
    
    def print_to_string(*args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()
        return contents
    def importexists(lib):
        import importlib.util
        _spec = importlib.util.find_spec(lib)
        found = _spec is not None
        if (not found):print("lib %s exists="% (lib),found)
        return found
    def GetAllFilesInDirectory(directory,name="",fullpath=True):
        start_path=directory
        res=[]
        for f in os.listdir(start_path):
            if (len(name)==0 or name in f):
                if (os.path.isfile(start_path+"\\"+f)==True):
                    if (fullpath==True):
                        res.append(start_path+"\\"+f)
                    else:res.append(f)
        return res
    
    def GetFileTextAsList(filename):
        with open(filename) as file:
            lines = [line.rstrip() for line in file]
            return lines
    def name_of_object(arg):
        import inspect
        try:
            return arg.__name__
        except AttributeError:
            pass
        gb=inspect.currentframe().f_back.f_globals
        for name, value in gb.items():
            if value is arg and not name.startswith('_'):
                return name
    def captureprint(func,*args):
        from contextlib import redirect_stdout
        with io.StringIO() as buf, redirect_stdout(buf):
            ret=func(*args)
            output = buf.getvalue()
        return output,ret
    def captureprintsystem(cmd):
        r=subprocess.run(cmd.split(), capture_output=True)
        return r.stdout
    def getlibinfofile(libname,base,fname):
        name=libname.replace("-", "_")
        start_path=sysconfig.get_paths()[base]
        data=""
        for f in os.listdir(start_path):
            if (name in f):
                if (os.path.isfile(start_path+"\\"+f)==False):
                    filename=start_path+"\\"+f+"\\"+fname
                    if (os.path.isfile(filename)==False):
                        continue
                    data=Utils.fgets(filename)
                    return data
        return data
    def toplevel(libname,base):
        #fname=Utils.getlibinfofile(libname,base,filename="top_level.txt"
        name=libname.replace("-", "_")
        start_path=sysconfig.get_paths()[base]
        print(start_path,name)
        for f in os.listdir(start_path):
            if (name in f):
                print("FOUND")
                if (os.path.isfile(start_path+"\\"+f)==False):
                    filename=start_path+"\\"+f+"\\"+"top_level.txt"
                    if (os.path.isfile(filename)==False):
                        filename=start_path+"\\"+f+"\\"+"RECORD"
                        print("no toplevel")
                        if (os.path.isfile(filename)==False):
                            print("no record")
                            return name,start_path+"\\"+f
                        with open(filename, 'r') as read_obj:
                            while(True):
                                toplevel = read_obj.readline().rstrip()
                                if not toplevel:break
                                if (toplevel[0]=='_' or toplevel[0]=='.'):continue
                                if ("/" not in toplevel):continue
                                toplevel=toplevel.split("/")[0]
                                if (name in toplevel):continue
                                folder=start_path+"\\"+toplevel
                                if (os.path.exists(folder)==False):
                                    print("notfolder")
                                    folder=start_path
                                print("data:%s,%s"%(toplevel,folder))
                                return toplevel,folder
                    #print("FOUNDTL")
                    with open(filename, 'r') as read_obj: 
                        toplevel = read_obj.readline().rstrip()
                        if (toplevel[0]=='_'):continue
                        folder=start_path+"\\"+toplevel
                        if (os.path.exists(folder)==False):
                            print("notfolder")
                            folder=start_path
                        print("data:%s,%s"%(toplevel,folder))
                        return toplevel,folder
        return name,None
    def findtoplevelimport(libname):
        name,direc=Utils.toplevel(libname,"purelib")
        return name
    def findtoplevelfolder(libname):
        name,direc=Utils.toplevel(libname,"purelib")
        if (direc==None):
            print("fail1")
            name,direc=Utils.toplevel(libname,'stdlib')
        if (direc==None):
            print("fail2")
            direc=sysconfig.get_paths()['stdlib']
        return direc
    def findbaselibfolder():
        start_path=sysconfig.get_paths()["purelib"]
        return start_path
    def findmetadata(libname):
        data=Utils.getlibinfofile(libname,"purelib",fname="METADATA")
        return data
    def GetBaseModules():
        start_path=sysconfig.get_paths()["stdlib"]
        print(start_path)
        d=[]
        for f in os.listdir(start_path):
            if (os.path.isfile(start_path+"\\"+f)==False):
                filename=start_path+"\\"+f+"\\"+"__init__.py"
                if (os.path.isfile(filename)==False):
                    continue;
                d.append(f)
            if (os.path.isfile(start_path+"\\"+f)==True):
                if (".py" in f):
                    d.append(f.split(".py")[0])
        return d
    def is_primitive(obj):
        primitives = (bool, str, int, float, type(None))
        return isinstance(obj, primitives)
    def is_subscriptable(obj):
        subscriptables = (dict)
        return isinstance(obj,subscriptables)
    def printobject(obj):
        print("\r\nNEW object:%s type:%s"%(obj,type(obj)))
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
    def printobjectrecursive(obj):
        try:
            for attr in dir(obj):
                if (Utils.is_primitive(obj[attr])==False and callable(obj)==False):
                    print("\r\nNEW object:%s type:%s"%(attr,type(obj[attr])))
                    Utils.printobjectrecursive(obj[attr])
                else:print(type(obj[attr]))
                print("%s.%s = %r" % (obj,attr, getattr(obj, attr)))
        except:
            print("error",obj)
    
    def DoThread(name,args=[]):
        x = threading.Thread(target=name, args=args)
        x.daemon = True
        x.start()
    def kill_thread(thread):
        import ctypes
        thread_id = thread.ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
    def DoToggleThread(name,args=[]):
        if (name not in Utils.togglethreads):
            Utils.togglethreads[name] = threading.Thread(target=name, args=args)
            Utils.togglethreads[name].daemon = True
            Utils.togglethreads[name].start() 
        else:
            Utils.kill_thread(Utils.togglethreads[name])
            del Utils.togglethreads[name]
    def GetLocalFolder():
        return os.getcwd()+"\\"
    def printo(obj):
        primitives = (bool, str, int, float, type(None))
        isprim=isinstance(obj, primitives)
        diro=dir(obj)
        print('type:',type(obj))#a_list.__len__()==len()
        print('\r\ndir:',diro)
        try:print('len:',len(obj))
        except:pass
        if (isprim==True):
            print('val:',obj)
            return
        if ('shape' in diro):
            print('shape:',obj.shape)
        if ('__dict__' in diro):
            print('\r\n__dict__:',obj.__dict__)
    def printobj(obj):
        primitives = (bool, str, int, float, type(None))
        isprim=isinstance(obj, primitives)
        diro=dir(obj)
        print('type:',type(obj))#a_list.__len__()==len()
        print('\r\ndir:',diro)
        try:print('len:',len(obj))
        except:pass
        if (isprim==True):
            print('val:',obj)
            return
        if ('shape' in diro):
            print('shape:',obj.shape)
        if ('__dict__' in diro):
            print('\r\n\r\n__dict__: len:%d'%(len(obj.__dict__)))
            for o in obj.__dict__:
                print("field:%s: "%(o))
                try:
                    print(obj.__dict__[o])
                except:
                    print("fail field",o)
        print('\r\n\r\nFULL DIR: len:%d'%(len(diro)))
        for o in diro:
            try:
                attr=getattr(obj,o)
                print("field:%s=%s: "%(o,attr))
            except:
                print("fail field",o)
        
    def format_bytes(size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        return str(round(size,5))+ power_labels[n]
    def getdatetime(time="%m/%d/%y %H:%M:%S"):
        from datetime import datetime
        now = datetime.now()
        dictt={"month":"%m","day":"%d","year":"%y","hour":"%H","minute":"%M","second":"%S","sec":"%S","min":"%M"}
        for i,j in dictt.items():time=time.replace(i,j)
        dt_string = now.strftime(time)
        return dt_string
    def get_processor_name():
        import re
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command ="sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(command).strip()
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
        return ""
    def get_pythonversion():
        return platform.python_version()
    def ln(x):
        return math.log(x)
    def log(x):
        return math.log(x,10)
    def clampscreenx(v):
        return max(0, min(GetScreenX(), v))
    def clampscreeny(v):
        return max(0, min(cd.GetScreenY(), v))
    def speedtest(fn, name):
        start = perf_counter()
        result = fn(DATA)
        duration = perf_counter() - start
        print('{} took {:.4f} seconds\n\n'.format(name, duration))
    def testsingleobj(fn, ct,name,**kwargs):
        start = perf_counter()
        for i in range(ct):
            result = fn(**kwargs)
        duration = perf_counter() - start
        print('%s,%dtotal: %.2f seconds + each:%s'%(name,ct, duration,Utils.format_time(duration/ct)))
    def big_cache(func):#vs @lru_cache(maxsize=None, typed=False)
        cache = {}
        def wrapper(x):
            if x not in cache:
                value = func(x)
                cache[x] = value
            return cache[x]
        return wrapper
    def CLAMP(value, minv, maxv):
        a=max(min(value, maxv), minv)
        return a
    #if (a>c):a=c;
    #elif (a<b):a=b
    #return a;
    def issorted(l):
        return all(l[i] <= l[i+1] for i in range(len(l) - 1))
    def signedcmp(a, b):
        return (a >= b) - (a < b)
    def prshape(a):
        print(type(a),":",a.shape)
    def showallimports():
        print(sys.modules.keys())
    def importer(name, root_package=False, relative_globals=None, level=0):
        """ We only import modules, functions can be looked up on the module.
        Usage: 

        from foo.bar import baz
        >>> baz = importer('foo.bar.baz')

        import foo.bar.baz
        >>> foo = importer('foo.bar.baz', root_package=True)
        >>> foo.bar.baz

        from .. import baz (level = number of dots)
        >>> baz = importer('baz', relative_globals=globals(), level=2)
        """
        #print(name, None,relative_globals,[] if root_package else [None],level)
        return __import__(name, locals=None, # locals has no use
                          globals=relative_globals, 
                          fromlist=[] if root_package else [""],
                          level=level)

class SL_AjaxDownloader:
    def __init__(self):
        import requests
        USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT
        self.session.cookies.set('CONSENT', 'YES+cb', domain='.youtube.com')
    def ajax_request(self, url, headers=None,data=None, retries=5, sleep=.020):
        '''url = 'https://www.youtube.com' + endpoint['commandMetadata']['webCommandMetadata']['apiUrl']

        data = {'context': ytcfg['INNERTUBE_CONTEXT'],
                'continuation': endpoint['continuationCommand']['token']}
        headers={'key': ytcfg['INNERTUBE_API_KEY']}'''
        print("url:",url)

        for _ in range(retries):
            self.response = self.session.post(url, params=headers, json=data)
            if  self.response.status_code == 200:
                return  self.response.text
            if  self.response.status_code in [403, 413]:
                return {}
            else:
                time.sleep(sleep)
    def postsite(self,url):
        self.ajax_request(url)
        return self.response
    def getsite(self,url):
        import requests
        import socket
        from urllib.parse import urlparse
        if ("http" not in url):
            url="http://"+url
        o=urlparse(url)
        domainname = '{uri.netloc}'.format(uri=o)
        #Utils.printhexstring(domainname)
        #Utils.printhexstring(url)
        #Utils.printhexstring(o.netloc)
        #print(socket.gethostbyname(url))
        ip=socket.gethostbyname(o.netloc)
        print("ip:",socket.gethostbyname(ip))
        
        #print(socket.gethostbyaddr(ip))
        #print(socket.getfqdn(ip))
        #print(socket.gethostbyname(domainname))
        
        r = requests.get(url)
        #Utils.printobj(r.raw._original_response)
        #Utils.printobj(r.connection.config)
        return r.content.decode(encoding="ISO-8859-1")
        
        
class Fps:
    def ms(self):
        return round(time.time() * 1000)
    def __init__(self,ct=0):
        self.ct=0
        self.tm=self.ms()
        self.tottm=self.ms()
        self.totct=0
    def update(self):
        self.ct+=1
        self.totct+=1
    def display(self):
        self.update()
        self.tm2=self.ms()-self.tm
        if (self.tm2>1000):
            self.tm=self.ms()
            fps=self.ct*1000/(self.tm2)
            print("fps:",fps)
            self.ct=0
    def gettotal(self):
        self.update()
        fps=(self.totct*1000.0)/(self.ms()-self.tottm)
        return fps
    def update_nodisplay(self):
        self.update()