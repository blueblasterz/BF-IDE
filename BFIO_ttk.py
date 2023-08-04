import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

"""TODO
* don't erase the used input, rather gray them / put them in another widget

"""

class BFInput(ttk.Frame):
    def __init__(self,root):
        style_bfinp = ttk.Style()
        style_bfinp.configure("frame_bfinp.TFrame", borderwidth=1, relief='raised')
        ttk.Frame.__init__(self,root,style="frame_bfinp.TFrame")


        # display for the current input list
        frame_list = ttk.Frame(self)
        frame_txt = ttk.Frame(frame_list)
        lbl_list = ttk.Label(frame_list, text="Current Input List :")
        self.displayed_list_var = tk.StringVar()
        # self.inp_list_display = tk.Entry(frame_txt,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var, disabledforeground="#000000")
        self.inp_list_display = ttk.Entry(frame_txt,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var, foreground="#FFFFFF")
        self.scrollbar_list = ttk.Scrollbar(frame_txt, orient="horizontal", command = self.inp_list_display.xview)
        self.inp_list_display.configure(xscrollcommand=self.scrollbar_list.set)
        self.displayed_list_var.set("")
        # hide scrollbar if it is not needed
        frame_list.bind("<Configure>", self.check_if_scroll_necessary)

        lbl_list.pack(side=tk.LEFT, padx=5, pady=15)
        self.inp_list_display.pack(fill='x')
        # self.scrollbar_list.pack(fill="x")
        frame_txt.pack(side=tk.LEFT,expand=True,fill='x',padx=5,pady=5)



        # the entry for the data
        frame_input = ttk.Frame(self)
        lbl1 = ttk.Label(frame_input,text="Add Input :")
        self.new_inp = tk.StringVar()
        validate_cmd = self.register(self.inp_validator)
        self.entry = ttk.Entry(
            frame_input,
            width=15,
            textvariable=self.new_inp,
            validate='all',
            validatecommand=(validate_cmd,'%d','%S') )
        self.new_inp.set("")

        lbl1.pack(side=tk.LEFT, padx=5)
        self.entry.pack(side=tk.LEFT,fill='x',expand=True)
        

        # data type choice, between ascii and decimal
        frame_type = ttk.Frame(frame_input)
        self.inp_type = tk.IntVar()
        self.b_dec = ttk.Radiobutton(frame_type, variable=self.inp_type, text="Decimal", value=1, command = lambda : self.new_inp.set(""))
        self.b_ascii = ttk.Radiobutton(frame_type, variable=self.inp_type, text="Ascii Code", value=2, command = lambda : self.new_inp.set(""))
        self.inp_type.set(1)
        
        self.b_dec.pack(side=tk.TOP,anchor="w")
        self.b_ascii.pack(side=tk.BOTTOM,anchor="w")


        # display for "used" input
        frame_used = ttk.Frame(self)
        frame_txt_used = ttk.Frame(frame_used)
        lbl_used = ttk.Label(frame_used, text="Used Input :")
        self.displayed_list_var_used = tk.StringVar()
        # self.inp_list_display_used = tk.Entry(frame_txt_used,width=10, state=tk.DISABLED, textvariable=self.displayed_list_var_used, disabledforeground="#505050")
        self.inp_list_display_used = ttk.Entry(
            frame_txt_used,
            width=10,
            state=tk.DISABLED,
            textvariable=self.displayed_list_var_used)
        self.scrollbar_list_used = ttk.Scrollbar(
            frame_txt_used,
            orient="horizontal",
            command = self.inp_list_display_used.xview)
        self.inp_list_display_used.configure(xscrollcommand=self.scrollbar_list_used.set)
        self.displayed_list_var_used.set("")
        frame_used.bind("<Configure>", self.check_if_scroll_necessary)
        self.button_repack = ttk.Button(
            frame_used,
            text="Repack used\ninputs",
            command=self.repack_input)

        lbl_used.pack(side=tk.LEFT, padx=5, pady=15)
        self.inp_list_display_used.pack(fill='x')
        # self.scrollbar_list_used.pack(fill="x")
        frame_txt_used.pack(side=tk.LEFT,expand=True,fill='x',padx=5,pady=5)
        self.button_repack.pack(side=tk.RIGHT,expand=False)



        frame_list.pack(side=tk.TOP, expand=False, fill='x')

        frame_type.pack(side=tk.LEFT,padx=5,pady=5)

        frame_input.pack(side=tk.TOP,fill='x')

        frame_used.pack(side=tk.TOP, fill='x')


        self.input_list = [] # list of numbers to be used as input for the BF program

        self.entry.bind("<KeyPress>", self.kbevt)
        # self.check_if_scroll_necessary()

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

        self.check_if_scroll_necessary()

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
        self.check_if_scroll_necessary()

    def get_input(self):
        if self.input_list:
            curr_text = self.displayed_list_var.get()
            curr_text_used = self.displayed_list_var_used.get()
            if " " in curr_text:
                self.displayed_list_var.set( curr_text[ curr_text.index(" ")+1:] )
            else:
                self.displayed_list_var.set("")
            
            self.displayed_list_var_used.set( self.displayed_list_var_used.get() + " " + str(self.input_list[0]))

            self.check_if_scroll_necessary()
            return self.input_list.pop(0)
        else:
            print("Empty input list, returning 0")
            self.displayed_list_var_used.set( self.displayed_list_var_used.get() + " 0")
            return 0

    def check_if_scroll_necessary(self, e=None):
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
            

