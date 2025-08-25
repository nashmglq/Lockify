from flask import Flask
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "supersecret"  
db.init_app(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
