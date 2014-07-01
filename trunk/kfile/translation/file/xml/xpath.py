# coding=utf-8

from kfile.translation import msg_types as MsgCode


class StandardException(Exception):
    msg_code = MsgCode.UNKNOWN_ERROR
    extra_info = "Unknown Error."


class NoXPathInfoError(StandardException):
    msg_code = MsgCode.NO_XPATH_INFO
    extra_info = "No Xpath Information."


class EmptyXPathContent(StandardException):
    msg_code = MsgCode.EMPTY_XPATH_CONTENT
    extra_info = "Xpath Content is Empty."


class XMLSyntaxError(StandardException):
    msg_code = MsgCode.XML_SYNTAX_ERROR
    extra_info = "XML Syntax Error."