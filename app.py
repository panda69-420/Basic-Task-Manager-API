from flask import Flask
from models import db
from routes import task_routes
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///tasks.db'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# register routes
app.register_blueprint(task_routes)

if __name__ == "__main__":
    app.run(debug=True)