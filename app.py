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


@app.route('/')
@app.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    return "All fields with latest moocs here!"


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
