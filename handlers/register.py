from handlers.bloghandler import BlogHandler
from handlers.signup import Signup
from models.user import User


class Register(Signup):
    """
    Create new user
    """
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)

        self.redirect('/mypage')
