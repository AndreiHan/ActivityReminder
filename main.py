import threading
import time
import schedule as sch
import signal
import sys
import pyautogui
from winotify import Notification
import os


def get_mouse():
    ans_list_positive = ["y", "Y"]
    ans_list_negative = ["n", "N"]

    answer = input("Do you want to move the mouse? y/n: ")
    while answer not in ans_list_positive and answer not in ans_list_negative:
        answer = input("Please use y/n only: ")

    if answer in ans_list_positive:
        return True
    return False


def get_minutes():
    message = "How often to receive a notification? [In minutes]: "
    minutes = 10
    try:
        minutes = int(input(message))
        if minutes <= 0:
            print("0 or smaller cannot be used")
            get_minutes()
    except ValueError:
        print("Please only use numbers")
        get_minutes()
    return minutes


# noinspection PyUnusedLocal
def sigint_handler(sig, fra):
    print('KeyboardInterrupt is caught')
    print('Bye now')
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


class ToastMenu:
    def __init__(self):
        self.minutes = get_minutes()
        self.move_mouse = get_mouse()
        self.example_sent = False
        self.notif_sent = -1

    def notification_loop(self):
        self.send_notification()
        sch.every(self.minutes).minutes.do(self.send_notification)
        while True:
            sch.run_pending()
            time.sleep(1)

    def send_notification(self):
        notif = threading.Thread(target=self.notification, args=())
        notif.start()
        self.notif_sent += 1

    def notification(self):
        print("Starting Thread")
        toast = Notification
        icon_path = os.getcwd() + "\\reminder.png"
        if self.example_sent:
            toast = Notification(app_id="Reminder nr: " + str(self.notif_sent),
                                 title="Send a new email",
                                 msg=str(self.minutes) + " minutes have passed!",
                                 icon=icon_path)

        if not self.example_sent:
            self.example_sent = True
            toast = Notification(app_id="Reminder Example",
                                 title="Windows Toast Example",
                                 msg="This is how the notification will look in " + str(self.minutes) + " minutes.",
                                 icon=icon_path)
        toast.show()
        print("Sent notification at: " + str(time.strftime("%H:%M:%S", time.localtime())))
        del toast
        print("Exiting Thread")

    def move_mouse_now(self):
        if self.move_mouse:
            pyautogui.moveTo(100, 100, duration=1)
            pyautogui.moveRel(0, 50, duration=1)


if __name__ == "__main__":
    ToastMenu().notification_loop()
