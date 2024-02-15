from datetime import datetime

class Logger(object):
    def log(self, message):
        global LOGFILE
        f = open(LOGFILE, "a")
        f.write(message + "\n")
        f.close()
        print(message)

class TimestampLogger(Logger):
    def log(self, message):
        message = "{ts} {msg}".format(ts=datetime.now().isoformat(),
                                      msg=message)
        super(TimestampLogger, self).log(message)
    def print(self, message):
        message = "{ts} {msg}".format(ts=datetime.now().isoformat(),
                                      msg=message)
        print(message)