# coding=utf-8
"""
created by SL on 14-3-26

交谈、邮件
"""
from flask.ext.login import current_user
import sqlalchemy as SA
from sqlalchemy.sql.expression import or_, and_
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from nowdo.controls.base import Base, id_generate
from nowdo.controls.account import Account
from nowdo.utils.session import session_cm

__author__ = 'SL'


class Dialogue(Base):
    """
      交谈表
    """
    __tablename__ = 'dialogue'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    first_speaker_id = SA.Column(BIGINT(unsigned=True), nullable=False, index=True)
    second_speaker_id = SA.Column(BIGINT(unsigned=True), nullable=False, index=True)
    latest_mail_content = SA.Column(SA.TEXT)
    mail_list = relationship("Mail", backref='dialogue')

    def target_user(self):
        target_id = self.first_speaker_id if current_user.id != self.first_speaker_id else self.second_speaker_id
        with session_cm() as account_session:
            return account_session.query(Account).get(target_id)

    def read(self):
        self.session.query(Mail)\
            .filter(Mail.receiver_id == current_user.id,
                    Mail.dialogue_id == self.id)\
            .update({Mail.is_read: True})
        self.session.commit()

    @property
    def is_all_read(self):
        return self.session.query(Mail).filter(Mail.dialogue_id == self.id,
                                               Mail.receiver_id == current_user.id,
                                               Mail.is_read == False).count() <= 0

    @staticmethod
    def my_dialogues(db_session, user):
        dialogues = db_session.query(Dialogue).filter(or_(Dialogue.first_speaker_id == user.id,
                                                          Dialogue.second_speaker_id == user.id)).all()
        return dialogues

    @staticmethod
    def get_dialogue(db_session, user_id, target_user_id):
        dialogue = db_session.query(Dialogue) \
            .filter(or_(and_(Dialogue.first_speaker_id == user_id, Dialogue.second_speaker_id == target_user_id),
                        and_(Dialogue.first_speaker_id == target_user_id, Dialogue.second_speaker_id == user_id))) \
            .first()
        return dialogue

    @staticmethod
    def update_dialogue(db_session, speaker_one_id, speaker_tow_id, latest_mail):
        dialogue = Dialogue.get_dialogue(db_session, speaker_one_id, speaker_tow_id)
        if not dialogue:
            dialogue = Dialogue(first_speaker_id=speaker_one_id,
                                second_speaker_id=speaker_tow_id)
        dialogue.latest_mail_content = latest_mail.content
        db_session.add(dialogue)
        return dialogue


class Mail(Base):
    __tablename__ = 'mail'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    dialogue_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('dialogue.id'))
    sender_id = SA.Column(BIGINT(unsigned=True), nullable=False, index=True)
    receiver_id = SA.Column(BIGINT(unsigned=True), nullable=False, index=True)
    content = SA.Column(SA.TEXT, nullable=False)
    is_read = SA.Column(SA.Boolean, default=False, nullable=False)

    @staticmethod
    def send(db_session, sender_id, receiver_id, content):
        mail = Mail(sender_id=sender_id,
                    receiver_id=receiver_id,
                    content=content)
        dialogue = Dialogue.update_dialogue(db_session, sender_id, receiver_id, mail)
        mail.dialogue = dialogue
        db_session.add(mail)
        db_session.commit()
        return dialogue

    @staticmethod
    def mail_detail_list(sender_id, receiver_id):
        with session_cm() as db_session:
            return db_session.query(Mail)\
                .filter(or_(and_(Mail.receiver_id == receiver_id, Mail.sender_id == sender_id),
                            and_(Mail.receiver_id == sender_id, Mail.sender_id == receiver_id)))\
                .order_by(Mail.created_date.desc()).all()