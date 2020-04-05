from tkinter import Button, END, Frame, Tk, Toplevel, Text
from tkinter import ttk
# from typing import Any


class NotaForm(Toplevel):
    """
    A form to display/save notes.
    param: var: Any             a variable to store the data in the form.
    param: initial_data: dict   a dictinary with the data to fill the form.
    """
    def __init__(self, var=None, initial_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Agregar Nota")
        self.geometry("350x450")
        self.resizable(False, False)
        self.grab_set()
        if var is not None:
            self.data = var
        else:
            self.data = {}
        self.make_widgets()
        if initial_data is not None:
            self.title("Modificar Nota")
            self.data['id'] = initial_data['id']
            self.load_data(initial_data)
        self.wait_window(self)


    def make_widgets(self):
        self.top_container = Frame(self)
        self.title_label = ttk.Label(self.top_container, text='Título:')
        self.title_entry = ttk.Entry(self.top_container)
        self.body_text = Text(self)
        self.save_btn = ttk.Button(self, text='Guardar', command=self.on_guardar)
        self.cancel_btn = ttk.Button(self, text='Cancelar', command=self.on_cancel)

        self.top_container.grid(row=0, column=0, sticky='ew', columnspan=2)
        self.top_container.columnconfigure(1, weight=1)
        self.title_label.grid(row=0, column=0, sticky='w')
        self.title_entry.grid(row=0, column=1, sticky='ew')
        self.body_text.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.save_btn.grid(row=2, column=0)
        self.cancel_btn.grid(row=2, column=1)

        # configuring columns and rows
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1), weight=1)

    def load_data(self, data):
        self.title_entry.insert(0, data['title'])
        self.body_text.insert(0.0, data['body'])

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
    btn = Button(root, text='abrir', command=lambda: create_note(vale))
    btn.pack()
    root.mainloop()

if __name__ == '__main__':
    main()