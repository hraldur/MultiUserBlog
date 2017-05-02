import os

import hashlib
import hmac
import webapp2
import jinja2

from utility import render_str
from models.user import User

from google.appengine.ext import db

secret = 'slfruisoink'

def make_secure_val(val):
    """
    Create a secure value
    """
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    """
    Check if value is secure
    """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    #render html using template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    #set secure cookie to browser
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    #Read secure cookie from browser
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    #verifies user information
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    #remove login information
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    # check if post exists
    def post_exists(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if post:
            return True

    # check if comment exists
    def comment_exists(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        if comment:
            return True

    # check if user owns post
    def user_owns_post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        user_id = self.read_secure_cookie('user_id')
        author_id = post.author.key().id()

        return long(user_id) == author_id

    # check if user owns comment
    def user_owns_comment(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        user_id = self.read_secure_cookie('user_id')
        author_id = comment.author.key().id()

        if user_id == '':
            return False

        return long(user_id) == author_id

    # check if user is logged in
    def check_user_logged_in(self):
        if self.user:
            return True
        else:
            self.redirect('/login')

    def get_post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
