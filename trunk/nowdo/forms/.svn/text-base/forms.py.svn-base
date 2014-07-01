# coding=utf-8
"""
Created on Jan 9, 2012

@author: zyj
"""

from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user

try:
    from flask.ext.wtf import TextField, HiddenField, BooleanField, SelectMultipleField, IntegerField, SelectField,\
        PasswordField, Form, TextAreaField, FileField
except:
    from wtforms import TextField, HiddenField, BooleanField, SelectMultipleField, IntegerField, SelectField,\
        PasswordField, TextAreaField, FileField
    from flask_wtf import Form
from sqlalchemy import or_
from wtforms.validators import ValidationError, Required, Length, Regexp, Email, NumberRange

from nowdo.controls.account import Account
from nowdo.controls.group import Group
from nowdo.utils.languages import supported_languages
from nowdo.utils.session import session_cm


class RequiredIf(object):
    # a validator which makes a field required if
    # the condition is True

    def __init__(self, condition, message=None):
        self.condition = condition
        if not message:
            message = _(u'必须填写')
        self.message = message

    def __call__(self, form, field):
        if self.condition(form) and (not field.data or isinstance(field.data, basestring) and not field.data.strip()):
            raise ValidationError(self.message)


class LoginForm(Form):
    email = TextField(_(u'邮箱或帐号'), validators=[Required(message=_(u'邮箱或帐号不能为空'))],
                      description=_(u'邮箱/帐号'))
    password = PasswordField(_(u'密码'), validators=[Required(message=_(u'密码不能为空'))], description=_(u'密码'))

    def validate_email(self, field):
        with session_cm() as session:
            user = session.query(Account).filter(or_(Account.email == field.data, Account.name == field.data)).first()
            if not user:
                raise ValidationError(_(u'邮箱或帐号不存在'))

    def validate_password(self, field):
        with session_cm() as session:
            user = session.query(Account).filter(
                or_(Account.email == self.email.data, Account.name == self.email.data)).first()
            if user and not user.check_password(field.data):
                raise ValidationError(_(u'密码不正确'))


class RegisterForm(Form):
    email = TextField(_(u'邮箱'), validators=[Required(message=_(u'邮箱不能为空')), Email(message=_(u'邮箱格式不正确'))],
                      description=_(u'邮箱'))
    password = PasswordField(_(u'密码'), validators=[Required(message=_(u'密码不能为空')),
                                                   Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))],
                             description=_(u'密码'))
    nickname = TextField(_(u'昵称'), description=_(u'昵称'))

    def validate_email(form, field):
        with session_cm() as session:
            user = session.query(Account).filter_by(email=field.data).first()
            if user:
                raise ValidationError(_(u'邮箱已存在'))


def validate_password_length(form, field):
    length_validate = Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))
    if field.data != u'':
        length_validate(form, field)


class UserInfoForm(Form):
    name = TextField(_(u'帐号'))
    email = TextField(_(u'邮箱'), validators=[
        Email(message=_(u'邮箱格式不正确'))
    ])

    old_password = PasswordField(_(u'现有密码'))

    password = PasswordField(_(u'新密码'))

    confirm_password = PasswordField(_(u'确认密码'))

    def validate_old_password(form, field):
        if not field.data:
            raise ValidationError(_(u'现有密码不能为空'))

        if field.data and not current_user.check_password(field.data):
            raise ValidationError(_(u'现有密码不正确'))

    def validate_password(form, field):
        if form.old_password.data and not field.data:
            raise ValidationError(_(u'新密码不能为空'))

        if form.old_password.data and field.data:
            length_validate = Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))
            length_validate(form, field)

    def validate_confirm_password(form, field):
        if form.old_password.data and \
                form.password.data and \
                not field.data:
            raise ValidationError(_(u'确认密码不能为空'))

        if form.password.data and field.data and \
                not field.data == form.password.data:
            raise ValidationError(_(u'两次密码不一致'))


