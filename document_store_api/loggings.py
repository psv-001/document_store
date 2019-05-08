import logging, os, socket
import logging.config

host = socket.gethostname()
user = os.environ.get('USER')

path = os.path.abspath(os.path.join(os.getcwd()))
path = os.path.join(path, 'config')
logConfPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'config/logging.ini')

logging.config.fileConfig(logConfPath)
logger = logging.LoggerAdapter(logging.getLogger('sample'), 
                               { "hostname" : host, "user" : user})
