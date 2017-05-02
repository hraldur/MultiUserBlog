from handlers.bloghandler import BlogHandler
from google.appengine.ext import db

class EditPost(BlogHandler):
    """
    Author of the post can edit and repost
    """
    def get(self, post_id):

        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)


        #check if user has permission to edit this post
        if self.user_owns_post(post_id):
            self.render("editpost.html", post = post)
        else:
            page_error = 'You do not have permission to edit this comment !'
            self.render('blog-front.html', page_error = page_error)




    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #Check if user is logged in
        if not self.read_secure_cookie('user_id'):
            page_error = 'please login !'
            return self.render('login-form.html', page_error = page_error)

        subject = self.request.get('subject')
        content = self.request.get('content')

        # Check if user owns post
        if self.user_owns_post(post_id):
            #Check if user wrote subject and content
            if subject and content:
                post.subject = subject
                post.content = content
                #Post
                post.put()
                self.redirect('/%s' %str(post.key().id()))
            #Error message
            else:
                error = "subject and content, please!"
                self.render("editpost.html", post = post, error=error)

        else:
            page_error = 'You do not have permission to edit this comment !'
            self.render('blog-front.html', page_error = page_error)
