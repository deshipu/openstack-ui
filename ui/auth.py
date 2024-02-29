import openstack
from keystoneauth1.identity import v3
from keystoneauth1.token_endpoint import Token
from keystoneauth1.session import Session
import keystoneauth1.exceptions
import functools
import flask


AUTH_URL="http://192.168.100.185:5000/v3"


def try_login(username, password):
    auth = v3.Password(
        auth_url = AUTH_URL,
        username=username,
        password=password,
        user_domain_id='default',
        project_domain_id='default',
        project_name='admin',
    )
    session = Session(auth=auth)
    try:
        token = auth.get_token(session)
    except keystoneauth1.exceptions.http.Unauthorized:
        flask.flash("wrong credentials")
        return False
    flask.session['username'] = username
    flask.session['token'] = token
    return True


def conn(project_id=None):
    token = flask.session.get('token')
    auth = v3.Token(
        auth_url=AUTH_URL,
        token=token,
        project_domain_id='default',
        project_id=project_id,
    )
    session = Session(auth=auth)
    return openstack.connection.Connection(
        session=session,
        app_name='ui',
        app_version='1.0',
    )
