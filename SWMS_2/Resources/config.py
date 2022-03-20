WAREHOUSE_TYPES = ["Virtual", "Raw Materials", "Finished Goods"]

# The key used for the password encryption
# Usually it is better to be stored somewhere less exposed
KEY = b'UldGNfHfPDDFdDpf-eLNx8rnoi9S-qyYEEKUI-MA3N4='

# Logging setup
#   Logging levels:
#       DEBUG -> Lowest level. Used to record simple details.
#       INFO -> Record general information.
#       WARNING -> Potential issues which may not cause errors in the future.
#       EROR -> Due to a more serious problem, the software has not been able #                 to perform some function
#       CRITICAL -> Highest level. Blockers which fails your whole program.
LOG_ENABLED = True
REWRITE_LOG_ON_STARTUP = False
LOG_LEVEL = "DEBUG"
DEFAULT_LOG_FILE = "log.txt"
