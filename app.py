from database_setup import Base, Field, MOOC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request, url_for, redirect, jsonify

engine = create_engine('sqlite:///top_mooc.db')

# Make a connection between class definitions and the corresponding tables within database
Base.metadata.bind = engine

# Establish a link of connection between code execution and the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# JSON Endpoints
@app.route('/api/categories')
def categories_json():
    """Return all fields and moocs"""
    fields = session.query(Field).all()
    fields_list = []
    for field in fields:
        moocs = session.query(MOOC).filter_by(field_id=field.id).all()
        moocs_list = [mooc.serialize for mooc in moocs]
        field_moocs = field.serialize
        field_moocs['items'] = moocs_list
        fields_list.append(field_moocs)

    return jsonify(Categories=fields_list)


@app.route('/api/fields')
def fields_json():
    """Return all fields"""
    fields = session.query(Field).all()
    return jsonify(Fields=[field.serialize for field in fields])


@app.route('/api/moocs')
def moocs_json():
    """Return all moocs"""
    moocs = session.query(MOOC).all()
    return jsonify(MOOCs=[mooc.serialize for mooc in moocs])


@app.route('/api/moocs/<int:mooc_id>')
def mooc_json(mooc_id):
    """Return a specific mooc"""
    mooc = session.query(MOOC).filter_by(id=mooc_id).first()
    if mooc is None:
        return jsonify({'error': 'This MOOC does not exist'})
    else:
        return jsonify(MOOC=[mooc.serialize])


# Normal Routing
@app.route('/')
@app.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    return "All fields and moocs here!"


@app.route('/fields/new', methods=['GET', 'POST'])
def new_field():
    """Add a new CS field"""
    if request.method == 'POST':
        pass
    else:
        return render_template('new_field.html')


@app.route('/fields/<int:field_id>/edit', methods=['GET', 'POST'])
def edit_field(field_id):
    """Edit a CS field"""
    if request.method == 'POST':
        pass
    else:
        return render_template('edit_field.html')


@app.route('/fields/<int:field_id>/delete', methods=['GET', 'POST'])
def delete_field(field_id):
    """Delete a CS field"""
    if request.method == 'POST':
        pass
    else:
        return render_template('delete_field.html')


@app.route('/fields/<int:field_id>/')
@app.route('/fields/<int:field_id>/moocs/')
def show_moocs(field_id):
    """Show all MOOCs with a specific field"""
    return render_template('moocs.html')


@app.route('/fields/<int:field_id>/moocs/new', methods=['GET', 'POST'])
def new_mooc(field_id):
    """Add new MOOC"""
    if request.method == 'POST':
        pass
    else:
        return render_template('new_mooc.html')


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/edit', methods=['GET', 'POST'])
def edit_mooc(field_id, mooc_id):
    """Edit a MOOC"""
    if request.method == 'POST':
        pass
    else:
        return render_template('edit_mooc.html')


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/delete', methods=['GET', 'POST'])
def delete_mooc(field_id, mooc_id):
    """Delete a MOOC"""
    if request.method == 'POST':
        pass
    else:
        return render_template('delete_mooc.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
