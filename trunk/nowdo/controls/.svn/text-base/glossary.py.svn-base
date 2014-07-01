# coding=utf-8
"""
created by SL on 14-4-4
"""
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate
from nowdo.utils.paginator import pagination_or_not

__author__ = 'SL'


# 暂时停用
# GlossaryTableTaskRelTable = SA.Table('glossary_table_task_rel', Base.metadata,
#                                      SA.Column('glossary_table_id',
#                                                BIGINT(unsigned=True), SA.ForeignKey('glossary_table.id')),
#                                      SA.Column('task_id',
#                                                BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id')))


class Glossary(Base):
    __tablename__ = 'glossary'

    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    creator_id = SA.Column(BIGINT(unsigned=True), index=True, nullable=True)
    source = SA.Column(SA.Text, nullable=False)
    target = SA.Column(SA.Text, nullable=False)
    tar_lang = SA.Column(SA.String(2), nullable=False)

    # glossary_table_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('glossary_table.id'))

    # @staticmethod
    # def create_glossary(db_session, source, target, glossary_table_id):
    #     glossary = Glossary(source=source,
    #                         target=target,
    #                         glossary_table_id=glossary_table_id)
    #     db_session.add(glossary)
    #     db_session.commit()
    #     return glossary

    def edit(self, source, target):
        self.source = source
        self.target = target
        self.session.commit()

    @staticmethod
    def my_glossaries(db_session, task, user, page=None, per_page=None):
        glossary_query = db_session.query(Glossary).filter(Glossary.creator_id == user.id,
                                                           Glossary.task == task)
        return pagination_or_not(glossary_query, page=page, per_page=per_page, default_per_page=30)



# 暂时停用
# class CheckingGlossary(Base):
#     __tablename__ = 'checking_glossary'
#
#     PER_PAGE = 30
#
#     id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
#     source_task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'))
#
#     source = SA.Column(SA.Text, nullable=False)
#     source_language = SA.Column(SA.String(4), nullable=False)
#
#     target = SA.Column(SA.Text, nullable=True)
#     target_language = SA.Column(SA.String(4), nullable=False)
#     # 推荐者
#     presenter = SA.Column(SA.String(64), nullable=True)
#     # 审核成功后的术语ID
#     glossary_id = SA.Column(BIGINT(unsigned=True), nullable=True)
#
#     @staticmethod
#     def checking_glossaries(db_session, user, page=None, per_page=None):
#         my_task_ids = db_session.query(CrowdSourceTask.id).filter(CrowdSourceTask.creator_id == user.id).subquery()
#         g_query = db_session.query(CheckingGlossary)\
#             .filter(CheckingGlossary.source_task_id.in_(my_task_ids),
#                     CheckingGlossary.glossary_id == None)
#         return pagination_or_not(g_query, page=page, per_page=per_page, default_per_page=CheckingGlossary.PER_PAGE)
#
#     @staticmethod
#     def create(db_session, user, task, source, target, tar_lang):
#         checking_glossary = CheckingGlossary(source_task_id=task.id,
#                                              source=source,
#                                              target=target,
#                                              presenter=user.email,
#                                              source_language=task.src_lang,
#                                              target_language=tar_lang)
#         db_session.add(checking_glossary)
#         db_session.commit()
#
#     @staticmethod
#     def patch_pass_check(db_session, glossary_ids, glossary_table):
#         """
#         批量通过审核
#         返回为通过审核的术语列表
#         """
#         checking_glossary_list = db_session.query(CheckingGlossary)\
#             .filter(CheckingGlossary.id.in_(glossary_ids)).all()
#         cannot_be_passed_glossaries = []
#         for c_glossary in checking_glossary_list:
#             if c_glossary.source_language == glossary_table.source_language \
#                     and c_glossary.target_language == glossary_table.target_language:
#                 c_glossary.pass_check(glossary_table.id)
#             else:
#                 cannot_be_passed_glossaries.append(c_glossary)
#         return cannot_be_passed_glossaries
#
#     def pass_check(self, glossary_table_id):
#         glossary = Glossary.create_glossary(self.session, self.source, self.target, glossary_table_id)
#         self.glossary_id = glossary.id
#         self.session.commit()
#
#     def edit_and_pass_check(self, source, target, glossary_table_id):
#         glossary = Glossary.create_glossary(self.session, source, target, glossary_table_id)
#         self.glossary_id = glossary.id
#         self.session.commit()
#
#
# # 暂时停用
# class GlossaryTable(Base):
#
#     PER_PAGE = 30
#
#     __tablename__ = 'glossary_table'
#
#     id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
#     name = SA.Column(SA.String(128), nullable=False)
#     target_language = SA.Column(SA.String(4), nullable=False)
#     source_language = SA.Column(SA.String(4), nullable=False)
#
#     user_id = SA.Column(BIGINT(unsigned=True), nullable=False)
#
#     glossaries = relationship('Glossary', backref='glossary_table')
#     tasks = relationship(CrowdSourceTask, secondary=GlossaryTableTaskRelTable, backref='glossary_tables')
#
#     @staticmethod
#     def glossary_table_list(db_session, user, page=None, per_page=None):
#         query = db_session.query(GlossaryTable) \
#             .filter(GlossaryTable.user_id == user.id).options(joinedload(GlossaryTable.glossaries))
#         return pagination_or_not(query, page, per_page, default_per_page=GlossaryTable.PER_PAGE)
#
#     @staticmethod
#     def create_glossary_table(db_session, name, source_language, target_language):
#         gt = GlossaryTable(name=name,
#                            user_id=current_user.id,
#                            source_language=source_language,
#                            target_language=target_language)
#         db_session.add(gt)
#         db_session.commit()