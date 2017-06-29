"""
API controller for Team
"""
from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse
from pulpopaul.models import Team


# Arg parsers
team_get_parser = reqparse.RequestParser()
team_get_parser.add_argument(
    'page',
    type=int,  # protip: this can be any function
    location=['args', 'headers'],
    required=False,
    default=1
)

team_post_parser = reqparse.RequestParser()
team_post_parser.add_argument(
    'name',
    type=str,
    required=True,
    help='Name is required'
)


team_fields = {
    'name': fields.String()
}

class TeamApi(Resource):
    """
    API controller for Team
    """

    @marshal_with(team_fields)
    def get(self, team_id=None):
        """
        Get all teams
        """
        if team_id:
            team = Team.query.get(team_id)
            if not team:
                abort(404)
            return team
        else:
            args = team_get_parser.parse_args()
            teams = Team.query.order_by(
                Team.name.asc()
            ).paginate(args.page, 10)

            # TODO add link to next page
            return teams.items

    # To test this endpoint
    # curl -d "name=Mexico" http://localhost:5000/api/team
    def post(self, team_id=None):
        if team_id:
            abort(400)
        else:
            args = team_post_parser.parse_args(strict=True)
            new_team = Team(args.get('name'))

            new_team.save()
            return new_team.id, 201

    # curl -d "name=Mexico" http://localhost:5000/api/team/{id}
    def put(self, team_id=None):
        if not team_id:
            abort(400)
        team = Team.query.get(team_id)
        if not team:
            abort(404)
        args = team_post_parser.parse_args(strict=True)
        team.name = args['name']
        team.save()
        return team.id, 201

    # curl -X DELETE http://localhost:5000/api/team/{id}
    def delete(self, team_id=None):
        if not team_id:
            abort(404)

        team = Team.query.get(team_id)
        if not team:
            abort(404)

        team.delete()
        return "", 204
