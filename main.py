from topics.exception import TopicsException
import sys
from topics.logger import logging


def exception_test():
    try:
        logging.error("We are dividing by zero")
        x = 1/0
    except Exception as e:
        raise TopicsException(e, sys)


if __name__=="__main__":
    try:
        exception_test()
    except Exception as e:
        print(e)