#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import tkinter as tk
import pyscreenshot as ImageGrab
from PIL import ImageTk
import time
import webbrowser
from datetime import datetime


class Sentinel(object):
    count = 0

    def __init__(self, root):
        Sentinel.count += 1
        self.root = root

    def __del__(self):
        Sentinel.count -= 1
        if Sentinel.count == 0:
            self.root.destroy()


class InitialWin(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.sentinel = Sentinel(master)
        self.master = master
        self.wm_attributes('-type', 'splash')
        self.wm_attributes('-topmost', 1)
        self._offsetx = 0
        self._offsety = 0
        self.configure(bg="#212121")
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)

        self.button1 = tk.Button(self, text='   Quit   ',
                                 command=self.ondelete,
                                 activebackground='#B71C1C',
                                 activeforeground='#FFFFFF',
                                 background='#F44336',
                                 foreground='#FFFFFF')
        self.button1_ttp = CreateToolTip(
            self.button1, text='Close this Window')
        self.button2 = tk.Button(self, text='   Snip   ',
                                 command=self.capture,
                                 activebackground='#1A237E',
                                 activeforeground='#FFFFFF',
                                 background='#3F51B5',
                                 foreground='#FFFFFF',)
        self.button2_ttp = CreateToolTip(self.button2, text='Snip')

        self.show_help = tk.Label(self, text=" \u030C Show Help \u030C ",
                                  background="#212121", foreground='#FFFFFF')
        self.hide_help = tk.Label(self, text=" \u0302 Hide Help \u0302 ",
                                  background="#212121", foreground='#FFFFFF')

        self.button2.grid(row=0, pady=(10, 2), padx=10)
        self.button1.grid(row=0, pady=(10, 2), column=1, padx=10)
        self.show_help.grid(row=1, columnspan=2, pady=7, padx=10, ipady=3)

        self.show_help.bind('<ButtonRelease-1>', self.toggle_help)
        self.show_help.bind('<Enter>', self.help_enter)
        self.show_help.bind('<Leave>', self.help_leave)
        self.hide_help.bind('<ButtonRelease-1>', self.toggle_help)
        self.hide_help.bind('<Enter>', self.help_enter)
        self.hide_help.bind('<Leave>', self.help_leave)

        helptext = """
Use Left Mouse Buttton and Drag to move the snip around.
Use Middle Mouse Button to close the snip.
Use Right Mouse Button to toggle Send to Back/Stay on Top.

For a seamless experience, assign your desired keyboard
shortcut to the command MinimalSnip --no-gui
to directly capture snips.

Issues and Feature Requests can be posted at"""

        self.helptext = tk.Label(self, text=helptext,
                                 background="#303030", foreground='#FFFFFF')
        self.hyperlink = tk.Label(self, text='GitHub',
                                  background="#303030", foreground='#009688')
        self.devname = tk.Label(self, text='\n<> with ♥ by Kushal Chauhan\n',
                                background="#303030", foreground='#FFFFFF')

        link = 'https://github.com/kushalchauhan98/minimal-snip'
        self.hyperlink.bind('<ButtonRelease-1>',
                            lambda event: webbrowser.open(link))
        self.hyperlink.bind('<Enter>', self.help_enter)
        self.hyperlink.bind('<Leave>', self.help_leave)
        self.hyperlink.bind('<B1-Motion>', self.dragwin)
        self.hyper_ttp = CreateToolTip(self.hyperlink,
                                       text=link)
        self.help_shown = False

    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def capture(self, event=None):
        self.withdraw()
        snap = CaptureWin(self.master, self)

    def toggle_help(self, event):
        if not self.help_shown:
            self.show_help.grid_forget()
            self.helptext.grid(row=1, columnspan=2, padx=10, pady=(10, 0),
                               ipadx=5, ipady=0)
            self.hyperlink.grid(row=2, columnspan=2, padx=10,
                                ipadx=5, ipady=0, sticky=('w', 'e'))
            self.devname.grid(row=3, columnspan=2, padx=10,
                              ipadx=5, ipady=0, sticky=('w', 'e'))
            self.hide_help.grid(row=4, columnspan=2, pady=7, padx=10, ipady=3)
            self.help_shown = True
        else:
            self.helptext.grid_forget()
            self.hyperlink.grid_forget()
            self.devname.grid_forget()
            self.hide_help.grid_forget()
            self.show_help.grid(row=1, columnspan=2, pady=7, padx=10, ipady=3)
            self.help_shown = False

    def help_enter(self, event):
        event.widget.config(background='#303030', cursor='hand2')

    def help_leave(self, event):
        event.widget.config(background='#212121', cursor='')

    def ondelete(self):
        self.destroy()
        del self.sentinel


