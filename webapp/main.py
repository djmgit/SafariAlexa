from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)
if os.environ.get('DATABASE_URL') is None:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/deep'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "THIS IS SECRET"

db = SQLAlchemy(app)

# define constants
STATUS = {'_FOUND': 'FOUND', '_NOT_FOUND': 'NOT_FOUND', '_EMPTY_QUERY': 'EMPTY_QUERY'}

class StateDB(db.Model):
    __tablename__ = 'statedb'

    id = db.Column('software_id', db.Integer, primary_key=True)
    state_name = db.Column(db.String)
    places_to_visit = db.Column(db.String)

    def __init__(self, state_name='', places_to_visit=''):
        self.state_name = state_name
        self.places_to_visit = places_to_visit

class Spots(db.Model):
    __tablename__ = 'spots'

    id = db.Column('spot_id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    info = db.Column(db.String)
    special_attraction = db.Column(db.String)
    things_to_do = db.Column(db.String)
    time_to_visit = db.Column(db.String)
    near_by_places = db.Column(db.String)
    similar_places = db.Column(db.String)
    how_to_reach = db.Column(db.String)

    def __init__(self, name='', location='', info='', special_attraction='', things_to_do='', time_to_visit='', near_by_places='', similar_places='', how_to_reach=''):
        self.name = name
        self.location = location
        self.info = info
        self.special_attraction = special_attraction
        self.things_to_do = things_to_do
        self.time_to_visit = time_to_visit
        self.near_by_places = near_by_places
        self.similar_places = similar_places
        self.how_to_reach = how_to_reach

db.create_all();

class StateDBView(ModelView):
    can_create = True
    can_view_details = True
    column_searchable_list = ['state_name']
    edit_modal = True
    column_filters = ['state_name', 'places_to_visit']

# setup admin
admin = Admin(app, name='AlexaSafari', template_mode='bootstrap3')
admin.add_view(StateDBView(StateDB, db.session))

@app.route('/api/query_state')
def query_state():
    response = {}
    state = request.args.get('state')

    if not state:
        response['STATUS'] = STATUS['_EMPTY_QUERY']
        return jsonify(response)

    state = state.lower() 

    state_obj = StateDB.query.filter_by(state_name=state).all()

    if not state_obj:
        response['state_name'] = state
        response['status'] = STATUS['_NOT_FOUND']
        return jsonify(response)

    state_obj = state_obj[0]
    places_to_visit = state_obj.places_to_visit

    response['status'] = STATUS['_FOUND']
    response['state_name'] = state
    response['places_to_visit'] = places_to_visit

    return jsonify(response)



@app.route('/')
def index():
	return 'alexa back end!!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
