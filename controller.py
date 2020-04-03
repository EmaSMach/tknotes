from views import NotaView
from tkinter import *
from models import Nota, session
from forms import NotaForm
# from db import Session
from pubsub import pub

# session = Session()

class Controller:
    
    def __init__(self, model=None, view=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.view = view()
        self.view.pack()
        self.update_table()
        pub.subscribe(self.update_table, 'nota_saved')
        pub.subscribe(self.update_table, 'nota_deleted')
        pub.subscribe(self.delete, 'delete_btn_clicked')
        pub.subscribe(self.update_table, 'update_btn_clicked')
        pub.subscribe(self.create_note, 'create_btn_clicked')

    def delete(self, _id):
        note = session.query(self.model).filter_by(id=_id).first()
        note.delete()

    def update_table(self):
        # fetching all the objects in the database
        values = session.query(self.model).all()
        # turning them into a list of tuples
        values = [note.to_tuple() for note in values]
        # updating the table with those values
        self.view.update_table(values=values)

    def create_note(self):
        data = {}
        form = NotaForm(var=data)
        del form
        if any(data.values()):
            new_form = Nota(title=data['title'], body=data['body'])
            new_form.save()


def main():
    root = Tk()
    view = NotaView
    controller = Controller(model=Nota, view=view)
    view.controller = controller
    # w = controller.view
    # w.pack()
    root.mainloop()
    # root.mainloop()

if __name__ == "__main__":
    main()