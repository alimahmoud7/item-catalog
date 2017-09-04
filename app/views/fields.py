from app.models import session, Field, MOOC, User
from app.models.user_helper import *

from sqlalchemy import asc, desc

from flask import render_template, request, url_for,\
    redirect, jsonify, flash, Blueprint

from flask import session as login_session

from .decorators import login_required, category_exist

field = Blueprint('field', __name__)


@field.route('/')
@field.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    fields = session.query(Field).order_by(asc(Field.name)).all()
    moocs = session.query(MOOC).order_by(desc(MOOC.id)).all()

    # Prevent unauthorized users from modification, They must login first
    if 'username' not in login_session:
        return render_template('public_index.html', fields=fields, moocs=moocs)

    return render_template('index.html', fields=fields, moocs=moocs)


@field.route('/fields/new', methods=['GET', 'POST'])
@login_required
def new_field():
    """Add a new CS field"""
    if request.method == 'POST':
        if request.form.get('name'):
            field = Field(name=request.form.get('name'),
                          user_id=login_session.get('user_id'))
            session.add(field)
            session.commit()
            flash('New Field {} Successfully Created'.format(field.name))
        return redirect(url_for('field.index'))

    return render_template('new_field.html')


@field.route('/fields/<int:field_id>/edit', methods=['GET', 'POST'])
@category_exist
@login_required
def edit_field(field_id):
    """Edit a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Verify if he is the user who created it
    if field.user_id == login_session['user_id']:
        if request.method == 'POST':
            if request.form.get('name'):
                field.name = request.form.get('name')
                session.add(field)
                flash('Field Successfully Edited {}'.format(field.name))
                session.commit()
            return redirect(url_for('field.index'))

        return render_template('edit_field.html', field=field)
    else:
        return jsonify(error={'msg': "You are not the owner of that!!"}), 401


@field.route('/fields/<int:field_id>/delete', methods=['GET', 'POST'])
@category_exist
@login_required
def delete_field(field_id):
    """Delete a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Verify if he is the user who created it
    if field.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(field)
            flash('Field {} Successfully Deleted'.format(field.name))
            session.commit()

            # Delete Field MOOCs too
            moocs = session.query(MOOC).filter_by(field_id=field.id).all()
            for mooc in moocs:
                session.delete(mooc)
                flash('MOOC {} Successfully Deleted'.format(mooc.title))
                session.commit()

            return redirect(url_for('field.index'))

        return render_template('delete_field.html', field=field)
    else:
        return jsonify(error={'msg': "You are not the owner of that!!"}), 401
