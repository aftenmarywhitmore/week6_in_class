#what we send off to our database to create our tables 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from flask_marshmallow import Marshmallow

#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash 

#Import for Secrets - creates a user token
import secrets

#timestamp for user creation 
from datetime import datetime

#flask login to check for an authenticated user 
from flask_login import UserMixin, LoginManager

db = SQLAlchemy() #instantiating <--don't forget ()
login_manager = LoginManager() 
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    #setting attributes which will be our columns 
    #when we assign attributes we instantiate a user 
    #creating columns and users
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '') #if we don't instantiate or provide data, it will be null/empty
    last_name = db.Column(db.String(150), nullable = True, default = '') #if no last name, it will come back null/empty
    email = db.Column(db.String(150), nullable = False) #nullable = False because we need data in email format 
    password = db.Column(db.String, nullable = True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = "", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref='owner', lazy=True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24) #token hex function takes in a length which we pass here and is 24 characters long
        self.g_auth_verify = g_auth_verify 

    def set_token(self, length):
        return secrets.token_hex(length) #return a random text string, string has nbytes and random bytes, each byte converted to two hex digits, if nbytes is non a reasonable default is used

    def set_id(self):
        return str(uuid.uuid4()) #creates a random id for us so we don't have to do it? Idk what this is...google later https://docs.python.org/3/library/uuid.html

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 
        #what in the motherlickin frick is going on

    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale = 2))
    camera_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token, id = ''):
        self.id = self.set_id()
        self.name = name 
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions 
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series 
        self.user_token = user_token

    def __repr__(self):
        return f"The following Drone has been added: {self.name}"

    def set_id(self):
        return secrets.token_urlsafe()

class DroneSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_production', 'series']


drone_schema = DroneSchema()
drones_schema = DroneSchema(many = True)
