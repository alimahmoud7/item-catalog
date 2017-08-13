from database_setup import Base, Field, MOOC
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request, url_for, redirect, jsonify

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json
from flask import make_response

engine = create_engine('sqlite:///top_mooc.db')

# Make a connection between class definitions and the corresponding tables within database
Base.metadata.bind = engine

# Establish a link of connection between code execution and the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
APPLICATION_NAME = "Top MOOC App"
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


# Authentication & Authorization
@app.route('/login')
def show_login():
    """Show login page and Generate a random state token"""
    state = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Handle login authentication and authorization with Google"""
    # Validate state token
    if request.args.get('state') != login_session.get('state'):
        print('Invalid state parameter.')
        return jsonify(error={'msg': 'Invalid state parameter.'}), 401

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        print('Failed to upgrade the authorization code.')
        return jsonify(error={'msg': 'Failed to upgrade the authorization code.'}), 401

    # Check that the access token is valid
    access_token = credentials.access_token
    print('access_token:', access_token)  ####
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
    result = requests.get(url).json()
    print('result7 by requests:', result)  ####

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        return jsonify(error={'msg': result.get('error')}), 500

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    print('gplus_id7:', gplus_id)  ####
    print('credentials.id_token:', credentials.id_token)  ####
    if result.get('user_id') != gplus_id:
        return jsonify(error={'msg': "Token's user ID doesn't match given user ID."}), 401

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        print("Token's client ID does not match app's.")
        return jsonify(error={'msg': "Token's client ID does not match app's."}), 401

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    print('stored_access_token:', stored_access_token)  #######
    print('stored_gplus_id:', stored_gplus_id)  #####
    print('login_session7:', login_session)  ########

    if stored_access_token is not None and stored_gplus_id == gplus_id:
        # Update the access_token in login_session
        login_session['access_token'] = credentials.access_token
        return jsonify(success={'msg': 'Current user is already connected.'}), 200

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    data = requests.get(userinfo_url, params=params).json()
    print('data7:', data)  ####

    # Store user info in the current session
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    welcome_html = '''
    <h1>Welcome, {}! <h1>
    <img src="{}" style="width: 200px; height: 200px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">
    '''
    print("done!")
    return welcome_html.format(login_session['username'], login_session['picture'])


@app.route('/gdisconnect/')
def gdisconnect():
    """Logout from Google Auth"""
    access_token = login_session.get('access_token')
    print('access_token7:', access_token)
    gplus_id = login_session.get('gplus_id')
    if gplus_id is None:
        print('Current user not connected.')
        return jsonify(error={'msg': 'Current user not connected.'}), 401

    print('In gdisconnect access token is {}'.format(access_token))
    print('User name is: {}'.format(login_session['username']))
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result httplib2 {}'.format(result))
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        # del login_session['user_id']
        del login_session['provider']
        print('login_session', login_session)
        return jsonify(success={'msg': 'Successfully disconnected.'})
    else:
        return jsonify(error={'msg': 'Failed to revoke token for given user.'}), 400


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
        return jsonify({'error': 'This MOOC does not exist!'})
    return jsonify(MOOC=[mooc.serialize])


# Normal Routing
@app.route('/')
@app.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    fields = session.query(Field).order_by(asc(Field.name)).all()
    moocs = session.query(MOOC).order_by(desc(MOOC.id)).all()
    return render_template('index.html', fields=fields, moocs=moocs)


@app.route('/fields/new', methods=['GET', 'POST'])
def new_field():
    """Add a new CS field"""
    if request.method == 'POST':
        if request.form.get('name'):
            field = Field(name=request.form.get('name'))
            session.add(field)
            session.commit()
        return redirect(url_for('index'))

    return render_template('new_field.html')


@app.route('/fields/<int:field_id>/edit', methods=['GET', 'POST'])
def edit_field(field_id):
    """Edit a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        if request.form.get('name'):
            field.name = request.form.get('name')
            session.add(field)
            session.commit()
        return redirect(url_for('index'))

    return render_template('edit_field.html', field=field)


@app.route('/fields/<int:field_id>/delete', methods=['GET', 'POST'])
def delete_field(field_id):
    """Delete a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        session.delete(field)
        session.commit()

        # Delete Field MOOCs too
        moocs = session.query(MOOC).filter_by(field_id=field.id).all()
        for mooc in moocs:
            session.delete(mooc)
            session.commit()

        return redirect(url_for('index'))

    return render_template('delete_field.html', field=field)


@app.route('/fields/<int:field_id>/')
@app.route('/fields/<int:field_id>/moocs/')
def show_moocs(field_id):
    """Show all MOOCs with a specific field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    moocs = session.query(MOOC).filter_by(field_id=field_id).order_by(asc(MOOC.title)).all()
    return render_template('moocs.html', field=field, moocs=moocs)


@app.route('/fields/<int:field_id>/moocs/new', methods=['GET', 'POST'])
def new_mooc(field_id):
    """Add new MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        if request.form.get('title') and request.form.get('provider') and request.form.get('url'):
            mooc = MOOC(title=request.form.get('title'), provider=request.form.get('provider'),
                        creator=request.form.get('creator'), level=request.form.get('level'),
                        url=request.form.get('url'), description=request.form.get('description'),
                        image=request.form.get('image'), field=field)
            session.add(mooc)
            session.commit()
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('new_mooc.html', field=field)


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/edit', methods=['GET', 'POST'])
def edit_mooc(field_id, mooc_id):
    """Edit a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Check if field doesn't exist in database
    if mooc is None or field is None:
        return jsonify({'error': 'This MOOC does not exist!'})

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
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('edit_mooc.html', mooc=mooc, field=field)


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/delete', methods=['GET', 'POST'])
def delete_mooc(field_id, mooc_id):
    """Delete a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Check if field doesn't exist in database
    if mooc is None or field is None:
        return jsonify({'error': 'This MOOC does not exist!'})

    if request.method == 'POST':
        session.delete(mooc)
        session.commit()
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('delete_mooc.html', mooc=mooc, field=field)


if __name__ == '__main__':
    app.secret_key = 'bluehat7_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
