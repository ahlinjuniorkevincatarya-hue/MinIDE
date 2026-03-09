from tkinter import *
from tkinter import font,ttk
from syntax_highlight import color_syntax
from menu_function import MenuFunctions

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

mf = MenuFunctions(root, notebook, console_txt)

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
    frame.txt_widget = txt
    txt.tag_configure("keyword", foreground="blue")
    txt.tag_configure("string", foreground="green")
    txt.tag_configure("comment", foreground="gray")
    txt.tag_configure("number", foreground="orange")
    txt.tag_configure("punctuation", foreground="red")

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

    def auto_indent(event):
        current_line = txt.get("insert linestart", "insert")
        # compter les espaces/tabs au début de la ligne
        indent = ""
        for char in current_line:
            if char in (" ", "\t"):
                indent += char
            else:
                break
        # augmenter l'indentation si la ligne finit par ":"
        if current_line.rstrip().endswith(":"):
            indent += "    "
        # insérer nouvelle ligne + indentation
        txt.insert("insert", "\n" + indent)
        return "break" 
        

    # Bindings pour mettre à jour les numéros
    txt.bind("<KeyRelease>", lambda e: (update_line_numbers(), color_syntax(txt)))
    txt.bind("<MouseWheel>", update_line_numbers)
    txt.bind("<Button-4>", update_line_numbers)  # scroll Linux
    txt.bind("<Button-5>", update_line_numbers)  # scroll Linux
    txt.bind("<Return>", auto_indent)
    
    # Ajouter onglet au Notebook
    notebook.add(frame, text=f"Tab {len(notebook.tabs())+1}")
    notebook.select(frame)
    txt.focus_set()
    

menubar = Menu(root)
#file menu
fmenu = Menu(menubar,tearoff=0)
fmenu.add_command(label="New", command = newTab)
fmenu.add_command(label="Save",command= mf.savefile)
fmenu.add_command(label="Open", command= mf.openfile)
fmenu.add_command(label="Close Tab", command=mf.closeTab)
fmenu.add_command(label="Save All", command=mf.saveAllTabs)

fmenu.add_separator()
fmenu.add_cascade(label="Exit",command=root.quit)
menubar.add_cascade(label="File",menu=fmenu)
#edit menu
emenu = Menu(menubar, tearoff=0)
emenu.add_command(label="Copy", command=mf.copytxt)
emenu.add_command(label="Paste", command=mf.pastetxt)
emenu.add_command(label="Cut", command=mf.cuttxt)
emenu.add_command(label="Undo", command=mf.undotxt)
emenu.add_command(label="Redo", command=mf.redotxt)
emenu.add_command(label="Select All", command=mf.selectalltxt)
#run menu
rmenu = Menu(menubar,tearoff = 0)
rmenu.add_command(label="Run", command=mf.runpy)
menubar.add_cascade(label="Run",menu=rmenu)

menubar.add_cascade(label="Edit",menu=emenu)

root.config(menu=menubar)


newTab()

root.mainloop()
