#!/usr/bin/env python

from django.test import TestCase

# Create your tests here.

import requests
import json

HOST = "http://localhost:8000/api"


def debug_to_file(text):
    open("debug.html", "w").write(text)


def create_user():
    data = dict(
        username="bunkdeath",
        full_name="Amrit Kshetri",
        password="changeme",
        email="bunkdeath@gmail.com"
    )

    data = json.dumps(data)

    url = "%s/%s/" % (HOST, "users")

    print "request url : %s" % url
    print "passed data : %s" % data

    r = requests.post(url, data=data)

    debug_to_file(r.text)

    users = json.loads(r.text)
    print json.dumps(users, indent=4)


def get_users(id=None):
    if id:
        print "getting user with id=%s" % id
        url = "%s/%s/%s" % (HOST, "users", id)
    else:
        print "getting all users"
        url = "%s/%s" % (HOST, "users/")

    print "request url : %s" % url

    r = requests.get(url)

    users = json.loads(r.text)
    print json.dumps(users, indent=4)


def update_users(id):
    print "updating user with id=%s" % id
    url = "%s/%s/%s/" % (HOST, "users", id)
    data = dict(full_name="Amrit Kshetri")
    data = json.dumps(data)

    print "request url : %s" % url
    print "passed data : %s" % data

    r = requests.put(url, data=data)

    users = json.loads(r.text)
    print json.dumps(users, indent=4)


def delete_user(id):
    print "deleting user with id=%s" % id
    url = "%s/%s/%s/" % (HOST, "users", id)

    print "request url : %s" % url

    r = requests.delete(url)

    print r.text

# create_user()
# get_users()
# print "\n--------------------------------------------------\n"
# get_users(2)
# print "\n--------------------------------------------------\n"
# update_users(2)
# print "\n--------------------------------------------------\n"
# delete_user(3)


def login():
    from base64 import b64encode

    print "login"
    url = "%s/%s/" % (HOST, "login")
    data = dict(username="admin", password="changeme")
    # data = dict(username="admin", password="pbkdf2_sha256$12000$x42qd6ucHd5j$UJkso2p4gQ1ZoIj3A60Lies/Uinrfuj4/XMmIlEJTjk=")

    data = json.dumps(data)

    print "request url  : %s" % url
    print "request data : %s" % data
    r = requests.post(url, data=data)
    print r.text
    debug_to_file(r.text)
    # import pdb
    # pdb.set_trace()

login()
