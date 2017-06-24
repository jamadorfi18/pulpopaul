from flask import render_template, Blueprint
# TODO do not use db
from pulpopaul.models import Team, db

team_blueprint = Blueprint('team', __name__)

@team_blueprint.route('/teams', defaults={'page': 1})
@team_blueprint.route('/teams/', defaults={'page': 1})
@team_blueprint.route('/teams/<page>')
def get_teams(page=1):
    pagination = Team.query.order_by(Team.name.asc()).paginate(int(page), 10)

    return render_template(
        'teams.html',
        teams=pagination.items,
        pagination=pagination
    )

@team_blueprint.route('/team/<id>')
def team(id):
    return '<h1>{}</h1>'.format(Team.query.get(id).name)

@team_blueprint.route('/team/delete/<id>')
def delete_team(id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()
    return 'deleted'

@team_blueprint.route('/team/save/<name>')
def save_team(name):
    team = Team(name)
    team.save()
    return 'saved'
