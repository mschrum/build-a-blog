import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Root(Handler):
    def get(self):
        self.redirect("/blog")

class BlogHandler(Handler):
    def render_frontpage(self, subject = "", content = "", error = ""):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
        self.render('frontpage.html', subject = subject, content = content, error = error, posts = posts)
    def get(self):
        self.render_frontpage()
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            b = BlogPost(subject = subject, content = content)
            b.put()
            self.redirect("/blog")
        else:
            error = "You need both a title and a body!"
            self.render_frontpage(subject, content, error)

app = webapp2.WSGIApplication([
    ('/', Root),
    ('/blog', BlogHandler)
], debug=True)
