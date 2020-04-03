from tkinter import *
from tkinter import ttk
from typing import Any


class NotaForm(Toplevel):
    """
    A form to display/save notes.
    param: var: Any  a variable to store the data in the form.
    """
    def __init__(self, var: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Agregar Nota")
        self.grab_set()
        if var is not None:
            self.data = var
        else:
            self.data = {}
        self.make_widgets()
        self.wait_window(self)

    def make_widgets(self):
        self.title_label = ttk.Label(self, text='Título:')
        self.title_entry = ttk.Entry(self)
        self.body_text = Text(self)
        self.save_btn = ttk.Button(self, text='Guardar', command=self.on_guardar)
        self.cancel_btn = ttk.Button(self, text='Cancelar', command=self.on_cancel)
        self.title_label.grid(row=0, column=0, sticky='ew')
        self.title_entry.grid(row=0, column=1, sticky='ew')
        self.body_text.grid(row=1, column=0, columnspan=2)
        self.save_btn.grid(row=2, column=0)
        self.cancel_btn.grid(row=2, column=1)

    def on_cancel(self):
        self.destroy()
        
    def on_guardar(self):
        self.data['title'] = self.title_entry.get().strip()
        self.data['body'] = self.body_text.get(0.0, END).strip()
        self.destroy()

def create_note(val):
    note = NotaForm(var=val)
    val = note.data
    if any(val.values()):
        return val
    else:
        return None

def main():
    root = Tk()
    vale = {}
    if create_note(None):
        print('data')
    btn = Button(root, text='abrir', command=lambda: create_note(vale))
    btn.pack()
    root.mainloop()
    print(vale)

if __name__ == '__main__':
    main()