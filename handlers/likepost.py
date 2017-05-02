from handlers.bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from google.appengine.ext import db

class LikePost(BlogHandler):
    """
    User can Like a post once, but can not like their own posts
    """
    def get(self, post_id):
        post_key = db.Key.from_path('Post', int(post_id))
        post = db.get(post_key)

        #Check if user is logged in
        if self.user:

            user_id = self.read_secure_cookie('user_id')
            author_id = post.author.key().id()

            u = self.user.name


            #check if user has permission to like this post
            if long(user_id) != author_id:

                user = User.by_name(u)
                user_key = self.user.key()
                post = Post.by_id(post_id)

                likes = Like.all().filter('post =', post)

                #Check if user has already liked this post
                hasLiked = False
                for l in likes:
                    if l.user.key() == user_key:
                        hasLiked = True

                if not hasLiked:

                    like = Like(user = user, post = post)
                    like.put()

                    count = Like.all().filter('post =', post).count()
                    #count += 1
                    self.render("like.html", like = like, count = count, post = post)
                else:
                    count = Like.all().filter('post =', post).count()
                    page_error = "You have already liked this post"
                    self.render("like.html", count = count, page_error = page_error, post = post)

            else:
                page_error = 'You can not like your own posts'
                self.render('like.html', page_error = page_error, post = post)

        else:
            error = 'please login'
            self.render('login-form.html', error = error, post = post)
