# -*- coding: utf-8 -*-
# pulpopaul - a platform to guess which teams is going to win
# Copyright (C) 2017 Juan José González

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
`Match` is a confrontation between two `Team`s
"""

from __future__ import unicode_literals
import datetime
from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields
from pulpopaul.models import Match


FIELDS = {
    'team_local_id': fields.String(),
    'team_visitor_id': fields.String(),
    'score_local': fields.Integer(),
    'score_visitor': fields.Integer(),
    'kickoff_at': fields.DateTime(),
}

def parse_datetime(string):
    """Parse datetime format"""
    return datetime.datetime.strptime(string, "%Y-%m-%d")


class MatchResource(Resource):
    """
    Match RESTful controller
    """

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'page',
            type=int,
            location=['args', 'headers'],
            required=False,
            default=1
        )

        def create_parser(method='post'):
            parser = reqparse.RequestParser()
            parser.add_argument(
                'team_local_id',
                type=int,
                required=True if method == 'post' else False
            )
            parser.add_argument(
                'team_visitor_id',
                type=int,
                required=True if method == 'post' else False
            )
            parser.add_argument(
                'kickoff_at',
                type=parse_datetime,
                required=True if method == 'post' else False
            )
            parser.add_argument(
                'score_local',
                type=int,
                required=False
            )
            parser.add_argument(
                'score_visitor',
                type=int,
                required=False
            )

            return parser

        self.post_parser = create_parser('post')
        self.put_parser = create_parser('put')

    @marshal_with(FIELDS)
    def get(self, match_id=None):
        """
        Return a list of all matches, or one match if id is provided
        """
        if match_id:
            match = Match.query.get(match_id)
            if not match:
                abort(404)
            return match
        else:
            args = self.get_parser.parse_args()
            matches = Match.query.paginate(args.page, 10)

            return matches.items

    def post(self, match_id=None):
        if match_id:
            abort(400)
        else:
            args = self.post_parser.parse_args(strict=True)
            new_match = Match(**args)

            new_match.save()
            return new_match.id, 201

    def put(self, match_id=None):
        if not match_id:
            abort(400)
        match = Match.query.get(match_id)
        if not match:
            abort(404)
        args = self.put_parser.parse_args(strict=True)

        if args['team_local_id']:
            match.team_local_id = args['team_local_id']
        if args['team_visitor_id']:
            match.team_visitor_id = args['team_visitor_id']
        if args['kickoff_at']:
            match.kickoff_at = args['kickoff_at']
        if args['score_local']:
            match.score_local = args['score_local']
        if args['score_visitor']:
            match.score_visitor = args['score_visitor']

        match.save()
        return match.id, 201

    def delete(self, match_id=None):
        if not match_id:
            abort(404)

        match = Match.query.get(match_id)
        if not match:
            abort(404)

        match.delete()
        return match_id, 204
