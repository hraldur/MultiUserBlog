from google.appengine.ext import db

from user import User
from utility import render_str



class Post(db.Model):
    """
    Create Post Model
    """
    author = db.ReferenceProperty(User,
                                collection_name='posts',
                                )
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now =True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)


    @classmethod
    def by_id(cls, post_id):
        return Post.get_by_id(int(post_id))

    @classmethod
    def by_author(cls, author):
        return Post.by_author(author)
