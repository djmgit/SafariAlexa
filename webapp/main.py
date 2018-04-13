from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
#from scrapers import get_time_to_visit
import requests
from bs4 import BeautifulSoup as bs
import traceback
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

BASE_QUERY = 'best time to visit'
BASE_URL = "https://www.google.co.in/search"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def get_html_page(place_name):
    url_query = "{} {}".format(BASE_QUERY, place_name)
    url = "{}?q={}".format(BASE_URL, url_query)
    response = requests.get(url, headers=headers, timeout=5)

    return response.content, response.status_code

def get_time_to_visit(place_name):

    response = {}

    html, status_code = get_html_page(place_name)
    if status_code != 200:
        response['status'] = 'NOT_FOUND'
        return response

    soup = bs(html, 'html.parser')
    try:
        data = soup.find_all('div', {'class': 'mod', 'data-md': '61'})[0]
        if data:
            response['status'] = 'FOUND'
            response['data'] = data.get_text()
        else:
            response['status'] = 'NOT_FOUND'
    except:
        response['status'] = 'NOT_FOUND'
        
    return response

# define constants
STATUS = {'_FOUND': 'FOUND', '_NOT_FOUND': 'NOT_FOUND'}
STATUS['_EMPTY_STATE'] = 'state cannot be empty'
STATUS['_EMPTY_SPOT'] = 'spot cannot be empty'
STATUS['_EMPTY_TYPE'] = 'type cannot be empty'

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

class User(db.Model):
    __tablename__ = "users"

    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, email='', password=''):
        self.email = email
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.email
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)

db.create_all();

class StateDBView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')
    can_create = True
    can_view_details = True
    column_searchable_list = ['state_name']
    edit_modal = True
    column_filters = ['state_name', 'places_to_visit']

class SpotDBView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

    can_create = True
    can_view_details = True
    edit_modal = True

class UserDBView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')
    can_create = True
    column_searchable_list = ['email']

class AdminLogin(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        return self.render('admin-login.html')

# setup admin
admin = Admin(app, name='AlexaSafari', template_mode='bootstrap3')
admin.add_view(AdminLogin(name='Admin Auth', endpoint='adminlogin'))
admin.add_view(StateDBView(StateDB, db.session))
admin.add_view(SpotDBView(Spots, db.session))
admin.add_view(UserDBView(User, db.session))

# setup authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user)
                g.user = current_user
                return redirect('/admin')
            else:
                return redirect('/admin/adminlogin')
        else:
            return redirect('/admin/adminlogin')
    else:
        return redirect('/admin/adminlogin')

@app.route('/api/query_state')
def query_state():
    response = {}
    state = request.args.get('state')

    if not state:
        response['status'] = STATUS['_EMPTY_STATE']
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

@app.route('/api/query_spot')
def query_spot():
    response = {}
    spot = request.args.get('spot')
    query_type = request.args.get('query_type')

    if not spot:
        response['status'] = STATUS['_EMPTY_SPOT']
        return jsonify(response)

    if not query_type:
        response['status'] = STATUS['_EMPTY_TYPE']
        return jsonify(response)

    spot = spot.lower()

    spot_obj = Spots.query.filter_by(name=spot).all()

    if spot_obj:
        print ("heeeeeeehaaaaaaaaaaa")

    # if not present in data base then scrape from web
    print ('jajajajaaj')
    if not spot_obj:
        print ('hahahahaha')
        print ('scraping data')
        response['spot_name'] = spot
        collected_data = collect_data(spot, query_type)
        print (collected_data)

        # check status first
        if collected_data['status'] == STATUS['_NOT_FOUND']:
            response['status'] = STATUS['_NOT_FOUND']
        else:
            response['status'] = STATUS['_FOUND']
            response[query_type] = collected_data['data']
        return jsonify(response)

    spot_obj = spot_obj[0]
    response['spot_name'] = spot
    response['status'] = STATUS['_FOUND']

    if query_type == 'location':
        response['location'] = spot_obj.location

    if query_type == 'info':
        response['info'] = spot_obj.info

    if query_type == 'things_to_do':
        response['things_to_do'] = spot_obj.things_to_do

    if query_type == 'special_attraction':
        response['special_attraction'] = spot_obj.special_attraction

    if query_type == 'time_to_visit':
        response['time_to_visit'] = spot_obj.time_to_visit

    if query_type == 'near_by_places':
        response['near_by_places'] = spot_obj.near_by_places

    if query_type == 'similar_places':
        response['similar_places'] = spot_obj.similar_places

    if query_type == 'how_to_reach':
        response['how_to_reach'] = spot_obj.how_to_reach

    return jsonify(response);

def collect_data(spot, query_type):
    print ('inside collectdata')
    response = {}
    response['status'] = STATUS['_NOT_FOUND']

    if query_type == 'time_to_visit':
        print ('inside time_to_visit')
        response = get_time_to_visit(spot)

    return response

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/admin/adminlogin')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect('/admin')

@app.route('/')
def index():
	return 'alexa back end!!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
