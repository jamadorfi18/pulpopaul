from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


# TODO no idea how to put them in different file
class Match(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    team_local_id = db.Column(db.Integer(), db.ForeignKey('team.id'), index=True)
    team_visitor_id = db.Column(db.Integer(), index=True)
    kickoff_at = db.Column(db.DateTime())
    score_local = db.Column(db.Integer())
    score_visitor = db.Column(db.Integer())

    def __init__(self, team_local, team_visitor):
        self.team_local_id = team_local.id
        self.team_visitor_id = team_visitor.id

    def __repr__(self):
        return "<Match {} vs {}>".format(self.team_local_id, self.team_visitor_id)

class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255))

    matches = db.relationship(
        'Match',
        backref='team',
        lazy='dynamic'
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Team {}>".format(self.name)

@app.route('/team/save/<name>')
def save_team(name):
    team = Team(name)
    db.session.add(team)
    db.session.commit()

    return 'saved'

@app.route("/match/save/<local>/<visitor>")
def save_match(local, visitor):
    local = Team.query.get(int(local))
    visitor = Team.query.get(int(visitor))

    app.logger.warning(local)
    app.logger.warning(visitor)

    m = Match(local, visitor)
    db.session.add(m)
    db.session.commit()

    return 'saved'

@app.route('/teams')
def get_teams():
    def teams_to_list(html, team):
        return html + '<li>{}</li>'.format(team.name)

    return '<ul>{}</ul>'.format(
        reduce(teams_to_list, Team.query.all(), '')
    )


@app.route("/matches")
def get_matches():
    def matches_to_list(html, match):
        return html + '<li><strong><a href="/team/{}">{}</a></strong> vs <strong>{}</strong></li>'.format(
            match.team_local_id,
            match.team.name, match.team_visitor_id)

    return '<ul>{}</ul>'.format(
        reduce(matches_to_list, Match.query.all(), '')
    )

@app.route('/team/<id>')
def team_detail(id):
    return '<h1>{}</h1>'.format(Match.query.get(id=id).name)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
