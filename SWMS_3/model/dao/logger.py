from datetime import datetime


class MyLogger:
    def __init__(self, enabled, file, log_level, rewrite_on_startup=False):
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

    def log(self, source, message, level, err_type=False, err_traceback=False):
        """
        Usage\n
        for debug/info/warning -> .log(__file__, "Message!", "level")\n\n
        for error/critical ->
            get the exception traceback -> tb = sys.exc_info()[2].tb_frame\n
            .log(__file__, "Message", "ERROR", type(ex), tb)
        :param source: File name we are logging from
        :param message: Message to log
        :param level: What type of log is it
        :param err_type: False by default, if not provide exception type
        :param err_traceback: False by default if not provide exception traceback
        :return: None
        """
        if not self.check_log_level(level):
            return
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%y %H:%M:%S")
        msg = f"Timestamp: {timestamp}    -    {level}    -    Logged from: {source}   -   {message}\n"

        if err_type != False and err_traceback != False:
            msg = f"Timestamp: {timestamp}    -    {level}    -    Logged from: {source}    -    " \
                  f"ErrType: {err_type}    -    ErrTraceback: {err_traceback}    -    {message}\n"

        with open(self.file, "at", encoding="utf-8") as f:
            f.write(msg)
