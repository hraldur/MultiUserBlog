from handlers import BlogFront, DeleteComment, DeletePost
from handlers import EditComment, EditPost, LikePost, Login, Logout
from handlers import MyPage, NewPost, PostPage, Register, Signup

import webapp2


app = webapp2.WSGIApplication([
    ('/signup', Register),
    ('/login', Login),
    ('/logout', Logout),
    ('/?', BlogFront),
    ('/([0-9]+)', PostPage),
    ('/newpost', NewPost),
    ('/mypage', MyPage),
    ('/([0-9]+)/editpost', EditPost),
    ('/([0-9]+)/deletepost', DeletePost),
    ('/([0-9]+)/like', LikePost),
    ('/([0-9]+)/([0-9]+)/editcomment', EditComment),
    ('/([0-9]+)/([0-9]+)/deletecomment', DeleteComment),
    ],
     debug=True)
