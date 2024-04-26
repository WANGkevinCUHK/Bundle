from flask import Flask
from config import Config
from controllers.user_controller import user_bp
from controllers.event_controller import event_bp
from controllers.friendship_controller import friendship_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(user_bp)
app.register_blueprint(event_bp)
app.register_blueprint(friendship_bp)

if __name__ == '__main__':
    app.run()