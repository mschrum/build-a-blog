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
    def render_frontpage(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render('frontpage.html', posts = posts)
    def get(self):
        self.render_frontpage()

class NewPost(Handler):
    def render_newpost(self, subject = "", content = "", error = ""):
        self.render('newpost.html', subject = subject, content = content, error = error)
    def get (self):
        self.render_newpost()
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            b = BlogPost(subject = subject, content = content)
            b.put()
            self.redirect("/blog/" + str(b.key().id()))
        else:
            error = "You need both a title and a body!"
            self.render_newpost(subject, content, error)

class ViewPostHandler(Handler):
    def get(self, id):
        int_id= int(id)
        idnum = BlogPost.get_by_id(int_id)
        if idnum:
            self.render('singlepost.html', error = "",int_id = int_id, idnum = idnum)
        else:
            error = "The post you requested does not exist!"
            self.render('singlepost.html', error = error, int_id = "", idnum = "")
app = webapp2.WSGIApplication([
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/', Root),
    ('/blog', BlogHandler),
    ('/newpost', NewPost)
], debug=True)
