import tkinter as tk
import tkinter.font as tkFont

"""TODO
* don't erase the used input, rather gray them / put them in another widget

"""

class BFInput(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root,borderwidth=1, relief=tk.RIDGE)

        frame_list = tk.Frame(self)
        frame_txt = tk.Frame(frame_list)
        lbl_list = tk.Label(frame_list, text="Current Input List :")
        self.displayed_list_var = tk.StringVar()
        self.inp_list_display = tk.Entry(frame_txt,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var, disabledforeground="#000000")
        self.scrollbar_list = tk.Scrollbar(frame_txt, orient="horizontal", command = self.inp_list_display.xview)
        self.inp_list_display.configure(xscrollcommand=self.scrollbar_list.set)
        self.displayed_list_var.set("")

        frame_list.bind("<Configure>", self.check_if_scroll_necessary)

        lbl1 = tk.Label(self,text="Add Input :")

        self.new_inp = tk.StringVar()
        validate_cmd = self.register(self.inp_validator)
        self.entry = tk.Entry(self, width=15, textvariable=self.new_inp, validate='all', validatecommand=(validate_cmd,'%d','%S') )
        self.new_inp.set("")
        
        frame_type = tk.Frame(self)
        self.inp_type = tk.IntVar()
        self.b_dec = tk.Radiobutton(frame_type, variable=self.inp_type, text="Decimal", value=1, command = lambda : self.new_inp.set(""))
        self.b_ascii = tk.Radiobutton(frame_type, variable=self.inp_type, text="Ascii Code", value=2, command = lambda : self.new_inp.set(""))
        self.inp_type.set(1)

        lbl_list.pack(side=tk.LEFT, padx=5, pady=15)
        self.inp_list_display.pack(fill='x')
        self.scrollbar_list.pack(fill="x")
        frame_txt.pack(side=tk.LEFT,expand=True,fill='x',padx=5,pady=5)

        frame_list.pack(side=tk.TOP, expand=False, fill='x')

        lbl1.pack(side=tk.LEFT, padx=5)
        self.entry.pack(side=tk.LEFT,fill='x',expand=True)
        
        self.b_dec.pack(side=tk.TOP,anchor="w")
        self.b_ascii.pack(side=tk.BOTTOM,anchor="w")
        frame_type.pack(side=tk.LEFT,padx=5,pady=5)


        self.input_list = [] # list of numbers to be used as input for the BF program

        self.entry.bind("<KeyPress>", self.kbevt)

    def inp_validator(self, cause : str, value : str):
        # print(f"{cause = } , {value = }")
        if cause == '1':
            if self.inp_type.get() == 1 and not value in " 0123456789":
                return False
        return True

    def kbevt(self,e : tk.Event):
        k = e.keysym
        if k == "Return":
            self.add_input(self.new_inp.get())
            self.new_inp.set("")

    def add_input(self,inp : str):
        # print(f"adding '{inp}' as " + ("ascii codes" if self.inp_type.get() == '2' else "numeric values"))
        if self.inp_type.get() == 1: #decimal
            tokens = inp.split()
            for t in tokens:
                self.displayed_list_var.set( self.displayed_list_var.get() + (" " if self.input_list else "")+ str(int(t)) )
                self.input_list.append( int(t) )

        else: # ascii
            for c in inp:
                self.displayed_list_var.set( self.displayed_list_var.get() + (" " if self.input_list else "") + str(ord(c)) )
                self.input_list.append( ord(c) )
        self.check_if_scroll_necessary()

    def get_input(self):
        if self.input_list:
            curr_text = self.displayed_list_var.get()
            if " " in curr_text:
                self.displayed_list_var.set( curr_text[ curr_text.index(" ")+1:] )
            else:
                self.displayed_list_var.set("")
            self.check_if_scroll_necessary()
            return self.input_list.pop(0)
        else:
            print("Empty input list, returning 0")
            return 0

    def check_if_scroll_necessary(self, e=None):
        font_measure = tkFont.nametofont("TkFixedFont").measure(" ")
        # print(len(self.inp_list_display.get())*font_measure, self.inp_list_display.winfo_width())
        if (len(self.inp_list_display.get())+1)*font_measure > self.inp_list_display.winfo_width():
            self.scrollbar_list.pack(fill="x")
        else:
            self.scrollbar_list.pack_forget()

class BFOutput(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)


if __name__ == '__main__':
    app = tk.Tk()
    app.title("BFIO test")

    app.option_add("*Font", "TkFixedFont")

    inp = BFInput(app)
    inp.pack(padx=10,pady=10, anchor="nw",fill="x")

    for i in range(100,115):
        inp.add_input(str(i))

    app.bind_all("w", lambda e: print(inp.get_input()))

    out = BFOutput(app)
    out.pack(padx=10,pady=10, anchor="nw",fill="x")

    app.mainloop()