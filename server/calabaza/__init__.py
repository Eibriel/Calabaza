from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.restful import Api

from calabaza.calabaza_auth import CalabazaAuth

app = Flask(__name__)

api = Api(app)
mongo = PyMongo(app)

app.secret_key = CalabazaAuth.flask_key

class Connection():
    def register(self, documents):
        pass

class Document():
    _data = {}
    def __setitem__(self, key, value):
        print (key)
        if self.structure.get(key) and self.validators.get(key)(value):
            self._data[key] = value
            print(value)

    def safe(self):
        return self._data

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

class userModel(Document):
    structure = {
        'username':str,
        'email':str,
        'password':str
    }

    validators = {
        'username':max_length(12),
        'email':max_length(120),
        'password':max_length(16),
    }

    use_dot_notation = True

    def __repr__(self):
        return '<User %r>' % (self.name)

connection = Connection()
connection.register([userModel])

from calabaza.modules.api.game import GameListApi
from calabaza.modules.api.game import GameActionApi
api.add_resource(GameListApi, '/api/game')
api.add_resource(GameActionApi, '/api/game/action/<action_id>')

from calabaza.modules.api.user import UserListApi
from calabaza.modules.api.user import UserApi
from calabaza.modules.api.user import UserLogoutApi
api.add_resource(UserListApi, '/api/user')
api.add_resource(UserApi, '/api/user/<job_id>')
api.add_resource(UserLogoutApi, '/api/user/logout')

from calabaza.modules.main import main
app.register_blueprint(main)
