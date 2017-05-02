from google.appengine.ext import db
from user import User
from post import Post

class Like(db.Model):
    """
    Create Like Model
    """
    user = db.ReferenceProperty(User,
                                collection_name = 'user_likes',
                                required = True)
    post = db.ReferenceProperty(Post,
                                collection_name = 'post_likes',
                                required = True)

    @classmethod
    def by_post(cls, post):
        return Like.get_by_post(post)
