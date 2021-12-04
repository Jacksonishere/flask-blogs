# looks for init module in flaskblog and imports app
from flaskblog import app
# this is now the file that just runs the app

if __name__ == '__main__':
    app.run(debug=True)
