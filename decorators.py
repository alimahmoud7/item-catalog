from functools import wraps
from flask import redirect, url_for, jsonify,\
    session as login_session
from database_setup import Base, Field, MOOC, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///top_mooc.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Prevent unauthorized users from modification, They must login first
        if 'username' not in login_session:
            return redirect(url_for('show_login'))
        return func(*args, **kwargs)
    return wrapper


def category_exist(func):
    @wraps(func)
    def wrapper(field_id):
        # Check if field doesn't exist in database
        if session.query(Field).filter_by(id=field_id).first() is None:
            return jsonify({'error': 'This Field does not exist!'})
        return func(field_id)
    return wrapper


def item_exist(func):
    @wraps(func)
    def wrapper(field_id, mooc_id):
        # Check if mooc doesn't exist in database
        if session.query(MOOC).filter_by(id=mooc_id, field_id=field_id)\
                .first() is None:
            return jsonify({'error': 'This MOOC does not exist!'})
        return func(field_id, mooc_id)
    return wrapper


# TODO: Add owner_check decorator for catalog and item
