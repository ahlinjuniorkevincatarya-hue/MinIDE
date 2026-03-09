import os
import subprocess
from tkinter import filedialog, messagebox, TclError, END

class MenuFunctions:
    def __init__(self, root, notebook, console_txt):
        self.root = root
        self.notebook = notebook
        self.console_txt = console_txt

    def get_txt_widget(self):
        current_tab = self.notebook.select()
        frame = self.notebook.nametowidget(current_tab)
        return frame.txt_widget

    def savefile(self):
        txt_widget = self.get_txt_widget()
        fd = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save File",
            filetypes=(("Text Files","*.txt"), ("All Files", "*.*")),
            defaultextension=".txt")
        if not fd:
            return
        with open(fd, "w", encoding="utf-8") as f:
            f.write(txt_widget.get("1.0", END))

    def openfile(self):
        txt_widget = self.get_txt_widget()
        fd = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open File",
            filetypes=(("Text Files","*.txt"), ("All Files", "*.*")))
        if not fd:
            return
        with open(fd, "r", encoding="utf-8") as f:
            txt_widget.insert("1.0", f.read())

    def closeTab(self):
        current_tab = self.notebook.select()
        if current_tab:
            self.notebook.forget(current_tab)

    def saveAllTabs(self):
        for tab_id in self.notebook.tabs():
            frame = self.notebook.nametowidget(tab_id)
            txt_widget = frame.txt_widget
            fd = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save File",
                filetypes=(("Text Files","*.txt"), ("All Files", "*.*")),
                defaultextension=".txt")
            if fd:
                with open(fd, "w", encoding="utf-8") as f:
                    f.write(txt_widget.get("1.0", END))

    def copytxt(self):
        txt_widget = self.get_txt_widget()
        try:
            t = txt_widget.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(t)
        except TclError:
            messagebox.showinfo("Copy", "No text selected to copy.")

    def pastetxt(self):
        txt_widget = self.get_txt_widget()
        try:
            t = self.root.selection_get(selection="CLIPBOARD")
            txt_widget.insert('insert', t)
        except TclError:
            messagebox.showinfo("Paste", "The clipboard is empty.")

    def cuttxt(self):
        txt_widget = self.get_txt_widget()
        try:
            t = txt_widget.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(t)
            txt_widget.delete("sel.first", "sel.last")
        except TclError:
            messagebox.showinfo("Cut", "No text selected to cut.")

    def undotxt(self):
        try:
            self.get_txt_widget().edit_undo()
        except TclError:
            messagebox.showinfo("Undo", "Nothing to undo.")

    def redotxt(self):
        try:
            self.get_txt_widget().edit_redo()
        except TclError:
            messagebox.showinfo("Redo", "Nothing to redo.")

    def selectalltxt(self):
        self.get_txt_widget().tag_add("sel", "1.0", "end")

    def runpy(self):
        txt_widget = self.get_txt_widget()
        code = txt_widget.get("1.0", "end-1c")
        with open("script.py", "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run(["python", "script.py"],
                capture_output=True, text=True, check=False)
            self.console_txt.config(state="normal")
            self.console_txt.delete("1.0", "end")
            if result.stdout:
                self.console_txt.insert("end", "OUT >>>\n" + result.stdout + "\n")
            if result.stderr:
                self.console_txt.insert("end", "ERROR >>>\n" + result.stderr + "\n")
            self.console_txt.config(state="disabled")
        except FileNotFoundError:
            messagebox.showerror("Run Error", "Python n'est pas trouvé.")
        except Exception as e:
            messagebox.showerror("Run Error", str(e))