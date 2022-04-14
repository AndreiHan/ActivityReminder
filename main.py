import threading
import time
import schedule as sch
import signal
import sys
import pyautogui
from winotify import Notification
import os
from config import Config

# noinspection PyUnusedLocal
def sigint_handler(sig, fra):
    print('KeyboardInterrupt is caught')
    print('Bye now')
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


class ToastMenu:
    def __init__(self):
        config = Config()
        self.minutes = config.minutes
        self.notif_nr = config.notif_nr
        self.move_mouse = config.move_mouse
        self.example_sent = False
        self.notif_sent = -1
        del config
        
    def notification_loop(self):
        self.send_notification()
        sch.every(self.minutes).minutes.do(self.send_notification)
        while True:
            sch.run_pending()
            time.sleep(1)
            

    def send_notification(self):
        notif = threading.Thread(target=self.notification, args=())
        notif.start()
        if self.move_mouse:
            move = threading.Thread(target=self.move_mouse_now, args=())
            move.start()
        self.notif_sent += 1

    def notification(self):
        print("\n")
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
        print("This was notification nr:" + str(self.notif_sent))
        del toast


    def move_mouse_now(self):
        if self.move_mouse:
            pyautogui.moveTo(50, 50, duration=1)
            pyautogui.moveTo(100, 100, duration=1)
            pyautogui.moveRel(0, 50, duration=1)


if __name__ == "__main__":
    ToastMenu().notification_loop()
