from handlers.bloghandler import BlogHandler
from models.user import User
from models.post import Post

class NewPost(BlogHandler):
    """
    Create new post
    """
    def get(self):
        #Check if user is logged in
        if self.user:
            self.render("newpost.html")
        #if not logged in, redirect to login
        else:
            self.redirect('/login')

    def post(self):

        subject = self.request.get('subject')
        content = self.request.get('content')

        #Check if user is logged in
        if self.user:
            u = self.user.name
            author = User.by_name(u)

            #check if user wrote subject and content and post
            if subject and content:
                p = Post(author = author, subject = subject, content = content )
                p.put()
                self.redirect('/%s' %str(p.key().id()))
            #else send error
            else:
                error = "subject and content, please!!"
                self.render("newpost.html", subject = subject, content = content, error = error)
        else:
            self.redirect('login')
