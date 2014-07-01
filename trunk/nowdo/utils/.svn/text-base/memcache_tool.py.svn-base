# coding=utf-8

"""
Memcached 操作，应该做成对象的。结果写成了一堆方法。

"""
import traceback
from functools import wraps
from flask import current_app
import memcache
from nowdo.config import setting


MEMCACHED_PREFIXES = ['snapshot', 'v2_snapshot']

print 'Connecting to memcached:', setting.MEMCACHED_MACHINES
memcached_client = memcache.Client(setting.MEMCACHED_MACHINES, debug=0)
#remote_memcached_clients = [memcache.Client(machines) for machines in REMOTE_MEMCACHED_MACHINES_LIST]


def traceback_wrap(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            current_app.logger.warn(traceback.format_exc())

    return new_func


@traceback_wrap
def memcache_delete(key, do_remote=False, **kwargs):
    ret = memcached_client.delete(str(key), **kwargs)
    if do_remote:
    #        remote_memcached_op.delay('delete', str(key), **kwargs)
        pass
    return ret


@traceback_wrap
def memcache_delete_multi(keys, do_remote=False, **kwargs):
    keys = [str(key) for key in keys]
    ret = memcached_client.delete_multi(keys, **kwargs)
    if do_remote:
    #        remote_memcached_op.delay('delete_multi', keys, **kwargs)
        pass
    return ret


@traceback_wrap
def memcache_get(key, **kwargs):
    return memcached_client.get(str(key), **kwargs)


@traceback_wrap
def memcache_set(key, val, do_remote=False, **kwargs):
    key = str(key)
    if 'time' not in kwargs:
        kwargs['time'] = 3600 * 24 * 7
    if do_remote:
    #        remote_memcached_op.delay('set', key, val, **kwargs)
        pass
    return memcached_client.set(str(key), val, **kwargs)


@traceback_wrap
def memcache_get_multi(keys, **kwargs):
    return memcached_client.get_multi(keys, **kwargs)


@traceback_wrap
def memcache_set_multi(mapping, **kwargs):
    return memcached_client.set_multi(mapping, **kwargs)


@traceback_wrap
def memcache_incr(key):
    return memcached_client.incr(key)


@traceback_wrap
def memcache_decr(key):
    return memcached_client.decr(key)


def join_cache_key(*keys):
    return '#'.join([str(key) for key in keys])


def cache_service_attribute(func):
    """
    :param func:
    :return:

    只Cache *args

    会把函数名加入MEMCACHED_PREFIXES，以便文件更新时遍历删除cache
    """

    if func.__name__ not in MEMCACHED_PREFIXES:
        MEMCACHED_PREFIXES.append(func.__name__)

    @wraps(func)
    def new_func(*args, **kwargs):
        memcache_key = join_cache_key(func.__name__, args[0].name, *args[1:])
        cache = memcache_get(memcache_key)
        if cache:
            current_app.logger.debug('Cache hit for ' + memcache_key)
            return cache
        current_app.logger.debug('Cache missed for ' + memcache_key)
        ret = func(*args, **kwargs)
        cache = ret
        memcache_set(memcache_key, cache)
        return cache

    return new_func


#from kratos.tasks import celery
#
#@celery.task(ignore_result=True)
#def remote_memcached_op(op, *args, **kwargs):
#    t = time.time()
#    for client in remote_memcached_clients:
#        getattr(client, op)(*args, **kwargs)
#    logger.debug('remote_memcached_op costs %.2f' % (time.time() - t))


if __name__ == '__main__':
    memcache_set('1', '2')