class CaptureWin(tk.Toplevel):

    def __init__(self, master, win=False):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.win = win
        self.x = self.y = 0
        self.wait_visibility(self)
        self.wm_attributes('-alpha', 0.2)
        self.canvas = tk.Canvas(self, cursor="cross", bg='white')
        self.attributes("-fullscreen", True)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_button_press(self, event):

        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1,
                                                 fill="black")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        x1 = min(self.start_x, self.curX)
        x2 = max(self.start_x, self.curX)
        y1 = min(self.start_y, self.curY)
        y2 = max(self.start_y, self.curY)
        self.destroy()
        time.sleep(0.5)
        im = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        if self.win:
            self.win.deiconify()
        snapshot = ShowWin(self.master, im, x2 - x1, y2 - y1)


class ShowWin(tk.Toplevel):

    def __init__(self, master, image, x, y):
        global pix
        tk.Toplevel.__init__(self, master)
        self.sentinel = Sentinel(master)
        self.x = x
        self.y = y
        self._offsetx = 0
        self._offsety = 0
        self.wm_attributes('-type', 'splash')
        self.topmost = True
        self.top = 0
        self.wm_attributes('-topmost', 1)
        self.canvas = tk.Canvas(self, width=x - 1, height=y - 1)
        self.canvas.pack()
        self.image = image
        self.snip = ImageTk.PhotoImage(image)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw",
                                                     image=self.snip)
        self.canvas.bind("<Enter>", self.enter)
        self.canvas.bind("<Leave>", self.leave)
        self.canvas.bind('<Button-1>', self.clickwin)
        self.canvas.bind('<Button-2>', self.ondelete)
        self.canvas.bind('<Button-3>', self.push_back)
        self.canvas.bind('<B1-Motion>', self.dragwin)
        self.bgborder = tk.Label(self)
        self.bglabel = tk.Label(self, background='#212121')
        self.xlabel = tk.Label(self, image=ShowWin.close_icon)
        self.xbutton_ttp = CreateToolTip(self.xlabel, text="Close Snip",
                                         enterfunc=self.enterx,
                                         leavefunc=self.leavex)
        self.olabel = tk.Label(self, image=ShowWin.hide_icon)
        self.tooltip = "Send to Back"
        self.obutton_ttp = CreateToolTip(self.olabel,
                                         textfunc=self.get_tooltip,
                                         enterfunc=self.entero,
                                         leavefunc=self.leaveo)
        self.slabel = tk.Label(self, image=ShowWin.save_icon)
        self.sbutton_ttp = CreateToolTip(self.slabel, text="Save Snip",
                                         enterfunc=self.enters,
                                         leavefunc=self.leaves)

        self.savelabel = tk.Label(self, text=' Save As', background='#212121',
                                  foreground='#FFFFFF', anchor='w')
        self.path = tk.StringVar()
        self.path.trace("w", self.validate)
        self.entry = tk.Entry(self, textvariable=self.path, bg='#303030',
                              fg='#FFFFFF', highlightbackground='#212121',
                              highlightcolor='#212121',
                              insertbackground='#FFFFFF')
        self.saveas = tk.Button(self, text='Save',
                                command=self.savenow,
                                activebackground='#1A237E',
                                activeforeground='#FFFFFF',
                                background='#3F51B5',
                                foreground='#FFFFFF',)
        self.dt = datetime.now().strftime("%Y-%M-%d-%H-%M-%S")
        self.savetooltip = 'Save Snip'
        self.save_ttp = CreateToolTip(
            self.saveas, textfunc=self.get_save_tooltip)

        self.bor = self.canvas.create_window(x, 1, anchor='ne',
                                             window=self.bgborder,
                                             height=28, width=73)
        self.bg = self.canvas.create_window(x, 1, anchor='ne',
                                            window=self.bglabel,
                                            height=27, width=72)
        self.xbutton = self.canvas.create_window(x - 5, 6, anchor='ne',
                                                 window=self.xlabel)
        self.obutton = self.canvas.create_window(x - 27, 6, anchor='ne',
                                                 window=self.olabel)
        self.sbutton = self.canvas.create_window(x - 49, 6, anchor='ne',
                                                 window=self.slabel)
        self.savewid = self.canvas.create_window(x, 1, anchor='ne',
                                                 window=self.savelabel,
                                                 height=28,
                                                 width=self.x - 1)
        self.pathtext = self.canvas.create_window(58, 5, anchor='nw',
                                                  window=self.entry,
                                                  height=20,
                                                  width=x - 108)
        self.savebutton = self.canvas.create_window(x - 45, 5, anchor='nw',
                                                    window=self.saveas,
                                                    height=20,
                                                    width=40)

        self.xlabel.bind('<Button-1>', self.ondelete)
        self.olabel.bind('<Button-1>', self.push_back)
        self.slabel.bind('<Button-1>', self.save_snip)

        self.canvas.itemconfigure(self.bor, state='hidden')
        self.canvas.itemconfigure(self.bg, state='hidden')
        self.canvas.itemconfigure(self.xbutton, state='hidden')
        self.canvas.itemconfigure(self.obutton, state='hidden')
        self.canvas.itemconfigure(self.sbutton, state='hidden')
        self.canvas.itemconfigure(self.savewid, state='hidden')
        self.canvas.itemconfigure(self.pathtext, state='hidden')
        self.canvas.itemconfigure(self.savebutton, state='hidden')

    def leave(self, event):
        if (event.y > self.top + 28 or event.x < self.x - 73) or\
           (event.y < 4 or event.x > self.x - 4) :
            self.canvas.itemconfigure(self.xbutton, state='hidden')
            self.canvas.itemconfigure(self.obutton, state='hidden')
            self.canvas.itemconfigure(self.sbutton, state='hidden')
            self.canvas.itemconfigure(self.bg, state='hidden')
            self.canvas.itemconfigure(self.bor, state='hidden')

    def enter(self, event):
        self.canvas.itemconfigure(self.xbutton, state='normal')
        self.canvas.itemconfigure(self.obutton, state='normal')
        self.canvas.itemconfigure(self.sbutton, state='normal')
        self.canvas.itemconfigure(self.bg, state='normal')
        self.canvas.itemconfigure(self.bor, state='normal')

    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def push_back(self, event=None):
        if self.topmost:
            self.wm_attributes('-topmost', False)
            self.topmost = False
            self.tooltip = "Stay on Top"
            self.lower()
        else:
            self.wm_attributes('-topmost', True)
            self.topmost = True
            self.tooltip = "Send to Back"

    def get_tooltip(self):
        return self.tooltip

    def enterx(self):
        self.xlabel.configure(image=ShowWin.close_hover)

    def entero(self):
        if self.topmost:
            self.olabel.configure(image=ShowWin.hide_hover)
        else:
            self.olabel.configure(image=ShowWin.show_hover)

    def enters(self):
        self.slabel.configure(image=ShowWin.save_hover)

    def leavex(self):
        self.xlabel.configure(image=ShowWin.close_icon)

    def leaveo(self):
        if self.topmost:
            self.olabel.configure(image=ShowWin.hide_icon)
        else:
            self.olabel.configure(image=ShowWin.show_icon)

    def leaves(self):
        self.slabel.configure(image=ShowWin.save_icon)

    def save_snip(self, event):
        if self.top == 0:
            self.top = 30
            offset = self.top
            self.canvas.itemconfigure(self.savewid, state='normal')
            self.canvas.itemconfigure(self.pathtext, state='normal')
            self.canvas.itemconfigure(self.savebutton, state='normal')
            self.path.set('/home/kushalchauhan98/Pictures/Snip-' + self.dt)
        else:
            offset = -self.top
            self.top = 0
            self.path.set('')
            self.canvas.itemconfigure(self.savewid, state='hidden')
            self.canvas.itemconfigure(self.pathtext, state='hidden')
            self.canvas.itemconfigure(self.savebutton, state='hidden')
        self.canvas.config(height=self.y - 1 + offset)
        self.canvas.move(self.canvas_image, 0, offset)
        self.canvas.move(self.bor, 0, offset)
        self.canvas.move(self.bg, 0, offset)
        self.canvas.move(self.sbutton, 0, offset)
        self.canvas.move(self.obutton, 0, offset)
        self.canvas.move(self.xbutton, 0, offset)

    def savenow(self):
        self.image.save(self.path.get() + '.png')
        self.save_snip(None)

    def get_save_tooltip(self):
        return self.savetooltip

    def validate(self, dummy1, dummy2, dummy3):
        p = '/'.join(self.path.get().split('/')[:-1])
        if os.path.exists(p):
            self.saveas.config(state='normal')
            self.savetooltip = 'Save Snip'
        else:
            self.saveas.config(state='disabled')
            self.savetooltip = 'Enter valid path first'

    def ondelete(self, event=None):
        self.destroy()
        del self.sentinel


