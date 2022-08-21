# flask-todo-crud
A CRUD To-Do application made with Python, Flask, SQLite, HTML, CSS

## How To Run
1. To install the dependencies:
```
$ (env) pip install -r requirements.txt
```

2. To start the web server:
```
$ (env) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
