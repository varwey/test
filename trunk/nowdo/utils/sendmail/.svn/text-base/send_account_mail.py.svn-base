import os
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


def _get_template_path():
    sep = os.path.sep
    altsep = os.path.altsep or '\\'
    file_path = __file__
    if altsep in __file__:
        file_path = __file__.replace(altsep, sep)
    tpl_path_slice = file_path.split(sep)
    tpl_path_slice.pop()
    tpl_path_slice.append('email_templates')
    return '/'.join(tpl_path_slice)


loader = FileSystemLoader(_get_template_path())
env = Environment(loader=loader)


def get_activate_email_content(**kwargs):
    return env.get_template('activate_mail.html').render(**kwargs)


def get_lost_psd_email_content(**kwargs):
    return env.get_template('i_lost_pw_mail.html').render(**kwargs)


def get_trial_email_content(**kwargs):
    return env.get_template('trial_mail.html').render(**kwargs)


def get_free_trial_email_content(**kwargs):
    return env.get_template('free_trial_mail.html').render(**kwargs)


def get_free_trial_email_zh_content(**kwargs):
    return env.get_template('free_trial_mail_zh.html').render(**kwargs)


def get_free_trial_email_en_content(**kwargs):
    return env.get_template('free_trial_mail_en.html').render(**kwargs)


def get_trial_expire_email_content(**kwargs):
    return env.get_template('trial_expire_mail.html').render(**kwargs)


def get_business_info_email_content(**kwargs):
    return env.get_template('business_info_mail.html').render(**kwargs)


def get_bd_notice_email_content(**kwargs):
    return env.get_template('bd_notice_mail.html').render(**kwargs)


def get_apply_for_open_project_email_content(**kwargs):
    return env.get_template('apply_for_open_project.html').render(**kwargs)


def get_reg_invitation_content(**kwargs):
    return env.get_template('reg_invitation.html').render(**kwargs)


if __name__ == '__main__':
    kwargs = {
        'name': 'sunlei',
        'key': '123456',
        'id': '456789',
        'host_url': 'www.baidu.com'
    }
    print get_free_trial_email_content(**kwargs)

