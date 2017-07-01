from __future__ import unicode_literals

from flask import Flask, url_for, redirect
from models import db
from controllers.team import team_blueprint
from controllers.match import match_blueprint
from config import DevConfig
from .extensions import (
    rest_api
)
from .controllers.rest import TeamApi, TournamentResource


def create_app(object_name):
    # init app
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)

    # register controllers
    app.register_blueprint(team_blueprint)
    app.register_blueprint(match_blueprint)

    # register REST controllers
    rest_api.add_resource(
        TeamApi,
        '/api/team',
        '/api/team/<int:team_id>',
    )
    rest_api.add_resource(
        TournamentResource,
        '/api/tournament',
        '/api/tournament/<int:tournament_id>'
    )
    rest_api.init_app(app)

    # redirect to default view
    @app.route("/")
    def index():
        return redirect(url_for('team.get_teams'))

    return app
