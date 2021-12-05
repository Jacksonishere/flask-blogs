# this is now the file that just runs the app

# looks for init module in flaskblog and imports app
from flaskblog import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
