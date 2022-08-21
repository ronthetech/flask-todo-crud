from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# telling our app where our db is located, can use mysql, postgresql
# 4/s is an absolute path; 3/s is a relative path: so we dont have to specify location, it can just reside in the project location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize db and pass in the settings from our app
db = SQLAlchemy(app)


class ToDo(db.Model):  # database model
    # int that references id of each entry, primary key
    id = db.Column(db.Integer, primary_key=True)

    # text that holds each To-Do, you dont want user to be able to make empty To-Dos
    content = db.Column(db.String(200), nullable=False)

    # completed = db.Column(db.Integer, default=0) maybe use as a boolean?

    # when the To-Do was created, automatic
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # creates string every time you create a new element
    def __repr__(self):

        # return the To-Do and the id of the To-Do
        return '<To-Do %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        todo_content = request.form['content']

        # create a to do object that will have its contents = to the input on 'index.html'
        new_todo = ToDo(content=todo_content)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:  # error message
            return 'There was an issue adding your todo item'

    else:  # look at the db contents in the order that they were created, and return all of them
        todos = ToDo.query.order_by(ToDo.date_created).all()
        # firstTodo = ToDo.query.order_by(ToDo.date_created).first()
        return render_template('index.html', todos=todos)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:  # error message
        return 'There was a problem deleting your todo item'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        todo.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:  # error message
            return 'There was a problem updating your todo item'

    else:
        return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)
