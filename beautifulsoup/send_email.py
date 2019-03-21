import smtplib


def send_email(SUBJECT, TEXT):
    SERVER = "localhost"
    FROM = "sender@example.com"
    TO = ["mgivskud9@gmail.com"]  # must be a list

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """.format(FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()
    print("Successfully sent notification mail")
