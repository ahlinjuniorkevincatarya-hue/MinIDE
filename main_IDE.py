from tkinter import *
from tkinter import font,filedialog, messagebox,ttk
import os
import subprocess

#Editeur de texte 
root = Tk()
root.title("MinIDE")
root.geometry("500x400")

#creation du notebook pour permettre l'affichage des onglets
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

#Creation d'une console pour afficher la sortie du script
console_frame = Frame(root,height=150)
console_frame.pack(fill="x")
console_txt = Text(console_frame,height=8, bg="black", fg="white", state="disabled")
console_txt.pack(fill="both",expand=True)


def newTab():
    frame = Frame(notebook)  # cadre de l'onglet, fond par défaut

    # Text widget pour les numéros de ligne
    my_font = font.Font(family="Arial", size=10, weight="normal")
    line_numbers = Text(frame, width=4, padx=4, takefocus=0, border=0,
                        background="SystemButtonFace", foreground="black",
                        state="disabled", wrap="none", font=my_font)
    line_numbers.pack(side="left", fill="y")

    # Text widget principal
    txt = Text(frame, font=my_font, undo=True)  # tout par défaut
    txt.pack(side="right", fill="both", expand=True)

    # Scrollbar commune
    scrollbar = Scrollbar(frame, command=lambda *args: [txt.yview(*args), line_numbers.yview(*args)])
    txt.config(yscrollcommand=scrollbar.set)
    line_numbers.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Met à jour les numéros de lignes
    def update_line_numbers(event=None):
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        line_count = int(txt.index("end-1c").split(".")[0])
        for i in range(1, line_count+1):
            line_numbers.insert("end", f"{i}\n")
        line_numbers.config(state="disabled")

    # Bindings pour mettre à jour les numéros
    txt.bind("<KeyRelease>", lambda e: update_line_numbers())
    txt.bind("<MouseWheel>", update_line_numbers)
    txt.bind("<Button-4>", update_line_numbers)  # scroll Linux
    txt.bind("<Button-5>", update_line_numbers)  # scroll Linux

    # Ajouter onglet au Notebook
    notebook.add(frame, text=f"Tab {len(notebook.tabs())+1}")
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

def closeTab():
    current_tab = notebook.select()
    if current_tab:  # vérifie qu'il y a un onglet actif
        notebook.forget(current_tab)  # supprime l'onglet du Notebook

def saveAllTabs():
    for tab_id in notebook.tabs():  # parcourt tous les onglets
        txt_widget = notebook.nametowidget(tab_id).winfo_children()[0]
        # on peut demander le nom de fichier pour chaque onglet
        fd = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save File",
            filetypes=(("Text Files","*.txt"), ("All Files", "*.*")),
            defaultextension=".txt")
        if fd:  # si l'utilisateur n'annule pas
            t = txt_widget.get("1.0", END)
            with open(fd, "w", encoding="utf-8") as f:
                f.write(t)

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
        t =root.selection_get(selection="CLIPBOARD")
        txt_widget.insert('insert',t)
    except TclError:
        messagebox.showinfo("Paste","The clipboard is empty.")

def cuttxt():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    try:
        t = txt_widget.get("sel.first","sel.last")
        root.clipboard_clear()
        root.clipboard_append(t)
        txt_widget.delete("sel.first","sel.last")
    except TclError:
        messagebox.showinfo("Cut","No text selected to cut.")

def undotxt():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    try:
        txt_widget.edit_undo()
    except TclError:
        messagebox.showinfo("Undo","Nothing to undo.")

def redotxt():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    try:
        txt_widget.edit_redo()
    except TclError:
        messagebox.showinfo("Redo","Nothing to redo.")

def selectalltxt():

    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[0]
    txt_widget.tag_add("sel", "1.0", "end")

def runpy():
    current_tab = notebook.select()
    txt_widget = notebook.nametowidget(current_tab).winfo_children()[1]  # Text principal
    code = txt_widget.get("1.0","end-1c")  # "-1c" pour éviter la ligne vide finale

    # Écriture du script temporaire
    with open("script.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    try:
        # Exécution du script
        result = subprocess.run(
            ["python", "script.py"], 
            capture_output=True,
            text=True,
            check=False
        )

        console_txt.config(state="normal")
        console_txt.delete("1.0", "end")

        if result.stdout:
            console_txt.insert("end", "[STDOUT]\n" + result.stdout + "\n")
        if result.stderr:
            console_txt.insert("end", "[STDERR]\n" + result.stderr + "\n")

        console_txt.config(state="disabled")

    except FileNotFoundError:
        messagebox.showerror("Run Error", "Python n'est pas trouvé. Vérifie ton installation.")
    except Exception as e:
        messagebox.showerror("Run Error", str(e))

    

menubar = Menu(root)
#file menu
fmenu = Menu(menubar,tearoff=0)
fmenu.add_command(label="New", command = newTab)
fmenu.add_command(label="Save",command= savefile)
fmenu.add_command(label="Open", command= openfile)
fmenu.add_command(label="Close Tab", command=closeTab)
fmenu.add_command(label="Save All", command=saveAllTabs)

fmenu.add_separator()
fmenu.add_cascade(label="Exit",command=root.quit)
menubar.add_cascade(label="File",menu=fmenu)
#edit menu
emenu = Menu(menubar, tearoff=0)
emenu.add_command(label="Copy", command=copytxt)
emenu.add_command(label="Paste", command=pastetxt)
emenu.add_command(label="Cut", command=cuttxt)
emenu.add_command(label="Undo", command=undotxt)
emenu.add_command(label="Redo", command=redotxt)
emenu.add_command(label="Select All", command=selectalltxt)
#run menu
rmenu = Menu(menubar,tearoff = 0)
rmenu.add_command(label="Run", command=runpy)
menubar.add_cascade(label="Run",menu=rmenu)

menubar.add_cascade(label="Edit",menu=emenu)

root.config(menu=menubar)


newTab()

root.mainloop()
