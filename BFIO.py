import tkinter as tk

class BFInput(tk.Frame):
    def __init__(self,root,width=30):
        tk.Frame.__init__(self,root)
        self.label = tk.Label(self,text="Input : ")
        self.entry = tk.Entry(self, width=width)

        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT)


class BFOutput(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)


if __name__ == '__main__':
    app = tk.Tk()
    app.title("BFIO test")

    inp = BFInput(app)
    inp.pack()

    app.mainloop()