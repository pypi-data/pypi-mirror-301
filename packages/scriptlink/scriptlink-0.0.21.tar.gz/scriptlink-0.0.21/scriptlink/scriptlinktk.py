from scriptlink import *

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import tkinter.filedialog
import tkinter.filedialog
import os
from os import listdir
from os.path import isfile, join
import io
from contextlib import redirect_stdout
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
lib_dirname = os.path.dirname(__file__)
def SetMainIcon(root,iconname):
    if (".ico" in iconname):
        root.iconbitmap(iconname)
    else:
        extensionsToCheck = ['.png', '.gif']
        if any(ext in iconname for ext in extensionsToCheck):
            photo = tk.PhotoImage(file = iconname)
            root.wm_iconphoto(False, photo)
        else:
            from PIL import Image, ImageTk
            ico = Image.open(iconname)
            photo = ImageTk.PhotoImage(ico)
            root.wm_iconphoto(False, photo)

def DoEventsTk(root):
        root.update_idletasks()
        root.update()
def SaveSettings(filename,settings):
    json={"settings":settings}
    Utils.savejsonfile(filename,json)
def LoadSettings(filename,settings,checkboxes=[],inputtexts=[],options=[]):
    found=1
    if os.path.isfile(filename):
        try:
            json=Utils.loadjsonfile(filename)
        except:
            found=0
    else:found=0
    if (found==1):settings.update(json["settings"])
    else:print("settings file not found")
    for t in checkboxes:
        for k,v in settings.items():
            if (t[0]==k):t[1]=v
        else:settings[t[0]]=t[1]
    for t in inputtexts:
        for k,v in settings.items():
            if (t[0]==k):t[1]=v
        else:settings[t[0]]=t[1]
    for i,t in enumerate(options):
        for k,v in settings.items():
            if (t["title"]==k):t["default"]=v
    if (found==0):SaveSettings(filename,settings)
        #else:settings[k]=t[1]
def printtkversion(root):
    print("tkinter version:",tk.TkVersion)
    print(root.tk.exprstring('$tcl_library'))
    print(root.tk.exprstring('$tk_library'))
#filename=OpenFileDialog(types=("Python files", ".py .txt"))
def OpenFileDialog(filetypes=[("Python files", ".py .txt")],directory=None):
    if ("initialdir" not in OpenFileDialog.__dict__):
        OpenFileDialog.__dict__["initialdir"]=os.getcwd()
    initialdir=OpenFileDialog.__dict__["initialdir"]
    if (directory!=None):initialdir=directory
    filename = tk.filedialog.askopenfilename(initialdir=initialdir,filetypes=filetypes)
    OpenFileDialog.__dict__["initialdir"]=os.path.dirname(filename)
    return filename.replace("/","\\")
    
def OpenFileFolderDialog():
    dirname = tk.filedialog.askdirectory(initialdir=os.getcwd())
    return dirname.replace("/","\\")
class MultiFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
class ButtonTable(tk.Frame):

    def __init__(self, parent, buttons_data,buttonsmap,buttons_color_map,funcclick,funchotkey=None):
        self.top=parent
        tk.Frame.__init__(self, parent)
        '''Initializes a new instance of the ButtonTable class'''
        self.funcclick=funcclick
        self.funchotkey=funchotkey
        # get data for building the buttons table
        self.get_buttons_data(buttons_data)#'''{"buttons": [{"Alias": "1"},{"Alias": "2"}}]}'''
        self.get_buttons_map(buttonsmap)#'''{"map": {"H": { "row": 1, "column" : 0 }}}'''
        self.get_buttons_color_map(buttons_color_map)#'''{"map": {"Alkali Metals": "grey"}}'''

        # add controls on UI
        self.buttons = {}
        self.parent = parent
        self.build_buttons_table(funcclick,funchotkey)
        #self.reset_button = tk.Button(self, text=self.reset_button_text, width=5, height=2, bg= "black", fg = "white",command=lambda text="": (self.change_header(self.default_header), self.funcclick("")))
        #self.reset_button.grid(row=12, column=0)

    def get_buttons_data(self,buttons_data):
        '''Loads buttons data from json'''
        if (type(buttons_data)==type(" ")):
            self.buttons_data = json.loads(buttons_data)
        else:self.buttons_data=buttons_data

    def get_buttons_map(self,buttonsmap):
        if (type(buttonsmap)==type(" ")):
            self.buttons_map=json.loads(buttonsmap)
        else:self.buttons_map=buttonsmap

    def get_buttons_color_map(self,buttons_color_map):
        if (type(buttons_color_map)==type(" ")):
            self.buttons_color_map=json.loads(buttons_color_map)
        else:self.buttons_color_map = buttons_color_map

    def build_buttons_table(self,funcclick,funchotkey):
        '''Adds button controls for each button on UI'''
        
        for button in self.buttons_data["buttons"]:

            if ("number" in button):
                bnumber = button["number"]
            else:bnumber = button["Alias"]
            if (funchotkey!=None):
                hotkey = button["hotkey"]
                print(button)
                Keyboard.SetTrigger(lambda e=button:funchotkey(e),*hotkey,once="onceup")
            row = self.buttons_map["map"][bnumber]["row"]
            col = self.buttons_map["map"][bnumber]["column"]
            #print(button["Categories"][0])
            color = self.buttons_color_map['map'][button["Categories"][0]]

            b = tk.Button(self, text=button["Alias"], width=5, height=2, bg=color,
                               command=lambda  e=button: funcclick(e))
            
            b.grid(row=row, column=col)            
            self.buttons[bnumber] = button

        self.fillerLine = tk.Label(self, text="")
        self.fillerLine.grid(row=10, column=0)

    def change_header(self, text): 
        '''Changes Label text at the top with the name of whichever 
        button tk.Button was pressed'''

        self.topLabel.config(text=text)

    def change_info(self, text):
        '''Displays information on the button of 
        whichever button tk.Button was pressed'''

        self.infoLine.config(text=text)
