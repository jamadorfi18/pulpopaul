from flask import Blueprint
# TODO abstract team inside match where is convenient
from pulpopaul.models import Match, Team

match_blueprint = Blueprint('match', __name__)

@match_blueprint.route("/match/save/<local>/<visitor>")
def save_match(local, visitor):
    local = Team.query.get(int(local))
    visitor = Team.query.get(int(visitor))

    m = Match(local, visitor)
    m.save()

    return 'saved'

@match_blueprint.route("/matches")
def get_matches():
    def matches_to_list(html, match):
        return html + '<li><strong><a href="/team/{}">{}</a></strong> vs <strong><a href="/team/{}">{}</a></strong></li>'.format(
            match.team_local.id, match.team_local.name,
            match.team_visitor.id, match.team_visitor.name)

    return '<ul>{}</ul>'.format(
        reduce(matches_to_list, Match.query.all(), '')
    )
