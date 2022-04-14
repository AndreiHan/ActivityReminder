import json
import os


class Config:
    def __init__(self):
        self.location = "config.json"
        self.minutes = 10
        self.notif_nr = 10
        self.move_mouse = True
        self.create_new_config()

    def create_new_config(self):
        if self.is_create_new_config():
            self.import_config_from_user_input()
            self.write_current_config_to_file()
            print("\nCreated new configuration")

            self.print_config()
            self.write_current_config_to_file()
        else:
            self.import_config_from_json()

    def is_create_new_config(self):
        ans_list_negative = ["y", "Y"]
        ans_list_positive = ["n", "N"]

        if not bool(self.get_config_from_file()):
            return True

        print("This is your old config\n")
        self.print_config()
        answer = input("\nDo you want to use your old configuration? y/n: ")
        while answer not in ans_list_positive and answer not in ans_list_negative:
            answer = input("Please use y/n only: ")

        if answer in ans_list_positive:
            return True

        return False

    def print_config(self):
        dictionary = self.get_config_from_file()
        print(json.dumps(dictionary, sort_keys=False, indent=4))

    def import_config_from_json(self):
        dictionary = self.get_config_from_file()
        self.minutes = dictionary["minutes"]
        self.notif_nr = dictionary["notif_nr"]
        self.move_mouse = dictionary["move_mouse"]

    def import_config_from_user_input(self):
        self.minutes = self.get_user_input_minutes()
        self.notif_nr = self.get_user_input_notif_nr()
        self.move_mouse = self.get_user_input_mouse()

    def write_current_config_to_file(self):
        dictionary = {"minutes": self.minutes, "notif_nr": self.notif_nr, "move_mouse": self.move_mouse}

        with open(self.location, "w+") as outfile:
            json.dump(dictionary, outfile)

    def get_config_from_file(self):

        if os.path.isfile(self.location):
            try:
                with open(self.location) as f:
                    data = json.loads(f.read())
                    return data
            except ValueError:
                data = {}
                return data

    def get_user_input_mouse(self):
        ans_list_positive = ["y", "Y"]
        ans_list_negative = ["n", "N"]

        answer = input("Do you want to move the mouse? y/n: ")
        while answer not in ans_list_positive and answer not in ans_list_negative:
            answer = input("Please use y/n only: ")

        if answer in ans_list_positive:
            self.move_mouse = True
            return True

        self.move_mouse = False
        return False

    def get_user_input_minutes(self):
        message = "How often to receive a notification? [In minutes]: "
        minutes = 10
        try:
            minutes = int(input(message))
            if minutes <= 0:
                print("0 or smaller cannot be used")
                self.get_user_input_minutes()
        except ValueError:
            print("Please only use numbers")
            self.get_user_input_minutes()
        self.minutes = minutes
        return minutes

    def get_user_input_notif_nr(self):
        notif_nr = int()
        message = "How many notifications do you want to receive? "
        try:
            notif_nr = int(input(message))
            if notif_nr <= 0:
                print("0 or smaller cannot be used")
                self.get_user_input_notif_nr()
        except ValueError:
            print("Please only use numbers")
            self.get_user_input_notif_nr()

        self.notif_nr = notif_nr
        return notif_nr