class ImageWindow(tk.Frame):
    def __init__(self,parent,image,callback=None):
        self.top=parent
        #self.root=root
        
        #print(image.shape,np.uint8,np.uint16,np.uint32)
        #height, width,bits = image.shape
        #print(height, width,bits)
        #root.geometry(f"{width+5}x{height+5}")
        tk.Frame.__init__(self, parent)
        #self.frame = tk.Frame(root)
        #self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
    def update(self,image):
        from PIL import Image, ImageTk
        import numpy as np
        #print(image.shape,self.canvas.winfo_width(), self.canvas.winfo_height()//3)
        if (any(elem<=0 for elem in image.shape)):return
        #print(image.shape)
        #print(image.shape)
        '''self.times+=1
        if self.times%100==0:
            self.master.title(f"numpy->tkinter @ {self.times/(time.time()-self.time_ref):.1f} FPS")
            self.times, self.time_ref = 0, time.time()'''
        image_id=1
        PPMimage = f'P6 {image.shape[1]} {image.shape[0]} 255 '.encode() + np.array(image, dtype=np.int8).tobytes()
        TKPimage = tk.PhotoImage(width=image.shape[1], height=image.shape[0], data=PPMimage, format='PPM')
        #print(f'P6 {image.shape[1]} {image.shape[0]} 255 ',TKPimage)
        if hasattr(self.canvas, 'dummy_image_reference'):
            self.canvas.itemconfig(image_id, image=TKPimage)
            #print("added",TKPimage)
        else:
            #print("created",self.canvas.winfo_width(), self.canvas.winfo_height()//3)
            self.canvas.create_image(1, 0, image=TKPimage, anchor=tk.NW)
        self.canvas.dummy_image_reference = TKPimage # prevents garbage collecting of the PhotoImage object
class Simpledlg:
    def __init__(self,title="New Item",description="Enter name of item:"):
        self.item = simpledialog.askstring(title, description)
    def get(self):
        return self.item
class LessSimpledlg:
    def __init__(self,root,msg="Enter Something",buttons=[],newfilebutton=None,listcallback=None,optionmenu=[],):
        self.top = tk.Toplevel(root)
        master=self.top
        self.frm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)
        label = tk.Label(self.frm, text=msg)
        label.pack(padx=4, pady=4)
        self.pw = tk.PanedWindow(self.top,orient=tk.HORIZONTAL)
        self.buttons=[]
        for i,value in enumerate(buttons):
            #print(value[1],value[0])
            self.buttons.append(tk.Button(master, height = 2,width = 20,text =value[0],command = value[1]))
            self.buttons[i].pack()
            self.pw.add(self.buttons[i])
        self.optionvariables=[]
        if (len(optionmenu)>0):
            for i,option in enumerate(optionmenu):
                self.optionvariables.append(tk.StringVar(master))
                self.optionvariables[i].set(option[0]) # default value
                w = tk.OptionMenu(master, self.optionvariables[i], *option)
                w.pack()
                self.pw.add(w,stretch="always")
        self.pw.pack(fill=tk.BOTH, expand=True)
        if (newfilebutton!=None):
            open_button = tk.Button(frm, text="Open File", command=self.opennewfile)
            open_button.pack(padx=20, pady=20)
    def getoptiontext(self,index):
        mytext= self.optionvariables[index].get()
        return mytext
    def setdefaultoption(self,optionindex,index):
        mytext= self.optionvariables[index].get()
        return mytext
    def close(self):
        self.top.destroy()
        
class _togbutton:
    def __init__(self,root,callback=None,label1="On",label2="Off",img1="on.png",img2="off.png",ison=False):
        self.root=root
        self.label1=label1
        self.label2=label2
        pane = tk.Frame(root,width=100, height=50)
        pane.pack(pady = 2)
        self.my_label = tk.Label(pane,text = label2,fg = "green",font = ("Helvetica", 12))
        self.my_label.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH)
        #self.my_label.pack(pady = 2,ipadx=10,ipady=10,expand=True,fill='both',side='left')
        self.on = tk.PhotoImage(file = lib_dirname+"\\"+img1)
        self.off = tk.PhotoImage(file = lib_dirname+"\\"+img2)
        self.on_button = tk.Button(pane, image = self.on, bd = 0,command = self.switch)
        self.on_button.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        self.is_on=not ison
        self.on_button.config(image = self.off)
        self.callback=callback
        self.switch(docallback=False)
    def switch(self,docallback=True):
        if self.is_on:
            self.on_button.config(image = self.off)
            self.my_label.config(text = self.label2,fg = "grey")
            self.is_on = False
        else:
            self.on_button.config(image = self.on)
            self.my_label.config(text = self.label1, fg = "green")
            self.is_on = True
        if (self.callback!=None and docallback==True):
            self.callback(self.is_on)
    def get(self):return self.is_on
    def set(self,val):
        if (val==True and self.is_on==False):self.switch()
        elif (val==False and self.is_on==True):self.switch()
    def getstatus(self):
        return self.is_on
