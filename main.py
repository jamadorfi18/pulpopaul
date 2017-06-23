from flask import Flask
from flask_sqlalchemy import SQLAlchemy, orm
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

        self.init_on_query()

    # http://docs.sqlalchemy.org/en/latest/orm/constructors.html
    @orm.reconstructor
    def init_on_query(self):
        self._team_local = Team.query.get(self.team_local_id)
        self._team_visitor = Team.query.get(self.team_visitor_id)

    @property
    def team_local(self):
        return self._team_local

    @team_local.setter
    def set_team_local(self, value):
        self._team_local = value

    @property
    def team_visitor(self):
        return self._team_visitor

    @team_visitor.setter
    def set_team_visitor(self, value):
        self._team_visitor = value

    def __repr__(self):
        return "<Match {} vs {}>".format(self.team_local.name, self.team_visitor.name)

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
        return html + '<li><strong><a href="/team/{}">{}</a></strong> vs <strong><a href="/team/{}">{}</a></strong></li>'.format(
            match.team_local.id, match.team_local.name,
            match.team_visitor.id, match.team_visitor.name)

    return '<ul>{}</ul>'.format(
        reduce(matches_to_list, Match.query.all(), '')
    )

@app.route('/team/<id>')
def team_detail(id):
    return '<h1>{}</h1>'.format(Team.query.get(id).name)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
