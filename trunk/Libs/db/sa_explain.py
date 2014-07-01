# -*- coding: utf-8 -*-

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement, _literal_as_text


class Explain(Executable, ClauseElement):
    def __init__(self, stmt, analyze=False):
        self.statement = _literal_as_text(stmt)
        self.analyze = analyze


@compiles(Explain, 'mysql')
def pg_explain(element, compiler, **kw):
    text = "EXPLAIN "
    text += compiler.process(element.statement)
    return text


def query_explain(session, query):
    return session.execute(Explain(query, analyze=True)).fetchall()


if __name__ == '__main__':
    pass