class _tkslider:
    def __init__(self,root,label1="title",fg = "green",callback=None,resolution=25,froms=0,tos=100,slider_text={},index=0):
        self.root=root
        self.index=index
        self.callback=callback
        self.pane = tk.Frame(root)
        self.pane.pack(pady = 2)
        self.slider_text=slider_text
        self.slider = tk.Scale(self.pane,from_=froms,to=tos,resolution=int(resolution),orient='horizontal',command=self.precallback)
        self.slider.pack(side = tk.LEFT)
        self.slider_label = tk.Label(self.pane,text = label1,fg = fg,font = ("Helvetica", 12))
        self.slider_label.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH,anchor="e")
        
        
    def settitle(self,title):
        self.slider_label.config(text = title)
    def precallback(self,event):
        if (len(self.slider_text)>0):
            self.settitle(str(self.slider_text[int(event)]))
        else: self.settitle(event)
        self.callback(self.index,event)
class _tkinputtext:
    def __init__(self,root,labeltext="title",defaulttext="",fg = "green",callback=None,index=0,width=80):
        self.root=root
        self.callback=callback
        self.index=index
        self.pane = tk.Frame(root)
        #self.pane.grid_columnconfigure((0,1), weight=1)
        self.pane.pack(anchor="w")
        self.labeltext=labeltext
        self.label = tk.Label(self.pane,text = labeltext)
        self.label.grid(row=1, column=0,sticky='w')
        #self.label.pack()
        
        self.sv = tk.StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.precallback(sv))
        #e = Entry(root, textvariable=sv)
        self.inputtext = tk.Entry(self.pane,width = width,textvariable=self.sv)
        #self.inputtext.config(wrap='none')
        self.inputtext.bind("<Return>", self.on_return)
        self.inputtext.bind("<Control-a>", self.select_all)
        
        #self.inputtext.bind('<<Modified>>', self.precallback)
        self.inputtext.grid(row=1, column=1, sticky="ew")
        self.settext(defaulttext)
        #self.inputtext.pack()
    def on_return(self, event):
        self.precallback(event)
    def select_all(self, *ignore):
        self.selection_range(0, 'end')
    def gettext(self):
        return self.inputtext.get()
    def getlabel(self):
        return self.label.cget("text")
    def settext(self,text):
        self.defaulttext=text
        self.inputtext.delete(0)
        self.inputtext.insert(tk.END, self.defaulttext)
    def setlabel(self,title):
        self.label.config(text = title)
    def precallback(self,event):
        #self.inputtext.edit_modified(False)
        if (self.callback!=None):
            self.callback(self.index,self.getlabel(),self.gettext())

class ThreeTogs:
    def __init__(self, root,tg1callback,tg2callback,tg3callback,btcallback,sldcallback,optionmenu=[]):#master=root
        self.root=root
        self.l = tk.Label(text = "Hole Cards. Example: As Ks Qc Jh 4d")
        self.holeinputtxt = tk.Text(root, height = 2,width = 25,bg = "white")
        self.holeinputtxt.insert(tk.END, "As Ks Ah 3h")
        self.l2 = tk.Label(text = "Board Cards. Example: Kc 2h 2d")
        self.boardinputtxt = tk.Text(root, height = 2,width = 25,bg = "white")
        self.tg1=_togbutton(root,tg1callback,"ReaderOn","ReaderOff",ison=False)
        self.tg2=_togbutton(root,tg2callback,"Hilo Omaha ON","HiLo Off",ison=False)
        self.tg3=_togbutton(root,tg3callback,"Pot Omaha ON","Omaha Off",ison=True)
        #current_range = DoubleVar()
        self.pane = tk.Frame(root)
        self.pane.pack(pady = 2)
        self.slider = tk.Scale(self.pane,from_=0,to=100,resolution=25,orient='horizontal',command=sldcallback)
        self.slider.pack(side = tk.LEFT)
        self.slider_label = tk.Label(self.pane,text = "OppRange",fg = "green",font = ("Helvetica", 12))
        self.slider_label.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH,anchor="e")
        self.l.pack()
        self.holeinputtxt.pack()
        self.l2.pack()
        self.boardinputtxt.pack()
        
        self.DisplayC = tk.Button(root, height = 2,width = 20,text ="Calculate winning odds",command =btcallback)
        self.DisplayC.pack()
        
        self.Output = tk.Text(root, height = 5,width = 25,bg = "light cyan")
        self.Output.pack()
        
        self.optionvariables=[]
        self.optionmenu=optionmenu
        self.pw=tk.PanedWindow(root,orient=tk.HORIZONTAL)
        self.pw.pack( expand=False)
        if (len(optionmenu)>0):
            for i,option in enumerate(optionmenu):
                self.optionvariables.append(tk.StringVar(root))
                self.optionvariables[i].set(option[0]) 
                w = tk.OptionMenu(root, self.optionvariables[i], *option)
                w.pack()
                self.pw.add(w,stretch="always")
    def setoutputtext(self,text):
        self.Output.delete("1.0",tk.END)
        self.Output.insert("1.0", text)
    def settitle(self,title):
        self.master.title(title)
    def getoptiontext(self,index):
        mytext= self.optionvariables[index].get()
        return mytext
    def getoptiontextindex(self,index):
        mytext= self.optionvariables[index].get()
        i=self.optionmenu[index].index(mytext)
        return i



