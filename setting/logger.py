# -*- coding: utf-8 -*-
import sys
import os
import logging

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set program name
prog_name = os.path.splitext(os.path.basename(__file__))[0]

##### set logger #####
# format, level
log_format = logging.Formatter("%(asctime)s [%(levelname)8s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# handler for standard output
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)

# handler for log file
file_handler = logging.FileHandler(os.path.join(app_home,"log", prog_name + ".log"), "a+")
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

