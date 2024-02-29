import flask
import auth
import time
import requests

bp = flask.Blueprint(
    'dashboard',
    __name__,
    url_prefix='/dashboard',
    static_folder='static',
    template_folder='templates',
)

@bp.before_request
def redirect_to_login():
    if flask.session.get('username') is None:
        return flask.redirect(flask.url_for('login'))

@bp.route('/')
def projects():
    conn = auth.conn()
    projects = conn.identity.projects()
    return flask.render_template("projects.html", projects=projects)

@bp.route('/<project_id>/')
def project(project_id):
    conn = auth.conn(project_id)
    project = conn.identity.get_project(project)
    return flask.render_template("project.html", project=project)

@bp.route('/<project_id>/instances')
def instances(project_id):
    conn = auth.conn(project_id)
    instances = conn.compute.servers()
    def gen():
        for i in instances:
            yield i
            time.sleep(2)
    auth_headers = {
        'X-Auth-Token': flask.session['token'],
    }
    resp = requests.get(conn.compute.get_endpoint() + '/servers',
                        headers=auth_headers)
    print(resp.content)
    return flask.stream_template("instances.html", instances=gen())
