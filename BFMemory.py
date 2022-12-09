import tkinter as tk
import numpy as np

class BFMemory(tk.Frame):
    """
    this widget is used to show and store the current state of the BF memory (+cursor position)

    - setCell(i,decimal_vamue) sets a cell's value (may not be the cell pointed by the cursor)
    - getCell(i) returns cell's value

    """

    def __init__(self,root,memorySize = 30000, cellType = np.uint8, lineDisplay=16):
        
        tk.Frame.__init__(self,root, relief=tk.RIDGE, borderwidth=1)
        self.root = root

        self.lineDisplay = lineDisplay
        self.memSize = memorySize
        self.type = cellType

        self.data = [[f"0x{i:04x}",0,""] for i in range(self.memSize) ]
        self.scroll_val = 0 # de combien on décale l'affichage dans data

        self.labels_title = []
        for i,titre in enumerate(["@","dec","ascii"]):
            l = tk.Label(self, text=titre,bg = "#FFFFFF",borderwidth=1,relief="solid",padx=10,pady=5, font='TkFixedFont')
            # l.bindtags(("Memory",) + l.bindtags())
            l.grid(row=0,column=i,sticky = "NSEW")
            self.labels_title.append(l)

        self.displayed = [ [0 for j in range(3)] for i in range(self.lineDisplay) ]

        for i in range(self.lineDisplay):
            for j in range(3):
                l = tk.Label(self,text= "", width = self.labels_title[j].cget("width"),bg = "#FFFFFF",borderwidth=1,relief="solid",pady=2, font='TkFixedFont')
                
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
        for i in range(self.lineDisplay):
            l = self.displayed[i]
            valeurs = self.data[i+self.scroll_val]

            for label,val in zip(l,valeurs):
                label.config(text=str(val))

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

    testSize=256*256

    mem = BFMemory(app, memorySize=testSize, lineDisplay=16)
    mem.pack(padx=10,pady=10)
    
    print(mem.bindtags())

    import random as rd
    for i in range(300):
        mem.setCell(rd.randint(0,testSize-1), rd.randint(0,255))

    mem.setCell(0,0)

    app.mainloop()

    # TODO : last cell is not being displayed