#List is actually Tree, in this case Swapable with Text Window
class ListClicker:
    def DoEvents(self):
        tk.update_idletasks()
        tk.update()
    def setalpha(self,alpha):
        self.master.attributes("-alpha", alpha)
    def newframe(self,fill=tk.X,expand=False):
            self.frames+=1
            self.pw.append(tk.PanedWindow(self.master,orient=tk.HORIZONTAL))
            self.pw[self.frames].pack(fill=fill, expand=expand)
    def __init__(self, master,toptexts=[],buttons=[],listcallback=None,optionmenu=[],rightclickmenu=[],columns=("c1", "c2", "c3"),columnwidths=None,columncallback=None,editable=False,buttontext="Back",geom="1000x780",ht = 20,wd = 95,title="tk"):#master=root
        self.master = master
        self.master.title(title)
        root=master
        if (geom!=None):
            self.master.geometry(geom)
        self.root=root
        self.label = tk.Label(text="")
        self.contents=0
        self.pw=[]
        self.frames=-1
        self.newframe()
        self.columncallback=columncallback
        self.editable=editable
        #buttons#########
        self.buttons=[]
        self.buttondata=buttons
        for i,value in enumerate(buttons):
            self.buttons.append(tk.Button(master, height = 2,width = 20,text =value[0],command = lambda x=i:self._prebutton_click(x)))
            self.buttons[i].pack()
            self.pw[self.frames].add(self.buttons[i],stretch="always")
        #options#########
        self.optionvariables=[]
        self.optionmenu=optionmenu
        if (len(optionmenu)>0):
            for i,option in enumerate(optionmenu):
                self.optionvariables.append(tk.StringVar(master))
                self.optionvariables[i].set(option[0]) 
                w = tk.OptionMenu(master, self.optionvariables[i], *option)
                w.pack()
                self.pw[self.frames].add(w,stretch="always")
        #texts#########
        self.texts=[]
        self.inputtexts=[]
        self.textcallbacks=[]
        self.args=[]
        
        self.newframe()
        for i,value in enumerate(toptexts):
            wd=80
            ht=2
            self.args.append(i)
            if (len(value)>2):
                wd=value[2]
            if (len(value)>3):
                ht=value[3]
            self.texts.append(tk.Text(master, height=ht ,width=wd ,bg = "white"))
            self.texts[i].insert("1.0", value[0])
            self.texts[i].pack()
            
            self.pw[self.frames].add(self.texts[i],stretch="always")
            self.textcallbacks.append(value[1])
            f=lambda e: self._PreOnModifyText(e)
            self.texts[i].bind('<<Modified>>', f)
            self.inputtexts.append("")
        #tree############  
        self.newframe(fill=tk.BOTH,expand=True)  
        self.tree = ttk.Treeview(master, column=columns, show= 'headings', height=ht)
        self.pw[self.frames].add(self.tree,stretch="always")
        for i, thing in enumerate(columns):
            c=i+1
            self.tree.heading("# "+str(c), text=columns[i],command=lambda g=i:self.precolumn_click(g))
            if (columnwidths!=None):
                if (type(columnwidths[i])==tuple):self.tree.column("# "+str(c), minwidth=0, width=columnwidths[i][0], stretch=columnwidths[i][1])
                else:self.tree.column("# "+str(c), minwidth=0, width=columnwidths[i], stretch=tk.NO)
        self.label.pack(side="bottom", fill="x")
        self.tree.bind("<Double-1>", self._PreOnDoubleClick)
        #scrollbar############  
        self.vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.pw[self.frames].add(self.vsb,stretch="always")
        self.treeframe=self.frames
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        #right click menu############  
        def do_popup(event):
            print("popup")
            #self.popup.tk_popup(event.x_root, event.y_root, 0)
            self.popup.selection = self.tree.set(self.tree.identify_row(event.y))
            rowid = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            self.popuplocation=(rowid,int(column[1:])-1)
            self.popup.post(event.x_root, event.y_root)
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()
        if (len(rightclickmenu)>0):
            self.popup = tk.Menu(self.root, tearoff=0)
            for i, thing in enumerate(rightclickmenu):
                self.popup.add_command(label=thing[0], command=thing[1])
                self.popup.add_separator()
            self.tree.bind("<Button-3>", do_popup)
        #waitcallback############  
        self.master.bind('<<WaitEvent>>', self._WaitEvent)
        self.waitcallback=None
        self.listcallback=listcallback
        self.swapped=0
    
    
    ####Swappable Tree funcs
    def setswaptext(self,text):
        if (self.swapped==1):
            self.swaptext.delete("1.0",tk.END)
            self.swaptext.insert("1.0", text)
    def getswaptext(self):
        if (self.swapped==1):return self.swaptext.get("1.0",'end-1c')
        return ""
    def setswaptextcursor(self,line,column):
        if (self.swapped==1):
            self.swaptext.mark_set("insert", "%d.%d" % (line + 1, column + 1))
            self.swaptext.see("%d.%d" % (line + 1, column + 1))
            #self.v
    def getswaptextcursor(self):
        if (self.swapped==1):
            return self.swaptext.index(tk.INSERT)
        return 0
    def isswappedtotext(self):
        return (self.swapped==1)
    def swaptree(self):
        if (self.swapped==1):
            print("tryhide")
            try: 
                self.swaptext.destroy()
                self.v.destroy()
                self.vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
                self.pw[self.treeframe].add(self.vsb,stretch="always")
                self.tree.configure(yscrollcommand=self.vsb.set)
            except AttributeError:
                pass
        else:
            self.vsb.destroy()
            
            self.master.update()
            (x,y,width,height)=(self.tree.winfo_x(),self.tree.winfo_y(),self.tree.winfo_width(),self.tree.winfo_height())
            print("tryhide",(x,y,width,height))
            self.swaptext = tk.Text(self.tree, height = 400,width = 25,bg = "white")
            self.swaptext.place(x=0, y=0, width=width, height=height, anchor='nw')
            self.v=tk.Scrollbar(self.master, orient='vertical',command=self.swaptext.yview)
            self.swaptext.configure(yscrollcommand=self.v.set)
            self.pw[self.treeframe].add(self.v,stretch="always")
        self.swapped=(self.swapped+1)%2
    ######Tree Funcs
    def showtree(self):
        print("tryshow")
        try: 
            self.swaptext.destroy()
        except AttributeError:
            pass
    def getpoplocation(self):
        return self.popuplocation
    def getselectedcopy(self):
        rows=self.tree.selection()
        rowvals = [self.tree.item(rowid, 'values') for rowid in rows]
        return (self.popuplocation,rows,rowvals)
    def getselected(self):
        rows=self.tree.selection()
        rowvals = [self.tree.item(rowid, 'values') for rowid in rows]
        return rowvals
    def setitemtext(self,rowid,column,text):
        vals = self.tree.item(rowid, 'values')
        vals = list(vals)
        vals[column] = text
        self.tree.item(rowid, values=vals)
    def getitemtext(self,rowid,column):
        vals = self.tree.item(rowid, 'values')
        vals = list(vals)
        return vals[column]
    def getnextrow(self,rowid):
        return self.tree.next(rowid)
    def getprevrow(self,rowid):
        return self.tree.prev(rowid)
    def setcolumntext(self,i,ctext):
        hi=int(i)+1
        h="# "+str(hi)
        self.tree.heading(h, text=ctext,command=lambda c=i:self.precolumn_click(c))
    def getcolumntext(self,i):
        hi=int(i)+1
        h="#"+str(hi)
        t=self.tree.heading(h)['text']
        return t
    def precolumn_click(self,index):
        print("clicked %s"%(str(index)))
        if self.columncallback!=None:
            self.columncallback(index)
    def gettreedata(self):
        v=[]
        for line in self.tree.get_children():
            v1=[]
            for value in self.tree.item(line)['values']:
                v1.append(value)
            v.append(v1)
        return v
    def addalternatingcolor(self,color):
        self.tree.tag_configure('even', background=color)
    def populatelist(self,items):
        self.tree.delete(*self.tree.get_children())
        for i, thing in enumerate(items):
            if (i%2==0):
                self.tree.insert('', 'end', tags=('odd',), values=thing)
            else :
                self.tree.insert('', 'end', tags=('even',), values=thing)
    def clearlist(self):
        self.tree.delete(*self.tree.get_children())
    
    ######Editable Tree Class and Funcs
    class EntryPopup(ttk.Entry):
        def __init__(self, parent, iid, column, text, **kw):
            ttk.Style().configure('pad.TEntry', padding='1 1 1 1')
            super().__init__(parent, style='pad.TEntry', **kw)
            self.tv = parent
            self.iid = iid
            self.column = column

            self.insert(0, text) 
            self['exportselection'] = False
            self.focus_force()
            self.select_all()
            self.bind("<Return>", self.on_return)
            self.bind("<Control-a>", self.select_all)
            self.bind("<Escape>", lambda *ignore: self.destroy())
        def on_return(self, event):
            rowid = self.tv.focus()
            vals = self.tv.item(rowid, 'values')
            vals = list(vals)
            vals[self.column] = self.get()
            self.tv.item(rowid, values=vals)
            self.destroy()


        def select_all(self, *ignore):
            self.selection_range(0, 'end')
            # returns 'break' to interrupt default key-bindings
            return 'break'
    def onDoubleClick(self, event):
        if (self.editable):
            try:  # in case there was no previous popup
                self.tree.entryPopup.destroy()
            except AttributeError:
                pass
            rowid = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            if not rowid:return
            x,y,width,height = self.tree.bbox(rowid, column)
            pady = height // 2
            text = self.tree.item(rowid, 'values')[int(column[1:])-1]
            self.tree.entryPopup = self.EntryPopup(self.tree, rowid, int(column[1:])-1, text)
            self.tree.entryPopup.place(x=x, y=y+pady, width=width, height=height, anchor='w')
    
    
    def _PreOnDoubleClick(self, event):
        #print("dc",event)
        if (self.editable==True):
            self.onDoubleClick(event)
        item = self.tree.selection()
        
        if (len(item)>0 and self.listcallback!=None):
            self.listcallback(self.tree.item(item)['values'])
    
    
    
    
    ######Basic Funcs##########
    def settitle(self,title):
        self.master.title(title)
    def _WaitEvent(self,event):
        if (self.waitcallback!=None):
            self.waitcallback()
    def waitforevent(self,waitcallback):
        self.waitcallback=waitcallback
        self.master.event_generate("<<WaitEvent>>", when="tail")
    def _PreOnModifyText(self, event):
        caller = event.widget
        for i,t in enumerate(self.texts):
            if (caller==t):break
        t = self.texts[i].get("1.0",'end-1c')
        #print("PreOnModifyText",i,t)
        if (self.inputtexts[i]!=t):
            self.inputtexts[i]=t
            if (self.textcallbacks[i]!=None):
                self.textcallbacks[i]()
        self.texts[i].edit_modified(False)
    def _prebutton_click(self,index):
        if len(self.buttondata[index])<3:
            self.buttondata[index][1]()
            return
        t=self.getbuttontext(index)
        if (t==self.buttondata[index][0]):
            self.setbuttontext(index,self.buttondata[index][2])
        else:self.setbuttontext(index,self.buttondata[index][0])
        self.buttondata[index][1]()
    
    def getoptiontext(self,index):
        mytext= self.optionvariables[index].get()
        return mytext
    def getoptiontextindex(self,index):
        mytext= self.optionvariables[index].get()
        i=self.optionmenu[index].index(mytext)
        return i
    
    def settoptext(self,i,text):
        self.texts[i].delete("1.0",tk.END)
        self.texts[i].insert("1.0", text)
    def gettoptext(self,i):
        t = self.texts[i].get("1.0",'end-1c')
        return t
    def setbottomtext(self,my_text):
        self.label.config(text = my_text)
    def setbuttontext(self,index,my_text):
        self.buttons[index].config(text = my_text)
        print("setbut",my_text)
    def getbuttontext(self,index):
        mytext= self.buttons[index].cget('text')
        return mytext
    


