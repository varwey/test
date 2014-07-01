from kfile.utils.md5_util import get_hex_md5


def get_name_md5(source):
    a = source.split('?')
    if len(a) > 1:
        return get_hex_md5(a[0]), get_hex_md5('?' + a[1])
    else:
        return get_hex_md5(a[0]), None