from django.core.mail import EmailMultiAlternatives
import threading


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html_message):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html_message:
            msg.attach_alternative(self.html_message, "text/html")
        msg.send(self.fail_silently)


def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html_message=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html_message).start()