class TripleButton1:
    def DoEvents(self):
        Utils.DoEventsTk(self.master)
    def newframe(self,fill=tk.X,expand=False,frame=None):
        if (frame==None):
            frame=tk.PanedWindow(self.master,orient=tk.HORIZONTAL)
        self.frames+=1
        self.pw.append(frame)
        self.pw[self.frames].pack(fill=fill, expand=expand)
    def __init__(self, master,buttons=[],optionmenu=[],toggles=[],sliders=[],inputtexts=[],checkboxes=[],images=[],callback=None,frameadd=None,ht = 2,wd = 45,geom="700x700",buttonwidth=40,bg = "white",fg = "black",title="tk",labeltext="",wraplength=120):
        #master=root
        self.bg=bg
        self.master = master
        self.callback=callback
        if (callback==None):
            self.callback=self.defaultcallback
        self.master.title(title)
        self.folder=""
        #self.dropdownVar = tk.StringVar(master)
        #self.dropdownVar.trace_add('write', self.option_changed)
        self.modellabel = tk.Label(text = labeltext)
        self.modellabel.pack()
        
        self.v=tk.Scrollbar(master, orient='vertical')
        self.v.pack(side=tk.RIGHT, fill='y')
        self.holeinputtxt = tk.Text(master, height=ht ,width=wd ,bg = bg,fg=fg,yscrollcommand=self.v.set)
        self.holeinputtxt.insert("1.0", self.folder)
        self.v.config(command=self.holeinputtxt.yview)
        self.holeinputtxt.pack(fill='both',expand=1)
        self.frames=-1;
        self.pw=[]
        self.buttons=[]
        if (frameadd!=None):
            if (type(frameadd)==type([])):
                for f in frameadd:
                    self.newframe(frame=f,expand=False,fill=tk.X)
            else:self.newframe(frame=frameadd,expand=False,fill=tk.X)
        self.frameadd=frameadd
        maxi=int(200/buttonwidth)
        if (len(optionmenu)>0 and type(optionmenu[0])==type(list())):
            self.optionmenulist=optionmenu
        else:
            self.optionmenulist=[i["choices"] for i in optionmenu]
        self.optionmenu=optionmenu
        self.master.geometry(geom)
        print("TripleButton buttons:%d options:%d geom:(%s)"%(len(buttons),len(optionmenu),geom))
        self.geowidth, self.geoheight = map(int, geom.split("x"))
        #print(self.geowidth)
        self.toggles=toggles
        self.togs=[]
        self.sliders=sliders
        self.sli=[]
        self.checkboxes=checkboxes
        self.ch=[]
        self.chvars=[]
        self.inputtexts=inputtexts
        self.inputtextnames=[_[0] for _ in inputtexts]
        self.inp=[]
        self.images=images
        #if (len(sliders)>0):self.newframe(expand=False)
        for i,image in enumerate(images):
            from PIL import ImageTk, Image
            img = ImageTk.PhotoImage(Image.open(image[1]))  # PIL solution
            image = tk.PhotoImage(file=image[1])
            dx,dy = image.width(), image.height()
            self.newframe()
            frm=tk.Frame(self.pw[self.frames])
            frm.pack()
            label = tk.Label(frm, compound="top", image=image, text=image[0])
            label.pack()
            
        for i,value in enumerate(checkboxes):
            togsize=int(self.geowidth/120)
            if (i%togsize==0):self.newframe()
            frm=tk.Frame(self.pw[self.frames], width=100, height=50)
            if (len(checkboxes)==1):frm.pack()
            else:frm.pack(side=tk.LEFT)
            
            self.chvars.append(tk.StringVar(value=checkboxes[i][1]))
            checkbox=tk.Checkbutton(frm, text=checkboxes[i][0],variable=self.chvars[i], onvalue=1, offvalue=0, command=(lambda x=i:self._pre_checkbox(x)))
            checkbox.pack()
            self.ch.append(checkbox)
            
        for i,value in enumerate(sliders):
            togsize=int(self.geowidth/200)
            if (i%togsize==0):self.newframe()
            frm=tk.Frame(self.pw[self.frames], width=100, height=50)
            if (len(sliders)==1):frm.pack()
            else:frm.pack(side=tk.LEFT)
            self.sli.append(_tkslider(frm,label1=value[0],fg = value[1],callback=self._preslider,resolution=value[3],froms=value[4],tos=value[5],slider_text=value[6],index=i))
        for i,value in enumerate(toggles):
            togsize=int(self.geowidth/200)
            if (i%togsize==0):self.newframe()
            frm=tk.Frame(self.pw[self.frames], width=100, height=50)
            if (len(toggles)==1):frm.pack()
            else:frm.pack(side=tk.LEFT)
            self.togs.append(_togbutton(frm,value[2],value[0],value[1],ison=False))
        self.newframe()
        for i,value in enumerate(inputtexts):
            #togsize=int(self.geowidth/320)
            #if (i%togsize==0):self.newframe()
            #self.newframe()
            frm=tk.Frame(self.pw[self.frames], height=50)
            frm.pack(side=tk.LEFT)
            ip=value[1] if (len(value)>1) else ""
            self.inp.append(_tkinputtext(frm,labeltext=value[0],defaulttext=ip,callback=self._preinputtext,index=i))
        self.newframe()
        self.buttondata=buttons
        i=0
        for i,value in enumerate(buttons):
            if ((i+1)%maxi==0):
                self.newframe()
            #print(value[1],value[0])
            self.buttons.append(tk.Button(master, height = 2,width = 20,text =value[0],wraplength=wraplength,command = (lambda x=i:self._prebutton_click(x))))
            #self.buttons.append(tk.Button(master, height = 2,width = buttonwidth,text =value[0],command = value[1]))
            self.buttons[i].pack()
            self.pw[self.frames].add(self.buttons[i],stretch="always")
        if ((i+1)%maxi>maxi/2):
            self.newframe()
        self.optionvariables=[]
        self.optionwidgets=[]
        self.optioncallback=None
        if (len(optionmenu)>0):
            for i,option in enumerate(optionmenu):
                if ((i+1)%maxi==0):
                    self.newframe()
                self.optionvariables.append(tk.StringVar(master))
                self.optionvariables[i].trace("w", lambda *args,x=i:self._preoption_click(x,*args))
                if (type(optionmenu[0])==type(list())):
                    self.optionvariables[i].set(option[0]) # default value
                    w = tk.OptionMenu(master, self.optionvariables[i], *option)
                else:
                    self.optionvariables[i].set(option["default"]) # default value
                    w = tk.OptionMenu(master, self.optionvariables[i], *option["choices"])
                self.optionwidgets.append(w)
                w.pack()
                self.pw[self.frames].add(w,stretch="always")
        
        
        self.line1=0
        self.outval=""
        self.master.geometry(geom)
    def setimage(self,index,filename):
        pass
    def getimage(self,index,filename):
        pass
    def setfont(self,name="Segoe UI",size=20,weight=tkinter.font.NORMAL):
        Font_tuple = (name, size, weight) 
        self.holeinputtxt.configure(font = Font_tuple) 
    def setalpha(self,alpha):
        self.master.attributes("-alpha", alpha)
    def ResetOptions(self,i,newoptions=[]):
        self.optionmenulist[i]=newoptions
        self.optionvariables[i].set('')
        self.optionwidgets[i]['menu'].delete(0, 'end')
        for choice in newoptions:
            self.optionwidgets[i]['menu'].add_command(label=choice, command=tk._setit(self.optionvariables[i], choice))
        self.setoptiontextindex(i,0)
    def defaultcallback(self,*args):
        pass
    def settoggle(self,i,value):
        self.togs[i].set(value)
    def gettoggle(self,i):
        self.togs[i].get()
    def setcheck(self,i,value):
        self.chvars[i].set(value)
    def getcheck(self,i):
        return self.chvars[i].get()
    def _preslider(self,i,event):
        self.callback("slider",i,self.sliders[i][0],event)
    def _pre_checkbox(self,i):
        self.callback("check",i,self.checkboxes[i][0],self.getcheck(i)=="1")
    def _preinputtext(self,i,name,value):
        self.callback("input",i,name,value)
    def _preoption_click(self,i,*args):
        t=self.getoptiontext(i)
        name=self.optionmenulist[i][0]
        if (type(self.optionmenu[i])==type(dict())):name=self.optionmenu[i]["title"]
        self.callback("option",i,name,t)
    def _prebutton_click(self,index):
        if len(self.buttondata[index])<3:
            self.buttondata[index][1]()
            return
        t=self.getbuttontext(index)
        if (t==self.buttondata[index][0]):
            self.setbuttontext(index,self.buttondata[index][2])
        else:self.setbuttontext(index,self.buttondata[index][0])
        self.buttondata[index][1]()
    def getinputtextbyname(self,name):
        index=self.inputtextnames.index(name)
        mytext= self.inp[index].gettext()
        return mytext
    def setinputtextbyname(self,name,text):
        index=self.inputtextnames.index(name)
        mytext= self.inp[index].settext(text)
    
    def getinputtext(self,index):
        mytext= self.inp[index].gettext()
        return mytext
    def setinputtext(self,index,text):
        self.inp[index].settext(text)
    def getoptiontext(self,index):
        mytext= self.optionvariables[index].get()
        return mytext
    def setoptiontext(self,index,text):
        self.optionvariables[index].set(text)
    def getoptiontextindex(self,index):
        mytext= self.optionvariables[index].get()
        i=self.optionmenulist[index].index(mytext)
        return i
    def getoptionindex(self,index):
        mytext= self.optionvariables[index].get()
        i=self.optionmenulist[index].index(mytext)
        return i
    def setoptiontextindex(self,index,index2):
        self.optionvariables[index].set(self.optionmenulist[index][index2])
    def settitle(self,title):
        self.master.title(title)
    def setbuttontext(self,index,my_text):
        self.buttons[index].config(text = my_text)
    def getbuttontext(self,index):
        mytext= self.buttons[index].cget('text')
        return mytext
    def getbigtext(self):
        t = self.holeinputtxt.get("1.0",'end')[:-1]
        return t
    def insertbigtext(self,text):
        self.holeinputtxt.insert(tk.INSERT, text)
    def setbigtext(self,text):
        t = self.holeinputtxt.get("1.0",'end')[:-1]
        if (t!=text):
            self.holeinputtxt.delete("1.0", tk.END)
            self.holeinputtxt.insert("1.0", text)
        self.holeinputtxt.see(tk.END)
    def setlabeltext(self,my_text):
        self.modellabel.config(text = my_text)
    def clearout1(self):
        self.holeinputtxt.delete("1.0", tk.END)
        self.line1=0
        self.outval=""
    def clearout(self):
        self.clearout1()
    def clear(self):
        self.clearout1()
    def printout1(self,*text,**kwargs):
        end=""
        endd=""
        if "sep" in kwargs:
            endd=kwargs["sep"]
        with io.StringIO() as buf, redirect_stdout(buf):
            for t in text:
                print(t,end=endd)
            print("")
            self.outval+= buf.getvalue()
        self.printout1flush()
        return
    def printout1flush(self):
        self.holeinputtxt.delete("1.0", tk.END)
        self.holeinputtxt.insert("1.0", self.outval)
        self.holeinputtxt.see(tk.END)
    def printout(self,*text,**kwargs):
        self.printout1(*text,*kwargs)
        return
    def print(self,*text,**kwargs):
        self.printout1(*text,*kwargs)
        return
    def printoutflush(self):
        self.printout1flush()
    def printflush(self):
        self.printout1flush()
    def option_changed(var, index, mode):
        text=dropdownVar.get()
        ind=OPTIONS.index(text)
        self.boardinputtxt.delete("1.0", tk.END)
        self.boardinputtxt.insert("1.0", text+str(w.shape)+str(w))
    def any(self,name, alternates):
        "Return a named group pattern matching list of alternates."
        return "(?P<%s>" % name + "|".join(alternates) + ")"
    def make_pat(self):
        import keyword
        import re
        import builtins
        kw = r"\b" + self.any("KEYWORD", keyword.kwlist) + r"\b"
        builtinlist = [str(name) for name in dir(builtins)
                                            if not name.startswith('_') and \
                                            name not in keyword.kwlist]
        builtin = r"([^.'\"\\#]\b|^)" + self.any("BUILTIN", builtinlist) + r"\b"
        comment = self.any("COMMENT", [r"#[^\n]*"])
        stringprefix = r"(?i:r|u|f|fr|rf|b|br|rb)?"
        sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
        dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
        sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
        dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
        string = self.any("STRING", [sq3string, dq3string, sqstring, dqstring])
        return kw + "|" + builtin + "|" + comment + "|" + string +\
               "|" + self.any("SYNC", [r"\n"])
    def highlight(self):
        cdg = ic.ColorDelegator()
        cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + self.make_pat(), re.S)
        cdg.idprog = re.compile(r'\s+(\w+)', re.S)

        cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}

        # These five lines are optional. If omitted, default colours are used.
        if (self.bg=="black"):
            cdg.tagdefs['COMMENT'] = {'foreground': '#dd0000', 'background': '#000000'}
            cdg.tagdefs['KEYWORD'] = {'foreground': '#0000FF', 'background': '#000000'}
            cdg.tagdefs['BUILTIN'] = {'foreground': '#FF0000', 'background': '#000000'}
            cdg.tagdefs['STRING'] = {'foreground': '#00aa00', 'background': '#000000'}
            cdg.tagdefs['DEFINITION'] = {'foreground': '#FF00FF', 'background': '#000000'}
            cdg.tagdefs['ERROR'] = {'foreground': '#FF00FF', 'background': '#000000'}

        ip.Percolator(self.holeinputtxt).insertfilter(cdg)
    

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()


class _TabbedClass(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        
    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])
class TabbedWin():
    def __init__(self, root,tabs=[],wd=200,ht=200):
        self.master=root
        self.notebook = _TabbedClass(width=wd, height=ht)
        self.notebook.pack(side="top", fill="both", expand=True)
        for t in tabs:
            self.addtab(t[0],t[1])
    def addtab(self,title,color):
        frame = tk.Frame(self.notebook, background=color)
        self.notebook.add(frame, text=title)
