"""
Entrypoint for pulpopaul
"""
from __future__ import unicode_literals

# pylint: disable=import-error
from flask import Flask, url_for, redirect
from pulpopaul.models import db
from pulpopaul.controllers.team import team_blueprint
from pulpopaul.controllers.match import match_blueprint
from pulpopaul.extensions import rest_api
from pulpopaul.controllers.rest import TeamApi, TournamentResource, MatchResource


def create_app(object_name):
    """
    Return a Flask application
    """

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
    rest_api.add_resource(
        MatchResource,
        '/api/match',
        '/api/match/<int:match_id>'
    )
    rest_api.init_app(app)

    # redirect to default view
    @app.route("/")
    def index():  # pylint: disable=unused-variable
        """
        Dummy index for now
        """
        return redirect(url_for('team.get_teams'))

    return app
