import logging
import logging.handlers
# logs
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-6s :: %(name)s.py -> %(funcName)s() -> L%(lineno)-4d :: %('
                           'message)s')
                    
                   
logger.setLevel(logging.DEBUG)
