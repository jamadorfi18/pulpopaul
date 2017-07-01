from flask_sqlalchemy import SQLAlchemy, orm

db = SQLAlchemy()

class Model:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Tournament(db.Model, Model):
    """
    Tournament model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    short_name = db.Column(db.String())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())

    def __init__(self, name, start_date, end_date, short_name=None):
        self.name = name
        self.short_name = short_name
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return "<Tournament '{}'>".format(self.name)


class Match(db.Model, Model):

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

class Team(db.Model, Model):
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
