from app.models import session, User, MOOC, Field


# User Helper Functions
def create_user(login_session):
    """Create a new user when logged in by oauth2 and Return user id"""
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    """Return a user from database"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """Return a user id from database"""
    user = session.query(User).filter_by(email=email).first()

    # Check if user doesn't exist
    if user is None:
        return None

    return user.id
