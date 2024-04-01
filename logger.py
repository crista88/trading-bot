 ### defining the path  liniile astea de cod ma aj sa definesc calea###
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as lg
import os
from datetime import datetime


def initialize_logger():
    # Define the logs directory
    logs_path = ".\\logs\\"

    # Create the logs directory if it doesn't exist
    try: 
        os.makedirs(logs_path, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed - it does not have to be bad" % logs_path)
    else:
        print("Successfully created log directory")

    # Generate log file name based on current time
    date = datetime.now().strftime("%Y%m%d_%H%M%S")  
    log_name = date + ".log"
    currentLog_path = os.path.join(logs_path, log_name)

    # Configure logging
    lg.basicConfig(filename=currentLog_path, format="%(asctime)s - %(levelname)s: %(message)s", level=lg.DEBUG, encoding="utf-8")
    lg.getLogger().addHandler(lg.StreamHandler())
    
    # Log some messages
    lg.info("Log initialized!")
    