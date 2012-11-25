from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

class CurrentUserMailHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			login_url = users.create_login_url(self.request.path)
			self.redirect(login_url)
			return
		try:
			to_addr = self.request.get("friend_email")
			msg_body = self.request.get("message")
			msg_sub = self.request.get("subject")
			if not mail.is_email_valid(to_addr):
				# Return an error message...
				pass

			message = mail.EmailMessage()
			message.sender = user.email()
			message.to = to_addr
			message.body = msg_body
			message.subject = msg_sub
			message.send()
			self.response.out.write("Mail Sent");
		except:
			self.response.out.write ("You have to pass 3 parameters using GET:<br> 1) friend_email <br> 2) message <br> 3) subject<br>");

		
class MailSender(webapp.RequestHandler):
	def get(self):

			message = mail.EmailMessage(sender="Udit Agarwal <uditiiita@gmail.com>",
							                            subject="Your account has been approved")

			message.to = "uditagarwal37@gmail.com"
			message.body = """
			Dear Udit:

			Your example.com account has been approved.  You can now visit
			http://www.example.com/ and sign in using your Google Account to
			access new features.

			Please let us know if you have any questions.

			The example.com Team
			"""

			message.send()
			self.response.out.write("Done")

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, webapp World!')
class TestHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("Test Page created for testing purposes<br>");
application = webapp.WSGIApplication(
				[('/sendmail', MailSender),
				('/custom', CurrentUserMailHandler),
				('/test', TestHandler),
				('/', MainPage)],
				debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
