# -*- coding: utf-8 -*-
import logging
import signal
import time
import sys


from app.config.settings import _config
from app.webapp.MainHandler import *

def main():
    logging.basicConfig(format="%(asctime)s %(levelname)s\t%(name)s:%(message)s", level= _config._settings['global']['log_level'])
    logging.getLogger("server.worker").setLevel(_config.logLevel)
    app = make_app()
    logging.info("Bind port: {}".format(_config.webport))
    app.listen(_config.webport)
    try:
        logging.info("System started")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
      logging.warn("caught {}, stopping".format(str(e)))
      tornado.ioloop.IOLoop.instance().stop()

    


if __name__ == '__main__':
    main()