class BFOutput(ttk.Frame):
    def __init__(self,root):
        # tk.Frame.__init__(self,root, borderwidth=1, relief=tk.RIDGE)
        style_bfinp = ttk.Style()
        style_bfinp.configure("frame_bfinp.TFrame", borderwidth=1, relief='raised')
        ttk.Frame.__init__(self,root,style="frame_bfinp.TFrame")

        tab_size = tkFont.nametofont("TkFixedFont").measure("    ")
        # if set to -1, tabs are displayed as tabs (tabs align every 4 chars)
        # if not, tabs are printed as x spaces
        # note that default tkinter implementation of \t seems wrong, or at least I can't make it work properly on my machine
        # so consider setting this to 4 or 8 (spaces)
        self.tabs_as_spaces = 4
        
        style_not_printable = {
            "background":"#305030",
            "relief":tk.GROOVE,
            "borderwidth":2,
            "tabs":(tab_size,'right')
        }
        style_special = {
            "background":"#404060",
            "tabs":(tab_size,)
        }


        frame_info = ttk.Frame(self)
        lbl = ttk.Label(frame_info, text="Output :")
        # wrap and clear output button
        frame_buttons = ttk.Frame(frame_info)
        self.var_chkbox_wrap = tk.IntVar()
        self.chkbox_wrap = ttk.Checkbutton(
            frame_buttons,
            text="auto-wrap",
            # indicatoron=True,
            variable=self.var_chkbox_wrap,
            command=self.set_autowrap)
        self.btn_clear = ttk.Button(
            frame_buttons,
            text="Clear output",
            command=self.clear_output)
        
        self.btn_clear.pack(side=tk.LEFT,padx=(0,5),pady=5)
        self.chkbox_wrap.pack(side=tk.RIGHT,padx=(0,5),pady=5)

        lbl.pack(side=tk.LEFT)
        frame_buttons.pack(side=tk.RIGHT)

        # display, with scrollbars
        frame_txt = ttk.Frame(self)
        self.txt = tk.Text(
            frame_txt,
            wrap='none',
            height=10,
            width=40,
            state='disabled',
            bg="#101010",
            tabs=tab_size)
        self.hscroll = ttk.Scrollbar(frame_txt, orient="horizontal", command= self.txt.xview)
        self.vscroll = ttk.Scrollbar(frame_txt, orient="vertical", command= self.txt.yview)
        self.txt.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)
        frame_txt.grid_columnconfigure(0,weight=1)
        frame_txt.grid_rowconfigure(0,weight=1)
        self.txt.grid(row=0,column=0,sticky="nesw")
        self.vscroll.grid(row=0,column=1,sticky="ns")
        self.hscroll.grid(row=1,column=0,sticky="ew")

        frame_info.pack(side=tk.TOP,fill='x')
        frame_txt.pack(side=tk.BOTTOM, expand=True,fill='both')

        self.grid_rowconfigure(tuple(range(10)), weight=1)
        self.grid_columnconfigure(tuple(range(20)),weight=1)
        self.txt.tag_config(
            "not_printable",
            **style_not_printable
            )
        self.txt.tag_config(
            "special",
            **style_special
            )


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

    app.tk.call("source","azure.tcl")
    app.tk.call("set_theme","dark")

    inp = BFInput(app)
    inp.pack(padx=10,pady=10, anchor="nw",fill="x")

    # inp.add_input("un bon test !",force_type=2)
    inp.add_input("123412341234\n\t1234\n\t\t1234\n\x03aaa\ta\taaa\n|\n|",force_type=2)
    # for i in range(100,115):
    #     inp.add_input(str(i))

    # app.bind_all("w", lambda e: print(inp.get_input()))

    app.bind_all("<KeyPress-Escape>", lambda e: app.destroy())

    out = BFOutput(app)
    out.pack(padx=10,pady=10, anchor="nw",expand=True,fill="both")
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

    app.mainloop()