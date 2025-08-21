from backend import emails


def send_change_email_mail(context, to):
    email = emails.ChangeEmail(context)
    if not isinstance(to, list):
        to = [to]
    email.send(to)
    return True
