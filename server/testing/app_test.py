from app import app
from models import db, Episode, Guest, Appearance

class TestApp:
    '''Flask application in app.py'''

    def test_gets_episodes(self):
        '''retrieves episodes with GET requests to /episodes.'''

        with app.app_context():
            Episode.query.delete()
            db.session.commit()

            e1 = Episode(date='1/1/2000', number=1)
            db.session.add(e1)
            db.session.commit()

            response = app.test_client().get('/episodes').json
            episodes = Episode.query.all()
            assert [episode['id'] for episode in response] == [episode.id for episode in episodes]
            assert [episode['date'] for episode in response] == [episode.date for episode in episodes]
            assert [episode['number'] for episode in response] == [episode.number for episode in episodes]

    def test_gets_episode_by_id(self):
        '''retrieves one episode using its ID with GET request to /episodes/<int:id>.'''

        with app.app_context():
            Episode.query.delete()
            db.session.commit()

            e2 = Episode(date='1/2/2000', number=2)
            db.session.add(e2)
            db.session.commit()

            response = app.test_client().get(f'/episodes/{e2.id}').json
            assert response['date'] == e2.date
            assert response['number'] == e2.number

            none_response = app.test_client().get(f'/episodes/3')
            assert none_response.json == {"error": "404: Episode not found"}
            assert none_response.status_code == 404

    def test_deletes_episode(self):
        '''deletes one episode using its ID with DELETE request to /episodes/<int:id>.'''

        with app.app_context():
            Episode.query.delete()
            db.session.commit()

            e3 = Episode(date='1/3/2000', number=3)
            db.session.add(e3)
            db.session.commit()

            response = app.test_client().delete(f'/episodes/{e3.id}')
            assert response.status_code == 204
            e3 = Episode.query.filter(Episode.id == e3.id).one_or_none()
            assert not e3

            none_response = app.test_client().delete(f'/episodes/4')
            assert none_response.json == {"error": "404: Episode not found"}
            assert none_response.status_code == 404

    def test_gets_guests(self):
        '''retrieves guests with GET requests to /guests.'''

        with app.app_context():
            Guest.query.delete()
            db.session.commit()

            g1 = Guest(name="Ben Botsford", occupation="Senior Python Curriculum Developer")
            db.session.add(g1)
            db.session.commit()

            response = app.test_client().get('/guests').json
            guests = Guest.query.all()
            assert [guest['id'] for guest in response] == [guest.id for guest in guests]
            assert [guest['name'] for guest in response] == [guest.name for guest in guests]
            assert [guest['occupation'] for guest in response] == [guest.occupation for guest in guests]

    def test_creates_appearance(self):
        '''creates appearances with POST requests to /appearances.'''

        with app.app_context():
            Episode.query.delete()
            Guest.query.delete()
            Appearance.query.delete()
            db.session.commit()

            e1 = Episode(date='1/1/2000', number=1)
            g1 = Guest(name="Ben Botsford", occupation="Senior Python Curriculum Developer")
            db.session.add_all([e1, g1])
            db.session.commit()

            response_json = app.test_client().post(
                '/appearances',
                json={
                    'rating': 1,
                    'episode_id': e1.id,
                    'guest_id': g1.id,
                }
            ).json

            assert response_json['rating'] == 1
            # assert response_json['episode_id'] == e1.id
            # assert response_json['guest_id'] == g1.id

            appearance = Appearance.query.filter(Appearance.id == response_json['id']).first()
            assert appearance.rating == 1
            assert appearance.episode == e1
            assert appearance.guest == g1
