from datetime import datetime


class MyLogger:
    """
    Logger class, used to log different messages like errors/warnings/information etc.\n
    Have different levels and settings, and can be configured through the configuration file.
    """

    def __init__(self, enabled, file, log_level, rewrite_on_startup=False):
        self._enabled = enabled
        self._file = file
        self._all_log_levels = {"DEBUG": 10,
                                "INFO": 20,
                                "WARNING": 30,
                                "ERROR": 40,
                                "CRITICAL": 50}
        self._log_level = log_level
        self._rewrite_on_startup = rewrite_on_startup
        if self._rewrite_on_startup:
            self._clear_log_file()

    def _clear_log_file(self) -> None:
        """
        This method is used to clear the log file on startup if the user chose to do so.
        :return: None
        """
        with open(self._file, "w", encoding="utf-8") as f:
            f.write("")

    def check_log_level(self, level: str) -> bool:
        """
        Checks where to log the information or no, depending on the currently selected log level.
        :param level: The level of the information we are trying to log
        :return: bool
        """
        if self._all_log_levels[level] >= self._all_log_levels[self._log_level]:
            return True
        else:
            return False

    def log(self, source, message, level, err_type=False, err_traceback=False):
        """
        Write the information as formatted string to the log file.\n\n
        Usage\n
        for debug/info/warning -> .log(__file__, "Message!", "level")\n\n
        for error/critical ->
            get the exception traceback -> tb = sys.exc_info()[2].tb_frame\n
            .log(__file__, "Message", "ERROR", type(ex), tb)
        :param source: File name we are logging from
        :param message: Message to log
        :param level: The level of the info we want to log
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

        with open(self._file, "at", encoding="utf-8") as f:
            f.write(msg)
