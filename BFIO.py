import tkinter as tk
import tkinter.font as tkFont

"""TODO
* don't erase the used input, rather gray them / put them in another widget

"""

class BFInput(tk.Frame):
    def __init__(self,root):
        # framestyle = {"background":"#202020"}
        framestyle = {}
        tk.Frame.__init__(self,root,borderwidth=1, relief=tk.RIDGE,**framestyle)

        frame_list = tk.Frame(self,**framestyle)
        frame_txt = tk.Frame(frame_list,**framestyle)
        lbl_list = tk.Label(frame_list, text="Current Input List :")
        self.displayed_list_var = tk.StringVar()
        self.inp_list_display = tk.Entry(frame_txt,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var, disabledforeground="#000000")
        self.scrollbar_list = tk.Scrollbar(frame_txt, orient="horizontal", command = self.inp_list_display.xview)
        self.inp_list_display.configure(xscrollcommand=self.scrollbar_list.set)
        self.displayed_list_var.set("")

        frame_list.bind("<Configure>", self.update_scrollbar_visibility)

        frame_input = tk.Frame(self)
        lbl1 = tk.Label(frame_input,text="Add Input :")
        self.new_inp = tk.StringVar()
        validate_cmd = self.register(self.inp_validator)
        self.entry = tk.Entry(frame_input, width=15, textvariable=self.new_inp, validate='all', validatecommand=(validate_cmd,'%d','%S') )
        self.new_inp.set("")
        
        frame_type = tk.Frame(frame_input)
        self.inp_type = tk.IntVar()
        self.b_dec = tk.Radiobutton(frame_type, variable=self.inp_type, text="Decimal", value=1, command = lambda : self.new_inp.set(""))
        self.b_ascii = tk.Radiobutton(frame_type, variable=self.inp_type, text="Ascii Code", value=2, command = lambda : self.new_inp.set(""))
        self.inp_type.set(1)



        frame_used = tk.Frame(self)
        frame_txt_used = tk.Frame(frame_used)
        lbl_used = tk.Label(frame_used, text="Used Input :")
        self.displayed_list_var_used = tk.StringVar()
        self.inp_list_display_used = tk.Entry(frame_txt_used,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var_used, disabledforeground="#505050")
        self.scrollbar_list_used = tk.Scrollbar(frame_txt_used, orient="horizontal", command = self.inp_list_display_used.xview)
        self.inp_list_display_used.configure(xscrollcommand=self.scrollbar_list_used.set)
        self.displayed_list_var_used.set("")
        frame_used.bind("<Configure>", self.update_scrollbar_visibility)
        self.button_repack = tk.Button(frame_used, text="Repack used\ninputs",command=self.repack_input)


        lbl_list.pack(side=tk.LEFT, padx=5, pady=15)
        self.inp_list_display.pack(fill='x')
        # self.scrollbar_list.pack(fill="x")
        frame_txt.pack(side=tk.LEFT,expand=True,fill='x',padx=5,pady=5)

        frame_list.pack(side=tk.TOP, expand=False, fill='x')

        lbl1.pack(side=tk.LEFT, padx=5)
        self.entry.pack(side=tk.LEFT,fill='x',expand=True)
        
        self.b_dec.pack(side=tk.TOP,anchor="w")
        self.b_ascii.pack(side=tk.BOTTOM,anchor="w")
        frame_type.pack(side=tk.LEFT,padx=5,pady=5)

        frame_input.pack(side=tk.TOP,fill='x')


        lbl_used.pack(side=tk.LEFT, padx=5, pady=15)
        self.inp_list_display_used.pack(fill='x')
        # self.scrollbar_list_used.pack(fill="x")
        frame_txt_used.pack(side=tk.LEFT,expand=True,fill='x',padx=5,pady=5)
        self.button_repack.pack(side=tk.LEFT)

        frame_used.pack(side=tk.TOP, expand=False, fill='x',padx=5,pady=5)


        self.input_list = [] # list of numbers to be used as input for the BF program

        self.entry.bind("<KeyPress>", self.kbevt)
        # self.update_scrollbar_visibility()

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
    
    def repack_input(self):
        # print("oki on repack :):):):)")
        tokens = self.displayed_list_var_used.get().split()
        if len(tokens) == 0: return

        for t in reversed(tokens):
            self.add_input(t, 1, prepend=True)
        
        self.displayed_list_var_used.set("")

        self.update_scrollbar_visibility()

    def add_input(self,inp : str, force_type=-1, prepend=False):
        # print(f"adding '{inp}' as " + ("ascii codes" if self.inp_type.get() == '2' else "numeric values"))
        if (self.inp_type.get() == 1 and force_type == -1) or force_type==1: #decimal
            tokens = inp.split()
            for t in tokens:
                if prepend:
                    self.displayed_list_var.set( str(int(t)) + (" " if self.input_list else "") + self.displayed_list_var.get() )
                    self.input_list[0:0] = [ int(t) ]
                else:
                    self.displayed_list_var.set( self.displayed_list_var.get() + (" " if self.input_list else "")+ str(int(t)) )
                    self.input_list.append( int(t) )

        else: # ascii
            for c in inp:
                if prepend:
                    self.displayed_list_var.set( str(ord(c)) + (" " if self.input_list else "") + self.displayed_list_var.get() )
                    self.input_list[0:0] = ( ord(c) )
                else:
                    self.displayed_list_var.set( self.displayed_list_var.get() + (" " if self.input_list else "") + str(ord(c)) )
                    self.input_list.append( ord(c) )
        self.update_scrollbar_visibility()

    def get_input(self):
        if self.input_list:
            curr_text = self.displayed_list_var.get()
            curr_text_used = self.displayed_list_var_used.get()
            if " " in curr_text:
                self.displayed_list_var.set( curr_text[ curr_text.index(" ")+1:] )
            else:
                self.displayed_list_var.set("")
            
            self.displayed_list_var_used.set( self.displayed_list_var_used.get() + " " + str(self.input_list[0]))

            self.update_scrollbar_visibility()
            return self.input_list.pop(0)
        else:
            print("Empty input list, returning 0")
            self.displayed_list_var_used.set( self.displayed_list_var_used.get() + " 0")
            return 0

    def update_scrollbar_visibility(self, e=None):
        font_measure = tkFont.nametofont("TkFixedFont").measure(" ")
        # print(len(self.inp_list_display.get())*font_measure, self.inp_list_display.winfo_width())
        if len(self.inp_list_display.get()) == 0 and self.inp_list_display.winfo_width() == 1:
            return
        
        if (len(self.inp_list_display.get())+1)*font_measure > self.inp_list_display.winfo_width():
            self.scrollbar_list.pack(fill="x")

        else:
            self.scrollbar_list.pack_forget()
        
        if len(self.inp_list_display_used.get()) == 0 and self.inp_list_display_used.winfo_width() == 1:
            return
        
        if (len(self.inp_list_display_used.get())+1)*font_measure > self.inp_list_display_used.winfo_width():
            self.scrollbar_list_used.pack(fill="x")
        else:
            self.scrollbar_list_used.pack_forget()
            
        


