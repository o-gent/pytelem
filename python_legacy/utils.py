# uPython support
try: import inspect
except: pass

class Logger():
    def __init__(self):
        # sets self to show all logs
        self.logging_level = 3

    def log(self, message, level = 0):
        if self.logging_level >= level:
            print(inspect.stack()[1][3], " : ", message)
    
    def log_root(self, message, level = 0):
        if self.logging_level >= level:
            print(inspect.stack()[2][3]," called: ", inspect.stack()[1][3], " : ", message)


class uLogger():
    # purely for uPython as logging not needed (so much) and inspect not supported
    def __init__(self):
        self.logging_level = 3
    
    def log(self, message, level = 0):
        if self.logging_level >= level:
            print(message)
    
    def log_root(self, message, level = 0):
        if self.logging_level >= level:
            print(message)