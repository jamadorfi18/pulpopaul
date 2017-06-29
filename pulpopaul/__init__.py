from __future__ import unicode_literals

from flask import Flask, url_for, redirect
from models import db
from controllers.team import team_blueprint
from controllers.match import match_blueprint
from config import DevConfig

# init app
app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

# register controller
app.register_blueprint(team_blueprint)
app.register_blueprint(match_blueprint)

# redirect to default view
@app.route("/")
def index():
    return redirect(url_for('team.get_teams'))

if __name__ == '__main__':
    app.run()
