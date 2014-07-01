# -*- coding: utf-8 -*-
import string
from os import urandom
from random import choice

__author__ = 'lhfu'


def generate_passwd():
    passwd_length = 10
    passwd_seed = string.digits + string.ascii_letters + string.punctuation
    '''''Function to generate a password'''
    passwd = []
    while (len(passwd) < passwd_length):
        passwd.append(choice(passwd_seed))
    return ''.join(passwd)