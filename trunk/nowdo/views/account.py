# coding=utf-8
"""
created by SL on 14-3-7
"""
import datetime
from flask import request, session, url_for, Blueprint, render_template, redirect, jsonify
from flask.ext.login import current_user, login_user, current_app, logout_user
from flask.ext.babel import gettext as _
from sqlalchemy.sql.expression import or_
from nowdo.config import setting
from nowdo.controls.follows import Follow
from nowdo.controls.account import Account
from nowdo.forms.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from nowdo.utils import cas_client, memcache_tool
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm
from nowdo.utils.string_utils import get_random_key

__author__ = 'SL'

account_bp = Blueprint('account', __name__, template_folder="templates/account")


@account_bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    res = ajax_response()
    with session_cm() as account_session:
        if not user_id and not email:
            res.update({
                'status': 'fail',
                'info': 'user id or email required'
            })
            return jsonify(res)
        user = None
        if user_id:
            user = account_session.query(Account).get(user_id)
        if email:
            user = account_session.query(Account).filter(Account.email == email).first()
        if not user:
            res.update({
                'status': 'fail',
                'info': u'用户不存在'
            })
            return jsonify(res)

        followed = False
        if current_user.is_authenticated():
            followed = current_user.followed(user.id) is not None
        res.update({
            'data': {
                'user_id': str(user.id),
                'avatar_url': user.avatar_url(50),
                'nickname': user.nickname,
                'followed': followed
            }
        })
        return jsonify(res)

@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next')

    context = {
        'next': request.args.get('next'),
    }

    if current_user.is_authenticated():
        # return redirect(next_url or url_for('frontend.index'))
        return redirect(next_url or request.url)

    if setting.CAS_ENABLE:
        session["next_url"] = next_url
        redirect_url = request.url_root.rstrip('/') + url_for('account.cas_auth')
        return redirect(cas_client.login_url(setting.CAS_SERVER_URL, redirect_url))

    if request.method == 'POST':
        login_form = LoginForm(request.form)
        if login_form.validate_on_submit():
            return validate_user(email=login_form.email.data,
                                 name=login_form.email.data,
                                 next_url=request.args.get('next'))
        context.update(form=login_form)
        return render_template('account/login.html', **context)
    else:
        context.update(form=LoginForm())
        return render_template('account/login.html', **context)


@account_bp.route('/ajax_login', methods=['POST'])
def ajax_login():
    res = ajax_response()

    email = request.form.get('email')
    password = request.form.get('password')

    with session_cm() as account_session:
        user = account_session.query(Account).filter(
            or_(Account.email == email, Account.name == email)).first()
        if not user:
            res.update({
                'status': 'fail',
                'info': u'用户不存在'
            })
            return jsonify(res)
        if not user.check_password(password):
            res.update({
                'status': 'fail',
                'info': u'密码不正确'
            })
            return jsonify(res)

        if user.is_active():
            login_user(user)
            res.update(data={
                'is_authenticated': True,
                'nickname': user.nickname
            })
            return jsonify(res)
        else:
            user.send_register_mail(host_url=request.host_url)
            res.update({
                'status': 'fail',
                'info': 'not_active',
                'data': {
                    'email': user.email,
                    'resend_url': user.get_activation_email_resend_url()
                }
            })
            return jsonify(res)


