from database_setup import Base, Field, MOOC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request, url_for, redirect

engine = create_engine('sqlite:///top_mooc.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    return "All fields with latest moocs here!"


@app.route('/fields/new')
def new_field():
    """Add a new CS field"""
    return "Create a new field here!"


@app.route('/fields/<int:field_id>/edit')
def edit_field(field_id):
    """Edit a CS field"""
    return "Edit a specific field here!"


@app.route('/fields/<int:field_id>/delete')
def delete_field(field_id):
    """Delete a CS field"""
    return "Delete a specific field here!"


@app.route('/fields/<int:field_id>/')
@app.route('/fields/<int:field_id>/moocs/')
def show_moocs(field_id):
    """Show all MOOCs with a specific field"""
    return "All moocs with a specific field here!"


@app.route('/fields/<int:field_id>/moocs/new')
def new_mooc(field_id):
    """Add new MOOC"""
    return "Create a new mooc here!"


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/edit')
def edit_mooc(field_id, mooc_id):
    """Edit a MOOC"""
    return "Edit a specific mooc here!"


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/delete')
def delete_mooc(field_id, mooc_id):
    """Delete a MOOC"""
    return "Delete a specific mooc here!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
