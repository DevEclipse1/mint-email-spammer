import yagmail
import customtkinter
import time
import json
import sys
import threading

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

def close_app():
    save_config()
    app.destroy()
    sys.exit()

close_button = customtkinter.CTkButton(app, text="Close", command=close_app)
close_button.pack()

# Close button
close_button = customtkinter.CTkButton(app, text="Close", command=close_app)
close_button.pack()

# Load data from a configuration file (if it exists)
config_file = "email_spammer_config.json"
default_config = {
    "emailFrom": "",
    "emailTo": "",
    "password": "",
    "content": "",
    "subject": "",
    "enabled": False
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

class Spammer:
    @staticmethod
    def send():
        yag = yagmail.SMTP(emailFrom.get("0.0", "end").strip(), password.get("0.0", "end").strip())
        yag.send(
            emailTo.get("0.0", "end").strip(),
            subject.get("0.0", "end").strip(),
            content.get("0.0", "end").strip()
        )

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

def send_emails_periodically():
    while True:
        if enabled.get() == 1:
            Spammer.send()
        time.sleep(0.01)

email_thread = threading.Thread(target=send_emails_periodically)
email_thread.daemon = True
email_thread.start()

app.mainloop()