# CAS ticket验证接口
@account_bp.route('/passport', methods=['POST', 'GET'])
def cas_auth():
    if request.method == 'POST':
        logout_request = request.form.get('logoutRequest', None)
        if logout_request:
            ticket = cas_client.get_logout_request_ticket(logout_request)
            current_app.logger.info("CAS LOGOUT ! ticket = %s , time = %s" % (
                ticket, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            current_app.session_interface.del_ticket_session_mapping(ticket)
        return redirect(url_for('frontend.index'))
    else:
        ticket = request.args.get('ticket', None)
        next_url = session.get("next_url")
        redirect_url = request.url_root.rstrip('/') + url_for('account.cas_auth')
        ticket_status, u_id = cas_client.get_ticket_status(setting.CAS_SERVER_URL, redirect_url, ticket)
        if ticket_status == -1 or ticket_status == 0:
            # app.logger.info("Ticket does not validate")
            print 'ticket does not validate'
            return redirect(url_for('frontend.index'))
        else:
            # app.logger.info("Ticket validates OK")
            current_app.session_interface.set_cas_ticket_to_session_mapping(current_app, session, ticket)
            return validate_user(email=u_id, name=u_id, next_url=next_url)


@account_bp.route('/ajax_forget_password', methods=['POST'])
def ajax_forget_password():
    res = ajax_response()
    email = request.form.get('email')
    if not email:
        res.update({
            'status': 'fail',
            'info': u'邮箱不能为空'
        })
        return jsonify(res)
    # send email to reset password
    with session_cm() as db_session:
        user = db_session.query(Account).filter_by(email=email).first()
        if not user:
            res.update({
                'status': 'fail',
                'info': u'用户不存在'
            })
            return jsonify(res)

        user.i_lost_pw(host_url=request.host_url)
        resend_email_url = user.get_reset_pwd_email_resend_url()
        res.update(data={
            'resend_email_url': resend_email_url,
            'email': email
        })
        return jsonify(res)


@account_bp.route('/forget_password', methods=['POST'])
def forget_password():
    forgot_form = ForgotPasswordForm(request.form)
    context = {
        'form': forgot_form
    }
    if request.method == 'POST':
        if forgot_form.validate_on_submit():
            # send email to reset password
            with session_cm() as db_session:
                user = db_session.query(Account).filter_by(email=forgot_form.email.data).one()
                user.i_lost_pw(host_url=request.host_url)

                resend_email_url = user.get_reset_pwd_email_resend_url()
                context.update(resend_email_url=resend_email_url,
                               category='success',
                               info=u'重置密码链接已经发送到您的邮箱：%s' % user.email)
                return render_template('account/operation_result.html', **context)
    return render_template('account/forgot_password.html', **context)


@account_bp.route('/reset_pw', methods=['GET', 'POST'])
def reset_pw():
    reset_pw_form = ResetPasswordForm(request.form)
    key = request.args.get('key') or reset_pw_form.key.data
    user_id = request.args.get('id') or reset_pw_form.id.data
    email = check_pw_code(key) or reset_pw_form.email.data
    reset_pw_form.email.data = email
    context = {}
    with session_cm() as db_session:
        user = db_session.query(Account).get(user_id)
        if not user:
            context.update({
                'info': _(u'用户不存在！'),
                'category': 'danger'
            })
            return render_template('account/operation_result.html', **context)
        if user.email == email:
            if reset_pw_form.validate_on_submit():
                user.set_password(reset_pw_form.password.data, key=key)
                db_session.commit()
                context.update({
                    'info': _(u'密码修改成功！'),
                    'category': 'success',
                    'login_url': url_for('account.login')
                })
                return render_template('account/operation_result.html', **context)
                #将链接参数传至页面
            reset_pw_form.id.data = user_id
            reset_pw_form.key.data = key
            context = {
                'form': reset_pw_form
            }
            return render_template('account/rest_pw.html', **context)
        else:
            context.update({
                'info': _(u'链接已经失效，请尝试重新找回密码！'),
                'category': 'info',
                'reset_pwd_url': url_for('account.forget_password')
            })
            return render_template('account/operation_result.html', **context)


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form)
    context = {
        'form': register_form
    }
    if request.method == 'POST':
        if register_form.validate_on_submit():
            with session_cm() as db_session:
                user = Account()
                user.email = register_form.email.data  # .split('@')[0]
                user.name = register_form.email.data  # .split('@')[0]
                user.display_name = register_form.nickname.data
                user.set_password(register_form.password.data)
                # 初始注册用户默认不激活
                user.active = False
                db_session.add(user)
                db_session.commit()
                official_account = db_session.query(Account).filter(Account.email == setting.OFFICIAL_ACCOUNT).first()
                if official_account:
                    Follow.follow(user, target_user=official_account)
                # 发送激活邮件
                user.send_register_mail(host_url=request.host_url)
                context = {
                    'email': user.email,
                    'category': 'success',
                    'resend_email_url': user.get_activation_email_resend_url()
                }
                return render_template('account/operation_result.html', **context)
    return render_template('account/register.html', **context)


@account_bp.route('/ajax_register', methods=['POST'])
def ajax_register():
    res = ajax_response()
    email = request.form.get('email')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    with session_cm() as account_session:
        user = account_session.query(Account).filter_by(email=email).first()
        if user:
            res.update({
                'status': 'fail',
                'info': u'用户已经存在'
            })
            return jsonify(res)

        user = Account()
        user.email = email  # .split('@')[0]
        user.name = email  # .split('@')[0]
        user.display_name = nickname
        user.set_password(password)
        # 初始注册用户默认不激活
        user.active = False
        account_session.add(user)
        account_session.commit()
        official_account = account_session.query(Account).filter(Account.email == setting.OFFICIAL_ACCOUNT).first()
        if official_account:
            Follow.follow(user, target_user=official_account)
        # 发送激活邮件
        user.send_register_mail(host_url=request.host_url)
        res.update({
            'data': {
                'email': user.email,
                'resend_url': user.get_activation_email_resend_url()
            }
        })
        return jsonify(res)


@account_bp.route('/resend_email')
def resend_email():
    email = request.args.get('email')
    op_type = request.args.get('type')
    context = {
        'email': email,
        'category': 'success'
    }
    if not email:
        context.update(category='danger', info=_(u'邮件发送失败'))
        return render_template('account/operation_result.html', **context)
    with session_cm() as db_session:
        user = db_session.query(Account).filter(Account.email == email).first()
        if user:
            if op_type == 'activate':
                user.send_register_mail(host_url=request.host_url)
            if op_type == 'reset_pwd':
                user.i_lost_pw(host_url=request.host_url)
            context.update(info=_(u'邮件已经成功重新发送到您的邮箱： %s' %email),
                           login_url=url_for('account.login'))

        return render_template("account/operation_result.html", **context)


@account_bp.route('/activate')
def account_activate():
    key = request.args.get('key')
    user_id = request.args.get('id')
    with session_cm() as db_session:
        user = db_session.query(Account).get(user_id)
        # 判断 帐号是否已经激活
        if user.is_active():
            context = {
                'category': 'success',
                'info': _(u'您的帐号已经激活，感谢您加入脑洞协作翻译平台！'),
                'login_url': url_for('account.login')
            }
        else:
            if user.email == check_pw_code(key):
                activate(db_session, key)
                db_session.commit()
                context = {
                    'category': 'success',
                    'info': _(u'您的帐号激活成功，感谢您加入脑洞协作翻译平台！'),
                    'login_url': url_for('account.login')
                }
            else:
                context = {
                    'category': 'info',
                    'info': _(u'激活链接已失效，请尝试登录重新获取激活邮件！'),
                    'resend_email_url': user.get_activation_email_resend_url()
                }
        return render_template('account/operation_result.html', **context)


@account_bp.route('/logout')
def logout():
    next_url = request.args.get('next')
    if current_user.is_authenticated():
        username = current_user.name
        logout_user()

        # Remove session keys set by Flask-Principal
        # for key in ('identity.name', 'identity.auth_type'):
        #     session.pop(key, None)

        # Tell Flask-Principal the user is anonymous
        # identity_changed.send(app._get_current_object(),
        #                       identity=AnonymousIdentity())

        if setting.CAS_ENABLE:
            current_app.logger.warn("user:" + username + " has logout")
            return redirect(cas_client.logout_url(setting.CAS_SERVER_URL, next_url or request.url_root))
    return redirect(next_url or url_for("frontend.frontend"))


@account_bp.route('/ajax_logout')
def ajax_logout():
    res = ajax_response()
    if current_user.is_authenticated():
        logout_user()
    return jsonify(res)


@account_bp.route('/cooperation_center')
def cooperation_center():
    pass


class EmailNotExist(Exception):
    pass


class BadPasswordCode(Exception):
    """
    修改密码验证码错误
    """
    pass


def email_exists(db_session, email):
    return db_session.query(Account).filter(Account.email == email).count() >= 0


def i_lost_pw(db_session, email):
    if not email_exists(db_session, email):
        raise EmailNotExist()
    key = get_random_key()
    memcache_tool.memcache_set(key, email)
    return key


def check_pw_code(pw_code):
    return memcache_tool.memcache_get(pw_code)


def change_password(db_session, pw_code, new_password):
    code = check_pw_code(pw_code)
    if not code:
        raise BadPasswordCode()
    account = db_session.query(Account).filter(Account.email == code).one()
    account.set_password(new_password)


def activate(db_session, pw_code):
    code = check_pw_code(pw_code)
    if not code:
        raise BadPasswordCode()
    account = db_session.query(Account).filter(Account.email == code).one()
    account.set_active(True)
    memcache_tool.memcache_set(pw_code, None)


def validate_user(email, name, next_url=None):
    with session_cm() as db_session:
        user = db_session.query(Account).filter(or_(Account.email == email, Account.name == name)).one()

        # Confirm whether the user is activated
        if user.is_active():
            # Keep the user info in the session using Flask-Login
            login_user(user)
            # Tell Flask-Principal the identity changed
            # identity_changed.send(app._get_current_object(), identity=Identity(user.id))
            return redirect(next_url or url_for('frontend.index'))
        else:
            user.send_register_mail(host_url=request.host_url, next=next_url)
            context = {
                'category': 'info',
                'info': u'您的账号尚未激活，激活邮件已经发送到您的邮箱: %s' % email,
                'email': email,
                'resend_email_url': user.get_activation_email_resend_url()
            }
            return render_template('account/operation_result.html', **context)