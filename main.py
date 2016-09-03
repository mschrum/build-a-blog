import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)
class BolgPost(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render('frontpage.html')
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        if title and body:
            self.write("Thank you for submitting a post!")
        else:
            error = "You need both a title and a body!"
            self.render("frontpage.html", error = error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
