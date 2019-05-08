import logging, os
import logging.config

path = os.path.abspath(os.path.join(os.getcwd()))
path = os.path.join(path, 'config')
logConfPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'config/logging.ini')
									 
logging.config.fileConfig(logConfPath)

# create logger
logger = logging.getLogger('Document store handler')
