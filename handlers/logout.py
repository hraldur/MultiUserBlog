from handlers.bloghandler import BlogHandler

class Logout(BlogHandler):
    """
    Logs out user
    """
    def get(self):
        self.logout()
        self.redirect('/login')
