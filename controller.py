from views import NotaView
from tkinter import Tk
from models import Nota, session
from forms import NotaForm
from pubsub import pub


class Controller:
    def __init__(self, model=None, view=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.view = view()
        self.view.pack()
        self.update_table()
        # subscribing to messages
        pub.subscribe(self.update_table, 'nota_saved')
        pub.subscribe(self.update_table, 'nota_deleted')
        pub.subscribe(self.delete, 'delete_btn_clicked')
        pub.subscribe(self.update_table, 'show_btn_clicked')
        pub.subscribe(self.create_note, 'create_btn_clicked')
        pub.subscribe(self.update_note, 'update_btn_clicked')

    def update_note(self, data):
        # loding initial data
        form = NotaForm(initial_data=data)
        data = form.data
        del form  # deleting the object, we no longer need it.
        if any(data.values()):
            note = session.query(self.model).filter_by(id=data['id']).first()
            # if data has title and body fields
            if data.get('title'):
                note.title = data['title']
                note.body = data['body']
                note.save()

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
        form = NotaForm()
        data = form.data
        del form
        if any(data.values()):
            new_note = Nota(title=data['title'], body=data['body'])
            new_note.save()


def main():
    root = Tk()
    view = NotaView
    controller = Controller(model=Nota, view=view)
    root.mainloop()

if __name__ == "__main__":
    main()