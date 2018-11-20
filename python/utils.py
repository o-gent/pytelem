import inspect


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