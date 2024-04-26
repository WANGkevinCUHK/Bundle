from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_migrate import Migrate
from config import Config
from exts import db
from models.user import User
from bp.user_BP import user_bp
from bp.event_BP import event_bp

# from models.event import Event
# from models.friendship import Friendship
#, event_controller, friendship_controller
# from flask_login import LoginManager
# from forms import user_form, event_form, friendship_form


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)


if __name__ == '__main__':
    app.run(debug=True)