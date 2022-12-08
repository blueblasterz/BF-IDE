import tkinter as tk
import numpy as np

class Memory(tk.Frame):
    """
    this widget is used to show and store the current state of the BF memory (+cursor position)

    - setCell(i,decimal_vamue) sets a cell's value (may not be the cell pointed by the cursor)
    - getCell(i) returns cell's value

    """

    def __init__(self,root,memorySize = 30000, cellType = np.uint8, lineDisplay=10):
        
        tk.Frame.__init__(self,root, relief=tk.RIDGE, borderwidth=1)
        self.root = root
        self.pack()

        self.lineDisplay = lineDisplay
        self.memSize = memorySize
        self.type = cellType

        self.data = [[f"0x{i:04x}",0,""] for i in range(self.memSize) ]
        self.scroll_val = 0 # de combien on décale l'affichage dans data

        self.labels_titre = []
        for i,titre in enumerate(["@","dec","ascii"]):
            l = tk.Label(self, text=titre,bg = "#FFFFFF",borderwidth=1,relief="solid",padx=10,pady=5)
            # l.bindtags(("Memory",) + l.bindtags())
            l.grid(row=0,column=i,sticky = "NSEW")
            self.labels_titre.append(l)

        self.displayed = [ [0 for j in range(3)] for i in range(self.lineDisplay) ]

        for i in range(self.lineDisplay):
            for j in range(3):
                l = tk.Label(self,text= "", width = self.labels_titre[j].cget("width"),bg = "#FFFFFF",borderwidth=1,relief="solid",pady=2)
                
                # l.bindtags(("Memory",) + l.bindtags())
                # if i==0: print(l.bindtags())
                l.grid(row=i+1,column=j,sticky="NSEW")

                self.displayed[i][j] = l
        # self.bindtags(("Memory",) + self.bindtags() )
        
        # self.bind("<Enter>", lambda e: self.bind_all("<Button>", self.scrollevt))
        # self.bind("<Leave>", lambda e: self.unbind_all("<Button>"))
        self.bind("<Enter>", lambda e: self.bind_all("<Button>", self.scrollevt))
        self.bind("<Leave>", lambda e: self.unbind_all("<Button>"))
    def scrollevt(self,evt):
        if evt.num == 4:
            self.scroll(-1)
        elif evt.num == 5:
            self.scroll(1)

    def scroll(self,n):
        if self.memSize <= n + self.scroll_val + self.lineDisplay:
            return
            print(f"{n=}, {self.scroll_val=}")

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
        if chr(val%256).isprintable():
            self.data[i][2] = chr(val%256)
        else:
            self.data[i][2] = f"\\u{val%256:02x}"
        self.update_aff()

    def getCell(self,i):
        if i>=self.memSize or i < 0:
            raise(IndexError(f"Memory Error : out of range (trying to access {i}"
            " while memorysize is {self.memSize}"))
        return self.data[i][1]


if __name__ == '__main__':
    app = tk.Tk()
    app.title("test Memory")

    testSize=100

    mem = Memory(app, memorySize=testSize, lineDisplay=32)
    mem.pack(padx=10,pady=10)
    
    print(mem.bindtags())

    import random as rd
    for i in range(1000):
        mem.setCell(rd.randint(0,testSize-1), rd.randint(0,255))

    app.mainloop()

    # TODO : last cell is not being displayed