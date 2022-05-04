import csv
import json
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, jsonify
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Location
from app.songs.forms import csv_upload
from werkzeug.utils import secure_filename, redirect
from flask import Response

map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations', methods=['GET'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET'])
def browse_locations(page):
    page = page
    per_page = 10
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_locations.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@map.route('/locations_datatables/', methods=['GET'])
def browse_locations_datatables():

    data = Location.query.all()

    try:
        return render_template('browse_locations_datatables.html',data=data)
    except TemplateNotFound:
        abort(404)

@map.route('/api/locations/', methods=['GET'])
def api_locations():
    data = Location.query.all()
    try:
        return jsonify(data=[location.serialize() for location in data])
    except TemplateNotFound:
        abort(404)


@map.route('/locations/map', methods=['GET'])
def map_locations():
    google_api_key = current_app.config.get('GOOGLE_API_KEY')
    log = logging.getLogger("myApp")
    log.info(google_api_key)
    try:
        return render_template('map_locations.html',google_api_key=google_api_key)
    except TemplateNotFound:
        abort(404)



@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def location_upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_locations = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_locations.append(Location(row['location'],row['longitude'],row['latitude'],row['population']))

        current_user.locations = list_of_locations
        db.session.commit()

        return redirect(url_for('map.browse_locations'))

    try:
        return render_template('upload_locations.html', form=form)
    except TemplateNotFound:
        abort(404)

@map.route('/locations')
@login_required
@admin_required
def browse_locations():
    current_app.logger.info('Info level log')
    current_app.logger.warning('Warning level log')
    data = Location.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    edit_url = ('map.edit_location', [('location_id', ':id')])
    add_url = url_for('map.add_location')
    delete_url = ('map.delete_location', [('location_id', ':id')])
    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           data=data, Location=Location, record_type="Locations")


@map.route('/locations/<int:location_id>')
@login_required
def retrieve_location(location_id):
    location = Location.query.get(location_id)
    return render_template('profile_view.html', location=location)


@map.route('/locations/<int:location_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_location(location_id):
    location = Location.query.get(location_id)
    form = location_edit_form(obj=location)
    if form.validate_on_submit():
        location.about = form.about.data
        location.is_admin = int(form.is_admin.data)
        db.session.add(location)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        return redirect(url_for('map.browse_locations'))
    return render_template('location_edit.html', form=form)


@map.route('/locations/new', methods=['POST', 'GET'])
@login_required
def add_location():
    form = register_form()
    if form.validate_on_submit():
        location = Location.query.filter_by(email=form.email.data).first()
        if location is None:
            location = Location(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(location)
            db.session.commit()
            flash('Congratulations, you just created a location', 'success')
            return redirect(url_for('map.browse_locations'))
        else:
            flash('Already Registered')
            return redirect(url_for('map.browse_locations'))
    return render_template('location_new.html', form=form)


@map.route('/locations/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_locations(location_id):
    location = Location.query.get(location_id)
    if location.id == current_location.id:
        flash("You can't delete yourself!")
        return redirect(url_for('map.browse_locations'), 302)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations'), 302)
