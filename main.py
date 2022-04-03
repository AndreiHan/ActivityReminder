import threading
import time
import schedule as sch
from winotify import Notification
import signal
import sys
import pyautogui


class ToastThread(threading.Thread):
    def __init__(self, example_sent):
        threading.Thread.__init__(self)
        self.example = example_sent

    def run(self):
        toast = Notification
        print("Starting Thread")
        if self.example:
            toast = Notification(app_id="windows app",
                                 title="Winotify Test Toast",
                                 msg="New Notification!",
                                 icon=r"c:\path\to\icon.png")

        if not self.example:
            toast = Notification(app_id="Reminder",
                                 title="Windows Toast Test",
                                 msg="This is how the notification will look")
        toast.show()
        print("Exiting Thread")


def do(example_sent):
    send_notification(example_sent)
    if move_mouse:
        move_mouse()


def move_mouse():
    try:
        pyautogui.moveTo(100, 100, duration=1)
        pyautogui.moveRel(0, 50, duration=1)
    except pyautogui.FailSafeException:
        print("Paused by the user")


def send_notification(example_sent):
    notif = ToastThread(example_sent)
    notif.start()
    notif.join()


def sigint_handler(signal, frame):
    print('KeyboardInterrupt is caught')
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":

    minutes = int(input("How often to receive a notification? [In minutes]: "))
    sch.every(minutes).minutes.do(send_notification)
    move_mouse = False
    example_sent = False

    while True:
        if example_sent:
            sch.run_pending()
            time.sleep(1)
        else:
            send_notification(example_sent)
            example_sent = True