class CreateToolTip(object):

    def __init__(self, widget, text='Widget Info', textfunc=None,
                 enterfunc=None, leavefunc=None):
        self.waittime = 500
        self.wraplength = 500
        self.widget = widget
        self.text = text
        self.textfunc = textfunc
        self.enterfunc = enterfunc
        self.leavefunc = leavefunc
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        if self.enterfunc != None:
            self.enterfunc()
        self.widget.configure(cursor='hand2')
        self.schedule()

    def leave(self, event=None):
        if self.leavefunc != None:
            self.leavefunc()
        self.widget.configure(cursor='')
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        if self.textfunc != None:
            self.text = self.textfunc()
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


root = tk.Tk()
root.withdraw()

ShowWin.close_icon = tk.PhotoImage(file="icons/close.ppm")
ShowWin.show_icon = tk.PhotoImage(file="icons/show.ppm")
ShowWin.hide_icon = tk.PhotoImage(file="icons/hide.ppm")
ShowWin.save_icon = tk.PhotoImage(file="icons/save.ppm")
ShowWin.close_hover = tk.PhotoImage(file="icons/close-hover.ppm")
ShowWin.show_hover = tk.PhotoImage(file="icons/show-hover.ppm")
ShowWin.hide_hover = tk.PhotoImage(file="icons/hide-hover.ppm")
ShowWin.save_hover = tk.PhotoImage(file="icons/save-hover.ppm")

if len(sys.argv) == 2:
    if sys.argv[1] == "--no-gui":
        win = CaptureWin(root)
        root.mainloop()
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        helptext = """
Use Left Mouse Buttton and Drag to move the snip around.
Use Middle Mouse Button to close the snip.
Use Right Mouse Button to toggle Send to Back/Stay on Top.

For a seamless experience, assign your desired keyboard shortcut to the \
command MinimalSnip --no-gui to directly capture snips.

Issues and Feature Requests can be posted at GitHub

<> with ♥ by Kushal Chauhan
"""
        print(helptext)
    else:
        print('Use MinimalSnip -h or MinimalSnip --help to display help.')
else:
    win = InitialWin(root)
    root.mainloop()
