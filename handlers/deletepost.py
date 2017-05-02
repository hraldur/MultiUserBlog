from handlers.bloghandler import BlogHandler
import time
from google.appengine.ext import db

class DeletePost(BlogHandler):
    """
    Author of the post can delete the post
    """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #Check if user is logged in
        if not self.read_secure_cookie('user_id'):
            page_error = 'please login !'
            return self.render('login-form.html', page_error = page_error)


        #check if user has permission to delete this post
        if self.user_owns_post(post_id):
            self.render("deletepost.html", post = post)
        else:
            page_error = 'You do not have permission to delete this comment !'
            self.render('blog-front.html', page_error = page_error)

    def post(self, post_id):
        post_key = db.Key.from_path('Post', int(post_id))

        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #Check if user is logged in
        if not self.read_secure_cookie('user_id'):
            page_error = 'please login !'
            return self.render('login-form.html', page_error = page_error)

        #check if user has permission to delete this post
        if self.user_owns_post(post_id):
            #delete post
            db.delete(post_key)
            time.sleep(0.1)
        else:
            page_error = 'You do not have permission to delete this post !'
            self.render('blog-front.html', page_error = page_error)

        self.redirect('/')
