# coding=utf-8
import hashlib
import logging
from logging import FileHandler
import urllib
from babel.support import Translations
import datetime
from nowdo.utils.htmltruncate import truncate as html_truncate_words
from flask import Flask, render_template
from flask.ext.babel import Babel
from flask.ext.login import current_user
import memcache
from nowdo.config import setting
from nowdo.controls.group import Group
from nowdo.extensions.memcache_session import MemcachedSessionInterface
from nowdo.forms.forms import LoginForm, RegisterForm
from nowdo.helpers import pull_current_group
from nowdo.utils import login_manager
from nowdo.utils.avatar import get_avatar_url
from nowdo.utils.date_utils import date_delta
from nowdo.utils.escape_utils import deal_topic_content, escape_unsafe_content, strip_images
from nowdo.utils.session import session_cm
from nowdo.views.account import account_bp
from nowdo.views.follow import follow_bp
from nowdo.views.frontend import frontend_bp
from nowdo.views.glossary import glossary_bp
from nowdo.views.group import group_bp
from nowdo.views.like import like_bp
from nowdo.views.mail import mail_bp
from nowdo.views.management import management_bp
from nowdo.views.notice import notice_bp
from nowdo.views.personal import personal_bp
from nowdo.views.search import search_bp
from nowdo.views.task import task_bp
from nowdo.views.translate import translate_bp
import views

__author__ = 'SL'

BLUEPRINTS = [
    (frontend_bp, ''),
    (account_bp, '/account'),
    (group_bp, '/group'),
    (task_bp, '/task'),
    (translate_bp, '/translate'),
    (personal_bp, '/personal'),
    (mail_bp, '/mail'),
    (follow_bp, '/follow'),
    (notice_bp, '/notice'),
    (like_bp, '/like'),
    (glossary_bp, '/glossary'),
    (search_bp, '/search'),
    (management_bp, '/management')
]


def create_app(blueprints=None):
    if blueprints is None:
        blueprints = BLUEPRINTS
    app = Flask(__name__)

    # config
    app.config.from_object(setting)

    configure_blueprints(app, blueprints)
    configure_logger(app)
    configure_login_manager(app)
    configure_i18n(app)
    configure_url_preprocessor(app)
    configure_context_processor(app)
    configure_template_filter(app)
    configure_memcache_session_interface(app)
    configure_error_handler(app)
    return app


def configure_blueprints(app, blueprints):
    # register blueprint
    if blueprints:
        for view, url_prefix in blueprints:
            app.register_blueprint(view, url_prefix=url_prefix)


def configure_login_manager(app):
    login_manager.init_app(app)


def configure_logger(app):
    format_str = '%(asctime)s %(levelname)s in %(pathname)s:%(lineno)d :\n%(message)s'
    formatter = logging.Formatter(format_str)
    debug_log = app.config['LOG_FILE']

    debug_file_handler = FileHandler(debug_log)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)


def configure_i18n(app):
    app.config['BABEL_DEFAULT_LOCALE'] = setting.DEFAULT_INIT_LOCALE

    def ugettext(self, message):
        missing = object()
        tmsg = self._catalog.get(unicode(message), missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.ugettext(message)
            return unicode(message)
        return tmsg

    Translations.ugettext = ugettext

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return setting.DEFAULT_INIT_LOCALE

    babel.list_translations()


def configure_url_preprocessor(app):
    @app.url_value_preprocessor
    def get_current_group(endpoint, values):
        pull_current_group(endpoint, values)


def configure_template_filter(app):
    @app.template_filter()
    def avatar(value, size=50):
        # construct the url
        return get_avatar_url(value, size)

    @app.template_filter()
    def delta(value):
        return date_delta(value)

    @app.template_filter()
    def escape_unsafe_tags(value):
        return escape_unsafe_content(value)
    
    @app.template_filter()
    def strip_img_tags(value):
        return strip_images(value)

    @app.template_filter()
    def html_truncate(value, target_len, ellipsis='...'):
        return html_truncate_words(value, target_len, ellipsis=ellipsis)


def configure_context_processor(app):

    @app.context_processor
    def inject_datetime():
        d = {
            'one_column': False,
            'today': datetime.datetime.today()
        }
        return d

    @app.context_processor
    def inject_layout():
        import random
        d = {
            'random': random.random(),
            'version': setting.VERSION
        }
        return d


def configure_error_handler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404


def configure_memcache_session_interface(app):
    '''store session with memcache'''
    client = memcache.Client(app.config['MEMCACHED_MACHINES'])
    app.session_interface = MemcachedSessionInterface(client)

application = create_app()