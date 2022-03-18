from datetime import datetime


class MyLogger():
    def __init__(self, enabled, file, log_level, rewrite_on_startup):
        self.enabled = enabled
        self.file = file
        self.all_log_levels = {"DEBUG": 10,
                               "INFO": 20,
                               "WARNING": 30,
                               "ERROR": 40,
                               "CRITICAL": 50}
        self.log_level = log_level
        self.rewrite_on_startup = rewrite_on_startup
        if self.rewrite_on_startup:
            self.clear_log_file()

    def clear_log_file(self):
        with open(self.file, "w", encoding="utf-8") as f:
            f.write("")

    def check_log_level(self, level):
        if self.all_log_levels[level] >= self.all_log_levels[self.log_level]:
            return True
        else:
            return False

    def log(self, source, message, level):
        if not self.check_log_level(level):
            return
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%y %H:%M:%S")
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"Timestamp: {timestamp}    -    {level}    -    Logged from: {source}   -   {message}\n")
