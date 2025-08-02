from flask import Flask
from Routes.routes_api import task_api
app = Flask(__name__)
app.register_blueprint(task_api)

if __name__ == '__main__':
    app.run(debug=True)