class BFOutput(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root, borderwidth=1, relief=tk.RIDGE)

        # if set to -1, tabs are displayed as tabs (tabs align every 4 chars)
        # if not, tabs are printed as x spaces
        # note that default tkinter implementation of \t seems wrong, or at least I can't make it work properly on my machine
        # so consider setting this to 4 or 8 (spaces)
        self.tabs_as_spaces = 4

        lbl = tk.Label(self, text="Output :")

        self.var_chkbox_wrap = tk.IntVar()

        self.chkbox_wrap = tk.Checkbutton(self, text="auto-wrap", indicatoron=True, bd=1,relief=tk.RAISED,
            variable=self.var_chkbox_wrap,
            command=self.set_autowrap)

        frame_txt = tk.Frame(self)

        tab_size = tkFont.nametofont("TkFixedFont").measure("    ")

        self.txt = tk.Text(frame_txt, wrap='none',height=10,width=40, state='disabled', bg="#CCCCCC",tabs=tab_size)

        self.hscroll = tk.Scrollbar(frame_txt, orient="horizontal", command= self.txt.xview)
        self.vscroll = tk.Scrollbar(frame_txt, orient="vertical", command= self.txt.yview)
        self.txt.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)

        self.btn_clear = tk.Button(self, text="Clear output", justify='center',command=self.clear_output)


        self.txt.grid(row=0,column=0,sticky="nsew")
        self.vscroll.grid(row=0,column=1,sticky="nsew")
        self.hscroll.grid(row=1,column=0,sticky='nsew')

        lbl.grid(row=0,column=0,sticky="w",padx=5,pady=5)
        self.btn_clear.grid(row=0,column=8,sticky="e",padx=(0,5),pady=5)
        self.chkbox_wrap.grid(row=0,column=9,sticky="e",padx=(0,5),pady=5)

        frame_txt.grid(row=1,column=0, columnspan=10, padx=5,pady=(0,5))


        self.txt.tag_config("not_printable", background="#E0C0E0",relief=tk.GROOVE,borderwidth=2,tabs=(tab_size,'right'))
        self.txt.tag_config("special", background="#E0E0C0",tabs=(tab_size,))


    def clear_output(self):
        self.txt.configure(state='normal')
        self.txt.delete('1.0', tk.END)
        self.txt.configure(state='disabled')
    
    def set_autowrap(self,val=None):
        """
        val: - None > sets autowrap according to the checkbox
             - True/False > sets autowrap to true/false, and updates checkbox
        """
        if val != None:
            self.var_chkbox_wrap.set(val)
        self.txt.configure(wrap='char' if self.var_chkbox_wrap.get() else 'none')

    def add(self,txt,color=None):
        """
        color : - None > default color
                - 'not_printable' > by default, #FF00FF (magenta)
                - 'special'       > by default, #FFFF00 (yellow)

        """
        self.txt.configure(state='normal')
        if txt == "\t" and self.tabs_as_spaces != -1:
            txt = " "*(self.tabs_as_spaces-(len(self.txt.get("end-1c linestart", "end-1c lineend")))%self.tabs_as_spaces)
        if not color:
            self.txt.insert(tk.END, txt)
        else:
            self.txt.insert(tk.END, txt, (color,))
        self.txt.configure(state='disabled')


if __name__ == '__main__':
    app = tk.Tk()
    app.title("BFIO test")

    app.option_add("*Font", "TkFixedFont")

    inp = BFInput(app)
    inp.pack(padx=10,pady=10, anchor="nw",fill="x")

    # inp.add_input("un bon test !\n\thihi\ta\nqq\teeeee\taa",force_type=2)
    inp.add_input("123412341234\n\t1234\n\t\t1234\n\x03aaa\ta\taaa\n|\n|",force_type=2)
    # for i in range(100,115):
    #     inp.add_input(str(i))


    out = BFOutput(app)
    out.pack(padx=10,pady=10, anchor="nw",fill="both",expand=True)

    def aa(e=None):
        # out.add(chr(inp.get_input()))
        # return
        r = repr(chr(inp.get_input()))[1:-1]

        if len(r) == 1:
            out.add(r)
        else:
            if r == "\\n":
                # print("special n")
                out.add(" ", color="special")
                out.add("\n")
            elif r == "\\t":
                # print("special t")
                out.add("\t", color="special")
            else:
                # print("not_printable")
                out.add(r,"not_printable")

    app.bind_all("w", aa)

    app.bind_all("<Escape>", lambda e: app.destroy())

    app.mainloop()