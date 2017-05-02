from handlers.bloghandler import BlogHandler

from google.appengine.ext import db

class DeleteComment(BlogHandler):
    """
    Users can delete their own comments
    """
    def get(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        if not self.comment_exists(comment_id):
            page_error = 'This comment does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #check if user has permission to delete comment
        if self.user_owns_comment(comment_id):
            self.render("deletecomment.html", comment = comment, post = post)
        else:
            page_error = 'You do not have permission to delete this comment !'
            self.render('blog-front.html', page_error = page_error)

    def post(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        comment_key = db.Key.from_path('Comment', int(comment_id))

        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        if not self.comment_exists(comment_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #Check if user is logged in
        if not self.read_secure_cookie('user_id'):
            page_error = 'please login !'
            return self.render('login-form.html', page_error = page_error)

        #check if user has permission to delete this post
        if self.user_owns_post(post_id):
            #delete comment
            db.delete(comment_key)
        else:
            page_error = 'You do not have permission to delete this comment !'
            self.render('blog-front.html', page_error = page_error)


        self.redirect('/%s' %str(post.key().id()))
