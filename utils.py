import os
import traceback
import sys




def write_error_to_log(logger, **kwargs):
    logger.error('ERROR_CLASS: {}'.format(sys.exc_info()[0]))
    logger.error('ERROR_MESSAGE: {}'.format(sys.exc_info()[1]))
    logger.error('TRACEBACK: {}'.format(traceback.format_exc()))
    for name, value in kwargs.items():
        logger.error(name.upper() + ": {}".format(value))




if __name__=="__main__":

    print()
































