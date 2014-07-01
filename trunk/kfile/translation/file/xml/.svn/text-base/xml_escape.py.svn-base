"""
Created on 2012-1-10

@author: onfireNB
"""


def __dict_replace(s, d):
    """
    Replace sub-string of a string using a dictionary.

    """
    for key, value in d.items():
        s = s.replace(key, value)

    return s


def unescape(data, entities=None):
    """
    entities: a dictionary

    Unescape &amp; &lt; and &gt; in a string of data.

    You can unescape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.

    """
    data = data.replace("&lt;", "<")
    data = data.replace("&gt;", ">")
    if entities:
        data = __dict_replace(data, entities)
    # must do ampersand last
    return data.replace("&amp;", "&")