# coding=utf-8

import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from celery.exceptions import MaxRetriesExceededError
from nowdo.config.celeryconfig import celery
from nowdo.utils.nowdo_logger import nowdo_celery_logger as logger


@celery.task(ignore_result=True)
def send_mail(subject,
              text,
              to=[],     # 收件人
              cc=[],     # 抄送人
              bcc=[],    # 密送人
              files=None,
              name='smtp.exmail.qq.com',
              account='noreply@xingcloud.com',
              password='xingcloudml2012'):
    u"""发送邮件的后台任务，可以单独调用
    """
    assert type(to) == list
    assert type(cc) == list
    assert type(bcc) == list

    logger.debug("to: %s, subject: %s" % (to, subject))

    fro = '脑洞<noreply@xingcloud.com>'
    real_to = to
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    if cc:
        msg['Cc'] = COMMASPACE.join(cc)
        real_to += cc
    if bcc:
        msg['Bcc'] = COMMASPACE.join(bcc)
        real_to += bcc
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'html', _charset='UTF-8'))

#    for file in files:
#        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
#        part.set_payload(open(file, 'rb'.read()))
#        encoders.encode_base64(part)
#        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
#        msg.attach(part)

    try:
        auth_info = {'name': name, 'user': account, 'passwd': password}
        smtp = smtplib.SMTP(auth_info['name'], 25, timeout=20)
        smtp.login(auth_info['user'], auth_info['passwd'])
        smtp.sendmail(fro, real_to, msg.as_string())
        smtp.quit()
    except Exception:
        logger.error(traceback.format_exc())
        try:
            logger.warn("retry send mail...")
            send_mail.retry(countdown=5, max_retries=20)
        except MaxRetriesExceededError:
            logger.error("max retry times exceeded!")


if __name__ == "__main__":
    #send_mail("Test Subject to", "Test Message", to=["zouyingjun@xingcloud.com", "hehuilin@xingcloud.com"])
    #send_mail("Test Subject cc", "Test Message", to=["zouyingjun@xingcloud.com"], cc=["hehuilin@xingcloud.com"])
    #send_mail("Test Subject bcc", "Test Message", to=["zouyingjun@xingcloud.com"], cc=["sunlei@xingcloud.com"], bcc=["hehuilin@xingcloud.com"])
    send_mail("Test Subject bcc2", "Test Message", bcc=["zouyingjun@xingcloud.com", "sunlei@xingcloud.com", "hehuilin@xingcloud.com"])