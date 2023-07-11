import logging
import os
from datetime import datetime

log_file = "{}.log".format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
log_path = os.path.join(os.getcwd(),'logs',log_file)
os.makedirs(log_path,exist_ok=True)

log_file_path = os.path.join(log_path,log_file)


logging.basicConfig(
    filename=log_file_path,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



# Checking working of code
# if __name__ == "__main__":
#     logging.info("Logging has started")