#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'mock challenge home page'

@app.route('/episodes', methods=['GET'])
def episodes():
    if request.method == 'GET':
        episode_list = [episode.to_dict() for episode in Episode.query.all()]
        return make_response(
            episode_list,
            200
        )

@app.route('/episodes/<int:id>', methods=['GET', 'DELETE'])
def episode_by_id(id):
    episode = Episode.query.filter_by(id=id).first()
    if not episode:
        return make_response(
            {"error": "404: Episode not found"},
            404
        )
    elif request.method == 'GET':
        return make_response(
            episode.to_dict(rules=('guests',)),
            200
        )
    elif request.method == 'DELETE':
        db.session.delete(episode)
        db.session.commit()

        return make_response(
            {},
            204
        )

@app.route('/guests', methods=['GET'])
def guests():
    if request.method == 'GET':
        guest_list = [guest.to_dict() for guest in Guest.query.all()]
        return make_response(
            guest_list,
            200
        )

@app.route('/appearances', methods=['GET', 'POST'])
def appearances():
    if request.method == 'GET':
        appearance_list = [appearance.to_dict() for appearance in Appearance.query.all()]
        return make_response(
            appearance_list,
            200
        )
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_appearance = Appearance(
                rating = data['rating'],
                episode_id = data['episode_id'],
                guest_id = data['guest_id']
            )
            db.session.add(new_appearance)
            db.session.commit()

            return make_response(
                new_appearance.to_dict(rules=('-episode_id', '-guest_id')),
                201
            )
        except Exception as e:
            return make_response(
                {"errors": "400: Validation error"},
                400
            )


if __name__ == '__main__':
    app.run(port=5555, debug=True)

#'-episode_id', '-guest_id'