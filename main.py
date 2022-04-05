import threading
import time
import schedule as sch
from winotify import Notification
import signal
import sys
import pyautogui
import os

class ToastThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.example = True

    def run(self):
        toast = Notification
        print("Starting Thread")
        if self.example:
            toast = Notification(app_id="Reminder",
                                 title="Send a new email",
                                 msg="10 Minutes have passed!",
                                 icon=os.getcwd() + "\\reminder.png")
        
        if not self.example:
            self.example = True
            toast = Notification(app_id="Reminder",
                                 title="Windows Toast Test",
                                 msg="This is how the notification will look",
                                 icon=os.getcwd() + "\\reminder.png")
            
        toast.show()
        print("Exiting Thread")


def send_notification():
    notif = ToastThread()
    notif.start()


def wrapper_start(example, move):
    notif = ToastThread()
    notif.example = example
    notif.start()
    if move:
        pyautogui.moveTo(100, 100, duration=1)
        pyautogui.moveRel(0, 50, duration=1)


def sigint_handler(signal, frame):
    print('KeyboardInterrupt is caught')
    print('Bye now')
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":

    move_mouse = False
    example_sent = False

    minutes = int(input("How often to receive a notification? [In minutes]: "))
    ans_list_positive = ["y", "Y"]
    ans_list_negative = ["n", "N"]

    answer = input("Do you want to move the mouse? y/n")
    while answer not in ans_list_positive and answer not in ans_list_negative:
        answer = input("Enter y/n only...  ")

    if answer in ans_list_positive:
        move_mouse = True

    sch.every(minutes).minutes.do(send_notification)

    while True:
        if example_sent:
            sch.run_pending()
            time.sleep(1)
        else:
            wrapper_start(example_sent, move_mouse)
            example_sent = True
