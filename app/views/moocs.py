from app.models import session, Field, MOOC, User
from app.models.user_helper import *

from sqlalchemy import asc, desc

from flask import render_template, request, url_for,\
    redirect, jsonify, flash, Blueprint

from flask import session as login_session

from .decorators import login_required, category_exist, item_exist
mooc = Blueprint('mooc', __name__)


@mooc.route('/fields/<int:field_id>/')
@mooc.route('/fields/<int:field_id>/moocs/')
@category_exist
def show_moocs(field_id):
    """Show all MOOCs with a specific field"""
    field = session.query(Field).filter_by(id=field_id).first()
    fields = session.query(Field).order_by(asc(Field.name)).all()
    moocs = session.query(MOOC).filter_by(field_id=field_id)\
        .order_by(asc(MOOC.title)).all()
    creator = get_user_info(field.user_id)

    # Prevent unauthorized users from modification, They must login first
    if 'username' not in login_session:
        return render_template('public_moocs.html', field=field,
                               moocs=moocs, creator=creator, fields=fields)

    return render_template('moocs.html', field=field,
                           moocs=moocs, creator=creator, fields=fields)


@mooc.route('/fields/<int:field_id>/moocs/<int:mooc_id>/')
@item_exist
def show_mooc(field_id, mooc_id):
    """Show a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Prevent unauthorized users from modification, They must login first
    if 'username' not in login_session:
        return render_template('public_mooc.html', field=field, mooc=mooc)

    return render_template('mooc.html', field=field, mooc=mooc)


@mooc.route('/fields/<int:field_id>/moocs/new', methods=['GET', 'POST'])
@category_exist
@login_required
def new_mooc(field_id):
    """Add new MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()

    if request.method == 'POST':
        if request.form.get('title') and request.form.get('provider') \
                and request.form.get('url'):
            mooc = MOOC(title=request.form.get('title'),
                        provider=request.form.get('provider'),
                        creator=request.form.get('creator'),
                        level=request.form.get('level'),
                        url=request.form.get('url'),
                        description=request.form.get('description'),
                        image=request.form.get('image'),
                        field=field, user_id=login_session.get('user_id'))
            session.add(mooc)
            session.commit()
            flash('New MOOC {} Successfully Created'.format(mooc.title))
        return redirect(url_for('mooc.show_moocs', field_id=field_id))

    return render_template('new_mooc.html', field=field)


@mooc.route('/fields/<int:field_id>/moocs/<int:mooc_id>/edit',
            methods=['GET', 'POST'])
@item_exist
@login_required
def edit_mooc(field_id, mooc_id):
    """Edit a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Verify if he is the user who created it
    if mooc.user_id == login_session['user_id']:
        if request.method == 'POST':
            if request.form.get('title'):
                mooc.title = request.form.get('title')
            if request.form.get('provider'):
                mooc.provider = request.form.get('provider')
            if request.form.get('creator'):
                mooc.creator = request.form.get('creator')
            if request.form.get('level'):
                mooc.level = request.form.get('level')
            if request.form.get('url'):
                mooc.url = request.form.get('url')
            if request.form.get('description'):
                mooc.description = request.form.get('description')
            if request.form.get('image'):
                mooc.image = request.form.get('image')
            session.add(mooc)
            session.commit()
            flash('MOOC {} Successfully Edited'.format(mooc.title))
            return redirect(url_for('mooc.show_moocs', field_id=field_id))

        return render_template('edit_mooc.html', mooc=mooc, field=field)
    else:
        return jsonify(error={'msg': "You are not the owner of that!!"}), 401


@mooc.route('/fields/<int:field_id>/moocs/<int:mooc_id>/delete',
            methods=['GET', 'POST'])
@item_exist
@login_required
def delete_mooc(field_id, mooc_id):
    """Delete a MOOC"""

    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Verify if he is the user who created it
    if mooc.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(mooc)
            session.commit()
            flash('MOOC {} Successfully Deleted'.format(mooc.title))
            return redirect(url_for('mooc.show_moocs', field_id=field_id))

        return render_template('delete_mooc.html', mooc=mooc, field=field)
    else:
        return jsonify(error={'msg': "You are not the owner of that!!"}), 401
