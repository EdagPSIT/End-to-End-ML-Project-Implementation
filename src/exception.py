import sys
import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno

    error_message = "Error occured in python script {} at line number {} and error is {}".format(file_name,line_no,error)

    return error_message

class CustomException(Exception):

    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail)

    def __str__(self):
        return self.error_message
    


# Checking working of code
# try:
#     a = 1/0
# except Exception as e:
#     logging.info('Divide by zero Error')
#     raise CustomException(e,sys)