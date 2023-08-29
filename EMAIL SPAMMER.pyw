import yagmail
import customtkinter
import time
import json
import sys
import threading
import random
import names

app = customtkinter.CTk()
app.geometry("300x375")
customtkinter.set_default_color_theme("green")
app.title("Mint Email Spammer")
app.iconbitmap("mint.ico")

label = customtkinter.CTkLabel(app, text="Mint Email Spammer")
label.pack()

label2 = customtkinter.CTkLabel(app, text="Email Sender")
label2.pack()
emailFrom = customtkinter.CTkTextbox(app, height=20)
emailFrom.pack()

label3 = customtkinter.CTkLabel(app, text="Email Reciever")
label3.pack()
emailTo = customtkinter.CTkTextbox(app, height=20)
emailTo.pack()

label4 = customtkinter.CTkLabel(app, text="Google App Password")
label4.pack()
password = customtkinter.CTkTextbox(app, height=20)
password.pack()

label5 = customtkinter.CTkLabel(app, text="Email Text")
label5.pack()
content = customtkinter.CTkTextbox(app, height=20)
content.pack()

label6 = customtkinter.CTkLabel(app, text="Email Subject")
label6.pack()
subject = customtkinter.CTkTextbox(app, height=20)
subject.pack()

enabled = customtkinter.CTkSwitch(app, text="Spam Enabled")
enabled.pack()

emailEnds = ["@gmail.com","@yahoo.com","@hotmail.com","@aol.com","@hotmail.co.uk","@hotmail.fr","@outlook.com"]

spamrandom = customtkinter.CTkSwitch(app, text="Spam Random Emails Enabled")
spamrandom.pack()

def close_app():
    save_config()
    app.destroy()
    sys.exit()

config_file = "email_spammer_config.json"
default_config = {
    "emailFrom": "",
    "emailTo": "",
    "password": "",
    "content": "",
    "subject": ""
}

try:
    with open(config_file, "r") as f:
        saved_config = json.load(f)
except FileNotFoundError:
    saved_config = default_config

emailFrom.insert("end", saved_config["emailFrom"])
emailTo.insert("end", saved_config["emailTo"])
password.insert("end", saved_config["password"])
content.insert("end", saved_config["content"])
subject.insert("end", saved_config["subject"])

def save_config():
    current_config = {
        "emailFrom": emailFrom.get("0.0", "end").strip(),
        "emailTo": emailTo.get("0.0", "end").strip(),
        "password": password.get("0.0", "end").strip(),
        "content": content.get("0.0", "end").strip(),
        "subject": subject.get("0.0", "end").strip()
    }

    with open(config_file, "w") as f:
        json.dump(current_config, f)

app.protocol("WM_DELETE_WINDOW", close_app)

class Spammer:
    @staticmethod
    def send():
        yag = yagmail.SMTP(emailFrom.get("0.0", "end").strip(), password.get("0.0", "end").strip())
        yag.send(
            emailTo.get("0.0", "end").strip(),
            subject.get("0.0", "end").strip(),
            content.get("0.0", "end").strip()
        )
    @staticmethod
    def sendRandom():
        yag = yagmail.SMTP(emailFrom.get("0.0", "end").strip(), password.get("0.0", "end").strip())
        email = ""

        num = random.randint(0,3)

        if num == 0:
            email += names.get_last_name()
        if num == 1:
            email += names.get_first_name()
        if num == 2:
            email +=names.get_full_name()
        if num == 3:
            email +=names.get_full_name()

        time.sleep(0.1)

        email += random.choice(emailEnds)

        email = email.replace(" ", "")

        yag.send(
            email,
            subject.get("0.0", "end").strip(),
            content.get("0.0", "end").strip()
        )

def send_emails_periodically():
    while True:
        if spamrandom.get() == 1:
            enabled.configure(state="disabled")
            Spammer.sendRandom()
        else:
            enabled.configure(state="enabled")

        if enabled.get() == 1:
            spamrandom.configure(state="disabled")
            Spammer.send()
        else:
            spamrandom.configure(state="enabled")
        
        time.sleep(1)

email_thread = threading.Thread(target=send_emails_periodically)
email_thread.daemon = True
email_thread.start()

app.mainloop()
