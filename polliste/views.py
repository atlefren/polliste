from flask import render_template, g, request, session, redirect, url_for
from webassets.loaders import PythonLoader
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, ROLE_USER

def setup_views(app):

    open_id = OpenID(app, 'tmp')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    assets = Environment(app)
    bundles = PythonLoader('assetbundle').load_bundles()
    for name, bundle in bundles.iteritems():
        assets.register(name, bundle)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    @app.before_request
    def before_request():
        print current_user
        g.user = current_user


    @app.route('/')
    def index():
        return render_template("base.html")

    @app.route('/login', methods = ['GET', 'POST'])
    @open_id.loginhandler
    def login():
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))

        if request.method == 'POST':
            print "!!"
            session['remember_me'] = True
            return open_id.try_login("https://www.google.com/accounts/o8/id", ask_for = ['nickname', 'email', 'fullname']) #
        else:
            return render_template('login.html')

    @open_id.after_login
    def after_login(resp):
        if resp.email is None or resp.email == "":
            redirect(url_for('login'))

        user = User.query.filter_by(email = resp.email).first()

        if user is None:
            username = resp.nickname
            if username is None or username == "":
                username = resp.email.split('@')[0]
            user = User(username = username, email = resp.email, name = resp.fullname, role = ROLE_USER)
            app.db_session.add(user)
            app.db_session.commit()
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember = remember_me)
        return redirect(request.args.get('next') or url_for('index'))


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))