class ResetPasswordForm(Form):
    email = TextField(_(u'邮箱'), validators=[Email(message=_(u'邮箱格式不正确'))], description=_(u'邮箱'))

    id = HiddenField(_(u'ID'))
    key = HiddenField(_(u'KEY'))

    password = PasswordField(_(u'新密码'), description=_(u'新密码'))

    confirm_password = PasswordField(_(u'确认密码'), description=_(u'确认密码'))

    def validate_password(self, field):
        if field.data:
            length_validate = Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))
            length_validate(self, field)
        else:
            raise ValidationError(_(u'新密码不能为空'))

    def validate_confirm_password(self, field):
        if self.password.data and \
                not field.data:
            raise ValidationError(_(u'确认密码不能为空'))

        if self.password.data and field.data and \
                not field.data == self.password.data:
            raise ValidationError(_(u'两次密码不一致'))


class ForgotPasswordForm(Form):
    email = TextField(_(u'注册邮箱'), validators=[Required(message=_(u'邮箱不能为空')), Email(message=_(u'邮箱格式不正确'))],
                      description=_(u'注册邮箱'))

    def validate_email(form, field):
        with session_cm() as session:
            user = session.query(Account).filter_by(email=field.data).first()
            if not user:
                raise ValidationError(_(u'邮箱不存在'))


class FreeTrialForm(Form):
    trial_name = TextField(_(u'您的名字'))
    trial_qq = TextField(_(u'QQ号码'), validators=[
        Required(message=_(u'请填写您的QQ号码')), Length(max=50, message=_(u'不能超过50个字符'))])
    trial_email = TextField(_(u'您的邮箱'),
                            validators=[
                                Required(message=_(u'请填写您的邮箱')),
                                Email(message=_(u'邮箱格式不正确'))])

    src_domain = TextField(
        _(u'您的网站'),
        validators=[
            Required(message=_(u'请填写您的域名')),
            Regexp(r'^(https?:\/\/)*[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*((\.[a-zA-Z0-9_-]{2,3}){1,2})\/?$',
                   message=_(u'域名格式不正确')),
        ])

    src_lang = HiddenField(_(u'现网站语言'), validators=[Required(message=_(u'请选择现网站语言'))])
    tar_lang = HiddenField(_(u'需要翻译语言'), validators=[Required(message=_(u'请选择目标语言'))])

    def validate_trial_email(form, field):
        with session_cm() as session:
            if session.query(Account).filter_by(email=field.data).first():
                raise ValidationError(_(u'邮箱已经存在'))


class CreateGroupForm(Form):
    group_name = TextField(_(u'小组名称'), validators=[Required(message=_(u'小组名称不能为空'))],
                           description=_(u'小组名称'))
    group_description = TextAreaField(_(u'小组描述'), validators=[Required(message=_(u'小组描述不能为空'))],
                                      description=_(u'小组描述'))
    group_tags = TextField(_(u'小组标签'), validators=[Required(message=_(u'小组标签不能为空'))],
                           description=_(u'小组标签'))

    def validate_group_name(self, field):
        with session_cm() as session:
            group = session.query(Group).filter(Group.group_name == field.data).first()
            if group:
                raise ValidationError(_(u'该小组已经存在'))


class EditGroupForm(CreateGroupForm):
    id = HiddenField()

    def validate_group_name(self, field):
        with session_cm() as session:
            group = session.query(Group).filter(Group.group_name == field.data,
                                                           Group.id != self.id.data).first()
            if group:
                raise ValidationError(_(u'该小组已经存在'))


