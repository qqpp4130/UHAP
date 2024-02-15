# !/usr/bin/python
import errno
import shc
import os
from datetime import datetime
from src import HttpServer
from src import Logger
LOGDIR = os.getcwd() + "\\log"
CURRENTTIME = datetime.now().strftime("%Y%m%d%H%M%S")
LOGFILE = LOGDIR + "\\" + CURRENTTIME + ".log"

isLogDir = os.path.exists(LOGDIR)

LOG = Logger.TimestampLogger()

if isLogDir:
    msg = "Log is goint to be logged in " + LOGFILE + "\n"
    LOG.print(msg)
else:
    msg = "./log is incorrect form, trying to fix \n"
    LOG.print(msg)
    try:
        os.remove(LOGDIR)
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise e # re-raise exception if a different error occurred
    except:
        print("Something else went wrong")
        raise
    finally:
        os.makedirs(LOGDIR, exist_ok=True)
        msg = "log directory created \n"
        LOG.print(msg)
