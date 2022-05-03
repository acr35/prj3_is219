import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Location
from app.map.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

map = Blueprint('map', __name__,
                        template_folder='templates')



@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def location_upload():
    form = csv_upload()

    try:
        return render_template('upload_locations.html', form=form)
    except TemplateNotFound:
        abort(404)