class CreateTaskForm(Form):
    task_name = TextField(_(u'主题名称'),
                          validators=[Required(message=_(u'主题名称不能为空'))],
                          description=_(u'主题名称'))
    task_description = TextAreaField(_(u'主题描述'),
                                     # validators=[Required(message=_(u'任务描述不能为空'))],
                                     description=_(u'主题描述'))

    reserved_words = TextField(_(u'保留词'), description=_(u'保留词'))
    status = BooleanField(_(u'立即开启'), description=_(u'立即开启'))

    max_translate_count = IntegerField(_(u'最大翻译结果数'), default=50,
                                       description=_(u'每个词条所允许的最多翻译结果数'),
                                       validators=[NumberRange(min=1, max=100, message=u'最大翻译结果数为1-100的数字')])
    src_lang = SelectField(_(u'源语言'),
                           description=_(u'源语言'),
                           choices=supported_languages().items())
    tar_lang = SelectField(_(u'目标语言'),
                           description=_(u'目标语言'),
                           choices=supported_languages().items())
    # glossary_table = SelectField(_(u'术语表(可选)'),
    #                              description=_(u'术语表'))
    task_file = FileField(_(u'文件'),
                          description=_(u'要翻译的文件'))

    tags = TextField(_(u'标签'), validators=[Required(message=_(u'标签不能为空'))],
                     description=_(u'标签'))

    task_content = TextAreaField(_(u'主题内容'), description=_(u'主题内容'))

    input_mode = HiddenField()

    def validate_task_content(self, field):
        if self.input_mode.data == 'text' and not field.data:
            raise ValidationError(u'主题内容不能为空')


class CreateTopicForm(Form):
    title = TextField(_(u'标题'),
                      validators=[Required(message=_(u'标题不能为空'))],
                      description=_(u'标题'))
    content = TextAreaField(_(u'话题内容'),
                            validators=[Required(message=_(u'话题内容不能为空'))],
                            description=_(u'话题内容'))


class CreateCommentForm(Form):
    # comment_id = HiddenField()
    content = TextAreaField(_(u'回复内容'),
                            validators=[Required(message=_(u'回复内容不能为空'))],
                            description=_(u'回复内容'))

    # def validate_comment_id(self, field):
    #     if field.data:
    #         with session_cm() as db_session:
    #             if not db_session.query(TopicComment).get(field.data):
    #                 raise ValidationError(_(u'回复的评论不存在'))


class ProfileForm(Form):
    # comment_id = HiddenField()
    display_name = TextField(_(u'昵称'),
                             validators=[Required(message=_(u'昵称不能为空')),
                                         Length(min=2, max=10, message=_(u'昵称必须是2-10个字符'))],
                             description=_(u'昵称'))


class WriteMailForm(Form):
    receiver_id = HiddenField()
    mail_content = TextAreaField(_(u'邮件内容'),
                                 validators=[Required(message=_(u'邮件内容不能为空'))],
                                 description=_(u'邮件内容'))


class GlossaryTableForm(Form):
    name = TextField(_(u'名称'),
                     validators=[Required(message=_(u'名称不能为空')),
                                 Length(min=2, max=100, message=_(u'名称长度必须介于2-100之间'))],
                     description=_(u'名称'))
    source_language = SelectField(_(u'源语言'),
                                  description=_(u'源语言'),
                                  choices=supported_languages().items())
    target_language = SelectField(_(u'目标语言'),
                                  description=_(u'目标语言'),
                                  choices=supported_languages().items())


class GlossaryForm(Form):
    source = TextAreaField(_(u'源词'),
                           validators=[Required(message=_(u'源词不能为空'))],
                           description=_(u'源词'))
    target = TextAreaField(_(u'目标词'),
                           validators=[Required(message=_(u'目标词不能为空'))],
                           description=_(u'目标词'))


class CheckingGlossaryForm(GlossaryForm):
    glossary_table = SelectField(_(u'术语表'),
                                 choices=[],
                                 validators=[Required(message=_(u'请选择一个术语表'))],
                                 description=_(u'术语表'))


class CategoryForm(Form):
    name = TextField(_(u'类别名称'),
                     validators=[Required(message=_(u'类别名称不能为空'))],
                     description=_(u'类别名称'))


class SendRegInvitationForm(Form):
    email = TextField(_(u'邮箱'), validators=[Required(message=_(u'邮箱不能为空'))],
                      description=_(u'邮箱'))

    def validate_email(self, field):
        with session_cm() as session:
            user = session.query(Account).filter_by(email=field.data).first()
            if user:
                raise ValidationError(_(u'邮箱已存在'))