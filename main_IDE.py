from tkinter import *
from tkinter import font,filedialog, messagebox,ttk
import os

#Editeur de texte 
root = Tk()
root.title("MinIDE")
root.geometry("500x400")

style = ttk.Style()
style.theme_use('clam')  # thème moderne
style.configure("TNotebook.Tab",
                padding=[12, 8],
                font=('Arial', 11, 'bold'),
                background="#FFD700",   # doré
                foreground="#000000",
                relief="flat")   # texte noir pour contraste
style.map("TNotebook.Tab",
          background=[("selected", "#FFA500")],  # onglet actif : orange doré
          foreground=[("selected", "#000000")])
style.configure("TNotebook", background="#222222",borderwidth=0)  # fond du Notebook (gris foncé/noir)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True,padx=5,pady=5)
my_font = font.Font(family="Consolas", size=12)


def newTab():
    frame = Frame(notebook,bg="#1e1e1e")
    txt = Text(frame, font=my_font,bg="#1e1e1e",fg="#FFFFFF",insertbackground="#FFD700",wrap="word", undo=True,relief=FLAT, bd=0)
    txt.pack(fill="both", expand=True,padx=5,pady=5)
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

    
    

menubar = Menu(root, bg="#1e1e1e", fg="#FFFFFF", activebackground="#333333", activeforeground="#FFFFFF",relief=FLAT)
#file menu
fmenu = Menu(menubar, tearoff=0, bg="#1e1e1e", fg="#FFFFFF", activebackground="#333333", activeforeground="#FFFFFF")
fmenu.add_command(label="New", command = newTab)
fmenu.add_command(label="Save",command= savefile)
fmenu.add_command(label="Open", command= openfile)
fmenu.add_separator()
fmenu.add_cascade(label="Exit",command=root.quit)
menubar.add_cascade(label="File",menu=fmenu)
#edit menu
emenu = Menu(menubar, tearoff=0, bg="#1e1e1e", fg="#FFFFFF", activebackground="#333333", activeforeground="#FFFFFF")
emenu.add_command(label="Copy", command=copytxt)
emenu.add_command(label="Paste", command=pastetxt)
menubar.add_cascade(label="Edit",menu=emenu)

root.config(menu=menubar)


newTab()

root.mainloop()