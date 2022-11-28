import logging
from datetime import datetime
import os


LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S_')}.log"
log_file_path = os.path.join(os.getcwd(),"logs",LOG_FILE_NAME)

os.makedirs(log_file_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(log_file_path, LOG_FILE_NAME)

logging.basicConfig(
    filename= LOG_FILE_PATH,
     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)