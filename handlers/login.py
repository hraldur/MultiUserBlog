from handlers.bloghandler import BlogHandler
from models.user import User

class Login(BlogHandler):
    """
    Logs in user
    """
    def get(self):
        self.render("login-form.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')


        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/mypage')
        else:
            error = "invalid login"
            self.render('login-form.html', error = error)
