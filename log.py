import logging

log = logging.getLogger("APP")
log_file = logging.FileHandler("data/check_ttn.log")
log_file.setFormatter(logging.Formatter("%(asctime)s, %(name)s : %(message)s"))
log.setLevel(logging.INFO)
log.addHandler(log_file)
