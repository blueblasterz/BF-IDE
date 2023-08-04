import tkinter as tk
import numpy as np
import tkinter.font as tkFont
import tkinter.ttk as ttk

# class Bordered_Label(tk.Label):
#     """
#     A simple label, but with an additionnal "borderColor" option
#     (relief is ignored, borderwitdh is overwritten)
#     """
#     def __init__(self, root, *args, **kwargs):
#         keys = kwargs.keys()
#         bd = 1
#         bc = "#000000"
#         for k in keys:
#             if k in ["bd", "borderwidth"]:
#                 bd = kwargs[k]
#                 del kwargs[k]
#             elif k in ["bc", "bordercolor"]:
#                 bc = kwargs[k]
#                 del kwargs[k]
#             elif k in ["relief"]:
#                 del kwargs[k]
#         tk.Frame.__init__(self,root,*args, **kwargs)


class BFMemory(ttk.Frame):
    """
    this widget is used to show and store the current state of the BF memory (+cursor position)

    - setCell(i,decimal_vamue) sets a cell's value (may not be the cell pointed by the cursor)
    - getCell(i) returns cell's value

    """
    def __init__(self,root,memorySize = 30000, cellType = np.uint8, lineDisplay=16):
        
        style_bfinp = ttk.Style()
        style_bfinp.configure("frame_bfmem.TFrame", borderwidth=1, relief='raised')
        ttk.Frame.__init__(self,root,style="frame_bfmem.TFrame")

        # self.bordercolor = "#00FFFF"
        self.bordercolor = "#808080"
        self.highlightcolor = "#353535"

        self.active_line = 0
        self.active_line_idx = -1
        
        self.root = root

        self.lineDisplay = lineDisplay
        self.memSize = memorySize
        self.type = cellType

        self.data = [[f"0x{i:04x}",0,""] for i in range(self.memSize) ]
        self.scroll_val = 0 # de combien on décale l'affichage dans data

        self.labels_title = []
        for i,titre in enumerate(["@","dec","ascii"]):
            l = ttk.Label(self, text=titre)
            # l.bindtags(("Memory",) + l.bindtags())
            l.grid(row=0,column=i,sticky = "NSEW",ipadx=2)
            self.labels_title.append(l)

        self.displayed = [ [0 for j in range(3)] for i in range(self.lineDisplay) ]

        for i in range(self.lineDisplay):
            for j in range(3):
                l = tk.Label(self,
                             text= "",
                             width=7 if j==0 else 4 if j==1 else 5 )
                
                # l.bindtags(("Memory",) + l.bindtags())
                # if i==0: print(l.bindtags())
                l.grid(row=i+1,column=j,sticky="NSEW")

                self.displayed[i][j] = l
        # self.bindtags(("Memory",) + self.bindtags() )
        
        self.bind("<Enter>", self.handler_enter)
        self.bind("<Leave>", self.handler_leave)

        self.bind("<Button>", self.scrollevt)

        # for some reason, without this, the scoll event does not register
        # but the keypresses do still work
        for child in self.winfo_children(): 
            child.bind("<Button>", self.scrollevt)
        
        self.bind("<KeyPress>", self.kbevt)
        self.bind("<KeyRelease>", self.kbevt)

        self.mods = []

        self.update_aff()

    def handler_enter(self,evt):
        self.focus_force()
        # self.bind_all("<Button>", self.scrollevt)

    def handler_leave(self,evt):
        self.root.focus_force()
        # self.unbind_all("<Button>")

    def kbevt(self,evt):
        # print(f"keypressed : {evt.keysym}")
        k = evt.keysym
        # print(self.mods, k, evt.type)
        if evt.type == tk.EventType.KeyPress: # press
            if k in ["Shift_L","Control_L"]:
                if not k in self.mods:
                    self.mods.append(k)
            elif k == "Up":
                if "Shift_L" in self.mods:
                    if "Control_L" in self.mods:
                        self.scroll(-4096)
                    else:
                        self.scroll(-self.lineDisplay)
                elif "Control_L" in self.mods:
                    self.scroll(-256)
                else :
                    self.scroll(-1)
            elif k == "Down":
                if "Shift_L" in self.mods:
                    if "Control_L" in self.mods:
                        self.scroll(4096)
                    else:
                        self.scroll(self.lineDisplay)
                elif "Control_L" in self.mods:
                    self.scroll(256)
                else :
                    self.scroll(1)
        elif evt.type == tk.EventType.KeyRelease: #release
            if k in ["Shift_L","Control_L"]:
                if  k in self.mods:
                    self.mods.pop(self.mods.index(k))

    def update_active_line(self,new=0):
        # print("call update")
        self.active_line = new
        self.update_aff()

    def scrollevt(self,evt):
        if evt.num == 4:
            self.scroll(-1)
        elif evt.num == 5:
            self.scroll(1)

    def scroll(self,n):
        if self.memSize <= n -1 + self.scroll_val + self.lineDisplay:
            n = self.memSize - self.scroll_val - self.lineDisplay

        self.scroll_val = max(0,self.scroll_val + n)
        self.update_aff()
        # print(self.scroll_val)


    def update_aff(self):
        # print(f"{self.scroll_val=}")
        # print(f"{self.active_line=}")
        # print(f"{self.active_line_idx=}")
        for i in range(self.lineDisplay):
            l = self.displayed[i]
            valeurs = self.data[i+self.scroll_val]

            for label,val in zip(l,valeurs):
                label.config(text=f" {str(val)} ",
                             bg="#000000")
            #TODO reset background only for previously highlighted lines

            # if i+self.scroll_val == self.active_line_idx:
            #     for label in l:
            #         label.config(bg="#000000")

        if self.scroll_val <= self.active_line \
        and self.active_line < self.scroll_val + self.lineDisplay:
            l = self.displayed[self.active_line-self.scroll_val]
            # for label in l:
            #     label.config(bg=self.highlightcolor)
            self.active_line_idx = self.active_line

    def setCell(self,i,val):
        if i>len(self.data) or self.data[i] == [""]*3:
            raise(IndexError(f"Trying to access cell {i} while memory size is {self.memSize}"))
        self.data[i][1] = val%256
        if val == 0:
            self.data[i][2] = ""
        else:
            self.data[i][2] = repr(chr(val%256))[1:-1]
        self.update_aff()

    def getCell(self,i):
        if i>=self.memSize or i < 0:
            raise(IndexError(f"Memory Error : out of range (trying to access {i}"
            " while memorysize is {self.memSize}"))
        return self.data[i][1]


if __name__ == '__main__':
    app = tk.Tk()
    app.title("test Memory")


    app.option_add("*Font", "TkFixedFont")
    app.tk.call("source","azure.tcl")
    app.tk.call("set_theme","dark")
    app.bind_all("<KeyPress-Escape>", lambda e: app.destroy())

    testSize=256*256

    mem = BFMemory(app, memorySize=testSize, lineDisplay=16)
    mem.pack(padx=10,pady=10)
    
    print(mem.bindtags())

    import random as rd
    for i in range(300):
        mem.setCell(rd.randint(0,testSize-1), rd.randint(0,255))

    mem.setCell(3,150)

    mem.focus_force()

    app.bind_all("r", lambda e: mem.update_aff())

    # app.after(1000, lambda: mem.update_active_line(5))

    app.mainloop()
