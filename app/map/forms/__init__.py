from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class csv_upload(FlaskForm):
  file = FileField()
  submit = SubmitField()

class location_edit_form(FlaskForm):
    title = StringField('Location Name', [
        validators.DataRequired(),

    ], description="Name of the location")
    longitude = StringField('Longitude', [
        validators.DataRequired(),

    ], description="Longitude of the location")
    latitude = StringField('Latitude', [
        validators.DataRequired(),

    ], description="Latitude of the location")
    population = IntegerField('Population', [
        validators.DataRequired(),

    ], description="Population of the location")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()

class location_form(FlaskForm):
    title = StringField('Location Name', [
        validators.DataRequired(),

    ], description="Name of the location")
    longitude = StringField('Longitude', [
        validators.DataRequired(),

    ], description="Longitude of the location")
    latitude = StringField('Latitude', [
        validators.DataRequired(),

    ], description="Latitude of the location")
    population = IntegerField('Population', [
        validators.DataRequired(),

    ], description="Population of the location")
    submit = SubmitField()


class register_form(FlaskForm):
  email = EmailField('Email Address', [
    validators.DataRequired(),

  ], description="You need to signup with an email")

  password = PasswordField('Create Password', [
    validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords must match'),

  ], description="Create a password ")
  confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
  submit = SubmitField()