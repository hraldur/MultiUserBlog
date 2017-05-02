from handlers.bloghandler import BlogHandler
from models.post import Post

class MyPage(BlogHandler):
    """
    Get logged in users posts
    """
    def get(self):
        #check if user is logged in
        if self.user:
            posts = Post.all().filter('author =', self.user.key())
            posts.order("-created")

            self.render('mypage.html', username = self.user.name, posts = posts)
        #if user is not logged in, redirect to login page
        else:
            self.redirect('/login')
