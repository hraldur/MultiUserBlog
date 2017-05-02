from google.appengine.ext import db
from user import User
from post import Post

from utility import render_str

class Comment(db.Model):
    """
    Create Comment Model
    """
    author = db.ReferenceProperty(User,
                                collection_name='user_comments',
                                )
    post = db.ReferenceProperty(Post,
                                collection_name='post_comments')
    content = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now =True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", c = self)
