import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import clipboard

"""
BFCodeArea is a widget that extends from tk.Frame
it contains a tk.Text widget, that does some syntax highlighting for BF

TODO:
* vertical scrollbar
* load from file 
    * with a function that the IDE will use, no GUI stuff
    * save, save as will be done from the IDE itself
* horizontal scrollbar ? or force the usual limit of 80 chars
* make the syntax highlight parameters (self.syntax_params) loadable from a json file
    * need some special instructions and treatment to allow for bold and italic
    * editable within the (future) option menu
* display all useless "<>", "><", "+-", "-+" as warnings
* display detectable infinite loops as errors
  (maybe this needs to be done from the IDE, not the BFCodeArea itself)


"""

class BFCodeArea(ttk.Frame):
    def __init__(self,root, width=80,height=20):
        style_bfinp = ttk.Style()
        style_bfinp.configure("frame_bfcode.TFrame", borderwidth=0, relief='raised')
        ttk.Frame.__init__(self,root,style="frame_bfcode.TFrame")

        tab_size = tkFont.nametofont("TkFixedFont").measure("    ")

        font_italic = tkFont.nametofont("TkFixedFont").copy()
        font_italic.configure(slant="italic")
        font_bold = tkFont.nametofont("TkFixedFont").copy()
        font_bold.configure(weight="bold")
        self.syntax_params = {
            "default": { 
                "params": { "foreground" : "#606060", "font":font_italic, "insertbackground":"#FFFFFF" },
                "tag_name": "syntax-default",
            },
            "+": { 
                "params": {"foreground" : "#00F000", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax-+",
                # "bind_name": "+",
            },
            "-": { 
                "params": {"foreground" : "#F00000", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax--",
                # "bind_name": "-",
            },
            ",": { 
                "params": {"foreground" : "#00B0B0", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax-,",
                # "bind_name": ",",
            },
            ".": { 
                "params": {"foreground" : "#00B0B0", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax-.",
                # "bind_name": ".",
            },
            "<": { 
                "params": {"foreground" : "#C08000", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax-<",
                # "bind_name": "<less>",
            },
            ">": { 
                "params": {"foreground" : "#C08000", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax->",
                # "bind_name": "<greater>",
            },
            "[": { 
                "params": {"foreground" : "#C0C000", "font":tkFont.nametofont("TkFixedFont") },
                "tag_name": "syntax-[",
                # "bind_name": "["
            },
            "]": { 
                "params": {"foreground" : "#C0C000", "font":tkFont.nametofont("TkFixedFont")},
                "tag_name": "syntax-]",
                # "bind_name": "]",
            },
            "highlight_bracket": {
                "params": { "foreground":"#FFFF00", "relief": tk.GROOVE, "borderwidth": 1, "font":font_bold },
                "tag_name": "syntax-highlight_bracket",
            },
            "highlight_error": {
                "params" : { "background":"#FF0000", "font":font_italic },
                "tag_name": "syntax-highlight_error",
            },
        }
        self.jump_table = {}

        frame_txt = ttk.Frame(self)
        self.txt = tk.Text(frame_txt,
                           width=width,
                           height=height,
                           **self.syntax_params["default"]["params"],
                           bg="#000000",
                           undo=True,
                           autoseparators=True,
                           maxundo=-1,
                           tabs=tab_size)
        self.vscroll = ttk.Scrollbar(frame_txt,
                                     orient="vertical",
                                     command=self.txt.yview )

        self.txt.configure(yscrollcommand=self.vscroll.set)

        self.txt.grid(row=0,column=0,sticky = "nsew")
        self.vscroll.grid(row=0,column=1,sticky="ns")

        frame_txt.grid(row=0,column=0, sticky="nsew", padx=5,pady=5)

        # def handler(e,k,tag):
        #     self.txt.insert("insert", k, (tag,))
        #     return "break"
        for k, v in self.syntax_params.items():
            # if not k in "+-<>.,[]": continue
            if k=="default": continue
            # print(k,v)
            params = v["params"]
            # bind_name = v["bind_name"]
            tag_name = v["tag_name"]
            self.txt.tag_configure(tag_name, **params)
            # self.txt.bind(bind_name, lambda e,k=k,tag_name=tag_name: handler(e,k,tag_name), add='+')
        self.txt.tag_raise("syntax-highlight_bracket","syntax-[")
        self.txt.tag_raise("syntax-highlight_bracket","syntax-]")

        # self.txt.bind_all("<KeyPress>", lambda e: print(e.keycode), add='+')
        self.txt.bind_all("<KeyRelease>", lambda e: self.update_syntax_highlight(beg="insert -2c", end="insert"))
        self.txt.bind_all("<Button-1>", lambda e: self.update_syntax_highlight(beg="insert -2c", end="insert"))

        # ctrl_handler.curr_pos = "1.0"
        def paste_handler(e : tk.Event):
            try: # remove selection before pasting
                self.txt.delete("sel.first","sel.last")
            except:
                pass
            t = clipboard.paste()
            print(t)
            self.update_syntax_highlight(beg=f"insert -{len(t)}c", end="insert")
            return "break"
        def copy_handler(e : tk.Event):
            t = self.txt.selection_get()
            self.txt.update()
            print(t)
            clipboard.copy(t)
            return "break"
        def cut_handler(e: tk.Event):
            t = self.txt.get("sel.first","sel.last")
            self.txt.delete("sel.first","sel.last")
            clipboard.copy(t)
            # return "break"
        self.txt.bind_all("<<Paste>>", paste_handler)
        self.txt.bind_all("<<Cut>>", cut_handler)
        self.txt.bind_all("<<Copy>>", copy_handler)
        def select_all(e):
            self.txt.tag_add(tk.SEL, "1.0", tk.END)
            self.txt.mark_set("insert", "1.0")
            self.txt.see("insert")
            return 'break'
        self.txt.bind("<Control-Key-a>", select_all)
        self.txt.bind("<Control-Key-A>", select_all)

    def update_syntax_highlight(self, e=None, beg=-1, end=-1):
        if beg == -1: 
            beg = "1.0"
            line,column = 1,0
        else:
            tmp = self.txt.index(beg).split(".")
            line = int(tmp[0])
            column = int(tmp[1])
        if end == -1:
            end = tk.END

        # print(f"updating from {beg} to {end}, txt={self.txt.get(beg,end)}")
        txt = self.txt.get(beg, end)
        # print(txt)
        for k in self.syntax_params.keys():
            self.txt.tag_remove(f"syntax-{k}", beg,end)

        self.txt.tag_remove("syntax-highlight_bracket","1.0",tk.END)
        self.txt.tag_remove("syntax-highlight_error","1.0",tk.END)

        # if (self.txt.get("insert-1c") in "[]") or self.jump_table == {}:
        if True:
            self.jump_table = {}
            stack = []
            l,co = 1,0
            for i,c in enumerate(self.txt.get("1.0",tk.END)):
                if c == '[':
                    # print(f"[ at {l}.{co}")
                    stack.append(f"{l}.{co}")
                elif c == ']':
                    if stack:
                        corresp = stack.pop()
                        self.jump_table[f"{l}.{co}"] = corresp
                        self.jump_table[corresp] = f"{l}.{co}"
                    else:
                        self.txt.tag_add("syntax-highlight_error", f"{l}.{co}")

                if c == '\n':
                    l += 1
                    co = -1
                co += 1
        for i in stack:
            self.txt.tag_add("syntax-highlight_error", i)

        

        for c in txt:
            tk_idx = f"{line}.{column}"
            # print(f"{tk_idx} : {c}, {self.txt.get(tk_idx)}")
            if c in self.syntax_params.keys():
                # print(self.syntax_params[c])
                # params = self.syntax.params[c]["params"]
                # bind_name = self.syntax.params[c]["bind_name"]
                tag = self.syntax_params[c]["tag_name"]
                self.txt.tag_add(tag, tk_idx, tk_idx+"+1c")
                pass

            if c == '\n':
                line += 1
                column = -1
            column += 1

        # print(self.txt.tag_names())

        # print( f"<{self.txt.get('insert')}>")
        next_to_bracket = False
        curr = self.txt.index("insert") # to the right of the cursor
        curr2 = self.txt.index("insert -1c") # to the left of the cursor
        if curr in self.jump_table.keys():
            self.txt.tag_add("syntax-highlight_bracket", curr)
            self.txt.tag_add("syntax-highlight_bracket", self.jump_table[curr])
            next_to_bracket = True
        elif curr2 in self.jump_table.keys():
            self.txt.tag_add("syntax-highlight_bracket", curr2)
            self.txt.tag_add("syntax-highlight_bracket", self.jump_table[self.txt.index(curr2)])
            next_to_bracket = True
        # if the cursor is not next to a bracket, then we try to find the closest enclosing bracket to highlight
        if not next_to_bracket:
            l,co = map(int, curr.split("."))
            txt = self.txt.get("insert",tk.END)
            possib = self.jump_table.keys()
            depth=0
            for c in txt:
                # print(f"testing {l}.{co} : {c}")
                if c == "[": depth += 1
                if c == "]" and f"{l}.{co}" in possib:
                    if depth == 0: break
                    else: depth -= 1
                if c == '\n':
                    l += 1
                    co = -1
                co += 1
            curr = f"{l}.{co}"
            if curr in possib:
                self.txt.tag_add("syntax-highlight_bracket", curr)
                self.txt.tag_add("syntax-highlight_bracket", self.jump_table[curr])

        

if __name__ == '__main__':
    app = tk.Tk()
    app.title("BFCodeArea test")

    app.option_add("*Font", "TkFixedFont")

    app.tk.call("source","azure.tcl")
    app.tk.call("set_theme","dark")

    app.bind_all("<Escape>", lambda e: app.destroy())

    codeArea = BFCodeArea(app)

    codeArea.pack(padx=5, pady=5)

    codeArea.bind_all("u", lambda e: codeArea.update_syntax_highlight(beg="1.0", end="1.27"))


#     codeArea.txt.insert("1.0", """>,[ ------------------------------------------------ < remove 48 to get value
# >> +++++++++ [- add (0)*9 to (1)
#   <<[->+>>+<<<]>>>[-<<<+>>>]<
# ] <<
# > [-<+>] < add (1) to (0)
# > , read next digit
# ]<""")

    # a Hello World! program taken from http://www.bf.doleczek.pl/
    # codeArea.txt.insert("1.0", """
    # [ This program prints "Hello World!" and a newline to the screen, its
    # length is 106 active command characters [it is not the shortest.]

    # This loop is a "comment loop", it's a simple way of adding a comment
    # to a BF program such that you don't have to worry about any command
    # characters. Any ".", ",", "+", "-", "<" and ">" characters are simply
    # ignored, the "[" and "]" characters just have to be balanced.
    # ]
    # +++++ +++               Set Cell #0 to 8
    # [
    #     >++++               Add 4 to Cell #1; this will always set Cell #1 to 4
    #     [                   as the cell will be cleared by the loop
    #         >++             Add 2 to Cell #2
    #         >+++            Add 3 to Cell #3
    #         >+++            Add 3 to Cell #4
    #         >+              Add 1 to Cell #5
    #         <<<<-           Decrement the loop counter in Cell #1
    #     ]                   Loop till Cell #1 is zero; number of iterations is 4
    #     >+                  Add 1 to Cell #2
    #     >+                  Add 1 to Cell #3
    #     >-                  Subtract 1 from Cell #4
    #     >>+                 Add 1 to Cell #6
    #     [<]                 Move back to the first zero cell you find; this will
    #                         be Cell #1 which was cleared by the previous loop
    #     <-                  Decrement the loop Counter in Cell #0
    # ]                       Loop till Cell #0 is zero; number of iterations is 8

    # The result of this is:
    # Cell No :   0   1   2   3   4   5   6
    # Contents:   0   0  72 104  88  32   8
    # Pointer :   ^

    # >>.                     Cell #2 has value 72 which is 'H'
    # >---.                   Subtract 3 from Cell #3 to get 101 which is 'e'
    # +++++++..+++.           Likewise for 'llo' from Cell #3
    # >>.                     Cell #5 is 32 for the space
    # <-.                     Subtract 1 from Cell #4 for 87 to give a 'W'
    # <.                      Cell #3 was set to 'o' from the end of 'Hello'
    # +++.------.--------.    Cell #3 for 'rl' and 'd'
    # >>+.                    Add 1 to Cell #5 gives us an exclamation point
    # >++.                    And finally a newline from Cell #6
    # """)

    codeArea.update_syntax_highlight()

    app.mainloop()