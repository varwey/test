# -*- coding: utf-8 -*-
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate

__author__ = 'lhfu'


class Image(Base):
    __tablename__ = 'image'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    image_url = SA.Column(SA.Text, nullable=False)

    #图片在任务中的位置
    position = SA.Column(BIGINT(unsigned=True), nullable=False)

    #: 关联任务id
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'), nullable=False)

    @classmethod
    def create(cls, db_session, image_url, position, task_id):
        new_image = cls(
            image_url=image_url,
            position=position,
            task_id=task_id,
        )

        db_session.add(new_image)
        db_session.commit()


