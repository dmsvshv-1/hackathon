import datetime
class Loggger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        vremya = datetime.datetime.now()
        stroka = f"{vremya} - {message}\n"
        print(stroka)
        with open(self.log_file, 'a') as f:
            f.write(stroka)
            