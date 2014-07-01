import imp
import os
import errno
import sys


class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_envvar(self, variable_name, silent=False):
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        self.from_pyfile(rv)
        return True

    def from_pyfile(self, config_path, silent=False):
        d = imp.new_module('config')
        d.__file__ = config_path
        try:
            execfile(config_path, d.__dict__)
        except IOError, e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, basestring):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __getattr__(self,i):
        if i in self:
            return self[i]

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))


PY2 = sys.version_info[0] == 2
if PY2:
    string_types = (str, unicode)
else:
    string_types = (str, )


def import_string(import_name):
    assert isinstance(import_name, string_types)

    import_name = str(import_name)
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
        # __import__ is not able to handle unicode strings in the fromlist
        # if the module is a package
        if PY2 and isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        try:
            return getattr(__import__(module, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            modname = module + '.' + obj
            __import__(modname)
            return sys.modules[modname]
    except ImportError as e:
        pass