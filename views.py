from tkinter import Tk, Frame, YES, BOTH, END
from tkinter import ttk
from pubsub import pub
from forms import NotaForm


class NotaView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # configuring row and columns of the container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.pack(expand=YES, fill=BOTH)
        self.make_widgets()

    def make_widgets(self):
        self.make_table()
        self.make_buttons()

    def make_buttons(self):
        self.btn_frame = Frame(self)
        self.show_btn = ttk.Button(self.btn_frame, text='Actualizar lista', command=self.on_show_btn)
        self.create_btn = ttk.Button(self.btn_frame, text='Crear nota', command=self.on_create_note_btn)
        self.delete_btn = ttk.Button(self.btn_frame, text='Borrar', command=self.on_delete_btn)
        self.update_btn = ttk.Button(self.btn_frame, text='Modificar', command=self.on_update_btn)
        self.show_btn.grid(row=0, column=0)
        self.create_btn.grid(row=0, column=1)
        self.delete_btn.grid(row=0, column=2)
        self.update_btn.grid(row=0, column=3)
        self.btn_frame.grid(row=1, column=0)
        
    def on_update_btn(self):
        selected = self.table.selection()
        if selected and len(selected) == 1:
            selected_data = self.table.item(selected)['values']
            new_data = {'id': selected_data[0], 'title': selected_data[1], 'body': selected_data[2]}
            pub.sendMessage('update_btn_clicked', data=new_data)

    def on_delete_btn(self):
        selected = self.table.selection()
        if selected and len(selected) == 1:
            selected_id = self.table.item(selected[0])['values'][0]
            pub.sendMessage('delete_btn_clicked', _id=selected_id)

    def on_show_btn(self):
        pub.sendMessage('show_btn_clicked')

    def on_create_note_btn(self):
        pub.sendMessage('create_btn_clicked')

    def clear_table(self):
        children = self.table.get_children()
        if children:
            self.table.delete(*children)

    def update_table(self, values):
        self.clear_table()
        for value in values:
            self.table.insert('', END, values=value)

    def make_table(self):
        columns = ('id', 'title', 'body')
        self.table = ttk.Treeview(self, columns=columns)
        self.table.config(show='headings')
        self.table.column(columns[0], width=50)
        self.table.column(columns[1], width=150)
        self.table.heading(column=columns[0], text='Id')
        self.table.heading(column=columns[1], text='Título')
        self.table.heading(column=columns[2], text='Cuerpo')
        self.table.grid(row=0, column=0, sticky='nsew')
        
    def on_save_button(self):
        pass


def main():
    root = Tk()
    w = NotaView(root)
    w.pack()
    root.mainloop()

if __name__ == '__main__':
    main()