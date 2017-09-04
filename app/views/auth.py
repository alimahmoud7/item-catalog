from app.models.user_helper import *

from flask import render_template, request, url_for,\
    redirect, jsonify, flash, Blueprint

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json
from flask import make_response

from app import csrf

# OAuth client ID for Google
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# OAuth APP ID and SECRET for Facebook
APP_ID = '1407391409368190'
APP_SECRET = '629a86589bbad38ab16ac6692967cac2'

auth = Blueprint('auth', __name__)


# Authentication & Authorization
@auth.route('/login/')
def show_login():
    """Show login page and Generate a random state token"""
    state = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@auth.route('/gconnect', methods=['POST'])
@csrf.exempt
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
        return jsonify(error={
            'msg': 'Failed to upgrade the authorization code.'}), 401

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    result = requests.get(url).json()

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        return jsonify(error={'msg': result.get('error')}), 500

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result.get('user_id') != gplus_id:
        return jsonify(error={
            'msg': "Token's user ID doesn't match given user ID."}), 401

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        print("Token's client ID does not match app's.")
        return jsonify(error={
            'msg': "Token's client ID does not match app's."}), 401

    # Verify if the user already connected
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and stored_gplus_id == gplus_id:
        # Update the access_token in login_session
        # to avoid error when signing out :)
        login_session['access_token'] = credentials.access_token
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    data = requests.get(userinfo_url, params=params).json()

    # Store user info in the current session
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create a new user if it doesn't exist
    old_user = False  # Track if user logged in before
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        # Create a new user
        user_id = create_user(login_session)
    else:
        old_user = True  # User in database so welcome back!
    login_session['user_id'] = user_id

    flash("You are now logged in as {}".format(login_session['username']))

    welcome = '''
    <div>
        <h2>Welcome, {}!</h2>
        <img src="{}" style="width: 200px; height: 200px;border-radius: 50%;">
    </div>
    '''
    welcome_back = '''
    <div>
        <h2>Welcome back, {}!</h2>
        <p>I remember you my friend :)</p>
        <img src="{}" style="width: 200px; height: 200px;border-radius: 50%;">
    </div>
    '''

    if old_user:
        return welcome_back.format(
            login_session['username'], login_session['picture'])

    return welcome.format(login_session['username'], login_session['picture'])


@auth.route('/gdisconnect/')
def gdisconnect():
    """Logout from Google Auth"""
    access_token = login_session.get('access_token')
    gplus_id = login_session.get('gplus_id')
    if gplus_id is None:
        print('Current user not connected.')
        return jsonify(error={'msg': 'Current user not connected.'}), 401

    # Revoke access of logged in user
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.\
        format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return jsonify(success={'msg': 'Successfully disconnected.'})

    return jsonify(error={
        'msg': 'Failed to revoke token for given user.'}), 400


@auth.route('/fbconnect', methods=['POST'])
@csrf.exempt
def fbconnect():
    """Handle login authentication and authorization with Facebook"""
    # Validate state token
    if request.args.get('state') != login_session.get('state'):
        print('Invalid state parameter.')
        return jsonify(error={'msg': 'Invalid state parameter.'}), 401

    # Obtain authorization token
    token = request.data.decode()

    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&client_id={}&client_secret={}' \
          '&fb_exchange_token={}'.format(APP_ID, APP_SECRET, token)
    result = requests.get(url).json()

    # Get access token from response
    access_token = result.get('access_token')

    # Verify if the user already connected
    if login_session.get('access_token') is not None:
        # Update the access_token in login_session
        # to avoid error when signing out :)
        login_session['access_token'] = access_token
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Use token to get user info from API
    url = 'https://graph.facebook.com/v2.8/me?access_token={}' \
          '&fields=name,id,email'.format(access_token)
    data = requests.get(url).json()

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = access_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token={}' \
          '&redirect=0&height=200&width=200'.format(access_token)
    data = requests.get(url).json()
    login_session['picture'] = data["data"]["url"]

    # Create a new user if it doesn't exist
    old_user = False  # Track if user logged in before
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        # Create a new user
        user_id = create_user(login_session)
    else:
        old_user = True  # User in database so welcome back!
    login_session['user_id'] = user_id

    flash("You are now logged in as {}".format(login_session['username']))

    welcome = '''
    <div>
        <h2>Welcome, {}!</h2>
        <img src="{}" style="width: 200px; height: 200px;border-radius: 50%;">
    </div>
    '''
    welcome_back = '''
    <div>
        <h2>Welcome back, {}!</h2>
        <p>I remember you my friend :)</p>
        <img src="{}" style="width: 200px; height: 200px;border-radius: 50%;">
    </div>
    '''
    if old_user:
        return welcome_back.format(
            login_session['username'], login_session['picture'])

    return welcome.format(login_session['username'], login_session['picture'])


@auth.route('/fbdisconnect/')
def fbdisconnect():
    """Logout from Facebook Auth"""
    facebook_id = login_session.get('facebook_id')

    # The access token must me included to successfully logout
    access_token = login_session.get('access_token')
    if facebook_id is None:
        print('Current user not connected.')
        return jsonify(error={'msg': 'Current user not connected.'}), 401

    url = 'https://graph.facebook.com/{}/permissions?access_token={}'\
        .format(facebook_id, access_token)
    result = requests.delete(url)
    print('result by requests ', result.json())

    del login_session['facebook_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    return jsonify(success={'msg': 'Successfully disconnected.'}), 200


@auth.route('/disconnect')
def disconnect():
    """Logout from any oauth provider"""
    if 'provider' in login_session:
        if login_session.get('provider') == 'google':
            gdisconnect()
        if login_session.get('provider') == 'facebook':
            fbdisconnect()
        try:
            del login_session['username']
            del login_session['access_token']
            del login_session['user_id']
            del login_session['email']
            del login_session['picture']
        except KeyError:
            pass

        flash("You have successfully been logged out.")
        return redirect(url_for('field.index'))

    flash("You were not logged in!")
    return redirect(url_for('field.index'))
