from handlers.bloghandler import BlogHandler
import utility

from models.post import Post

from google.appengine.ext import db

class BlogFront(BlogHandler):
    """
    Get Blog frontpage
    """
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render("blog-front.html", posts = posts)
