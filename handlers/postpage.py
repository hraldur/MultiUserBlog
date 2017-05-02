from handlers.bloghandler import BlogHandler
from models.comment import Comment
from models.post import Post
from models.like import Like
from models.user import User

import time
from google.appengine.ext import db

class PostPage(BlogHandler):
    """
    Get specific post and related comments
    """
    def get(self, post_id):
        post_key = db.Key.from_path('Post', int(post_id))
        post = db.get(post_key)

        #Get all comments for post id
        comments = Comment.all().filter('post =', post_key)
        comments.order("-created")

        #check if post exists
        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)


        user_id = self.read_secure_cookie('user_id')
        author_id = post.author.key().id()
        edit = False

        #check if logged in user is the author of the post
        #if the user is the author he can edit and/or delete the post
        if user_id:
            if (long(user_id) == author_id):
              edit = True



        #number of likes
        post = Post.by_id(post_id)
        likes = Like.all().filter('post =', post).count()

        self.render("permalink.html", post = post, comments = comments, edit = edit, likes = likes)

    def post(self, post_id):
        #comment
        content = self.request.get('content')

        #check if post exists
        if not self.post_exists(post_id):
            page_error = 'This post does not exist !'
            return self.render('login-form.html', page_error = page_error)

        #Check if user is logged in
        if self.user:
            u = self.user.name
            author = User.by_name(u)

            post = Post.by_id(post_id)

            #Check if user wrote comment
            if content:
                c = Comment(author = author, post = post, content = content )
                c.put()
                time.sleep(0.1)
                self.redirect('/%s' %str(c.post.key().id()))

            else:
                page_error = "content, please!!"
                self.render('permalink.html', page_error = page_error, post = post)


        #User is redirected to login
        else:
            page_error = "You must login in to comment!"
            self.render('login-form.html', page_error = page_error)
