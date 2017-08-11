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
def index():
    return "Hello!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
