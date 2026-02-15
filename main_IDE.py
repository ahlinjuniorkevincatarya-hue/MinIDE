from tkinter import *
from tkinter import font,filedialog, messagebox,ttk
import os

#Editeur de texte 
root = Tk()
root.title("MinIDE")
root.geometry("500x400")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


def newTab():
    frame = Frame(notebook)
    my_font = font.Font(family="Arial", size=10, weight="normal")
    txt = Text(frame, font=my_font)
    txt.pack(fill="both", expand=True)
    notebook.add(frame,text=f"Tab {len(notebook.tabs())+1}")
    notebook.select(frame)
    txt.focus_set()

def savefile():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    fd = filedialog.asksaveasfilename(
        initialdir=os.getcwd(), 
        title="Save File", 
        filetypes=(("Text Files","*.txt"), ("All Files", "*.*")),
        defaultextension=".txt")
    if not fd:
        return 
    
    t = txt_widget.get("1.0",END)
    with open(fd,"w",encoding="utf-8") as f:
        f.write(t)

def openfile():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    fd = filedialog.askopenfilename(
        initialdir=os.getcwd(),
          title="Open File",
          filetypes=(("Text Files","*.txt"), ("All Files", "*.*"))
    )
    if not fd:
        return 
    with open(fd,"r",encoding="utf-8") as f:
        txt_widget.insert("1.0",f.read())    

def copytxt():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    try:
        t = txt_widget.get("sel.first","sel.last")
        root.clipboard_clear()
        root.clipboard_append(t)
    except TclError:
        messagebox.showinfo("Copy","No text selected to copy.")

def pastetxt():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    try:
        t =root.selection_get()
        txt_widget.insert('insert',t)
    except TclError:
        messagebox.showinfo("Paste","The clipboard is empty.")

    
    

menubar = Menu(root)
#file menu
fmenu = Menu(menubar,tearoff=0)
fmenu.add_command(label="New", command = newTab)
fmenu.add_command(label="Save",command= savefile)
fmenu.add_command(label="Open", command= openfile)
fmenu.add_separator()
fmenu.add_cascade(label="Exit",command=root.quit)
menubar.add_cascade(label="File",menu=fmenu)
#edit menu
emenu = Menu(menubar, tearoff=0)
emenu.add_command(label="Copy", command=copytxt)
emenu.add_command(label="Paste", command=pastetxt)
menubar.add_cascade(label="Edit",menu=emenu)

root.config(menu=menubar)


newTab()

root.mainloop()