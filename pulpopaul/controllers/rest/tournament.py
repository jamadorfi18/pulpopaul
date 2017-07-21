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
`Tournament` is a collection of `Team`s and `Match`es, arranged in a certain way
that produces a winner `Team`
"""

from __future__ import unicode_literals
import datetime
from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields
from pulpopaul.models import Tournament


FIELDS = {
    'name': fields.String(),
    'short_name': fields.String(),
    'start_date': fields.DateTime(),
    'end_date': fields.DateTime(),
}

def parse_datetime(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d")


class TournamentResource(Resource):
    """
    Tournament RESTful controller
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

        def get_parser(method='post'):
            parser = reqparse.RequestParser()
            parser.add_argument(
                'name',
                type=str,
                required=True if method == 'post' else False
            )
            parser.add_argument(
                'short_name',
                type=str,
                required=False
            )
            parser.add_argument(
                'start_date',
                type=parse_datetime,
                required=True if method == 'post' else False
            )
            parser.add_argument(
                'end_date',
                type=parse_datetime,
                required=True if method == 'post' else False
            )

            return parser

        self.post_parser = get_parser('post')
        self.put_parser = get_parser('put')

    @marshal_with(FIELDS)
    def get(self, tournament_id=None):
        """
        Return a list of all tournaments, or one tournament if id is provided
        """
        if tournament_id:
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                abort(404)
            return tournament
        else:
            args = self.get_parser.parse_args()
            tournaments = Tournament.query.paginate(args.page, 10)

            return tournaments.items

    def post(self, tournament_id=None):
        if tournament_id:
            abort(400)
        else:
            args = self.post_parser.parse_args(strict=True)
            new_tournament = Tournament(**args)

            new_tournament.save()
            return new_tournament.id, 201

    def put(self, tournament_id=None):
        if not tournament_id:
            abort(400)
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            abort(404)
        args = self.put_parser.parse_args(strict=True)

        if args['name']:
            tournament.name = args['name']
        if args['short_name']:
            tournament.short_name = args['short_name']
        if args['start_date']:
            tournament.start_date = args['start_date']
        if args['end_date']:
            tournament.end_date = args['end_date']

        tournament.save()
        return tournament.id, 201

    def delete(self, tournament_id=None):
        if not tournament_id:
            abort(404)

        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            abort(404)

        tournament.delete()
        return tournament_id, 204
