import logging, sys, traceback, threading
import colorama

def thread_except_hook(args):
    log_except_hook(args.exc_type, args.exc_value, args.exc_traceback)

def log_except_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return None
    logging.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt):
        super().__init__(fmt=fmt, datefmt=datefmt)
        grey = "\033[90m"
        white = "\033[97m"
        yellow = "\033[33m"
        red = "\033[31m"
        bold_red = "\033[1;31m"
        reset = "\033[0m"

        self.FORMATS = {
            logging.DEBUG: grey + self._fmt + reset,
            logging.INFO: white + self._fmt + reset,
            logging.WARNING: yellow + self._fmt + reset,
            logging.ERROR: red + self._fmt + reset,
            logging.CRITICAL: bold_red + self._fmt + reset
        }

    def format(self, record):
        log_fmt = self._fmt
        if isinstance(record.handler, logging.StreamHandler):
            log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup(level=logging.DEBUG, capture_warnings=True, exception_hook=True, tg_handler=False, file_handler=False, file_config=None, tg_config=None):
    """
    file_config
        name [dvlogger_{kind}]
        level
        kind [DATE/ROTATING/APPEND/OVERWRITE]
        rotate_max
        rotate_size
        date_format

    tg_config
        level [ERROR]
        bot_key
        chat_id
        thread_id [None]
    """

    colorama.init()
    formatter_string = '%(asctime)s - %(threadName)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
    formatter_string_date = '%Y-%m-%d %H:%M:%S.%f'
    logging.captureWarnings(capture_warnings)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = CustomFormatter(fmt=formatter_string, datefmt=formatter_string_date)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler]

    if exception_hook:
        sys.excepthook = log_except_hook
        threading.excepthook = thread_except_hook

    if tg_handler:
        pass

    if file_handler:
        if file_config['kind'] == 'ROTATING':
            file_handler = RotatingFileHandler(f'{file_config.get("name", "dvlogger_rotating")}.log', mode='a', maxBytes=file_config['rotate_max'], backupCount=file_config['rotate_size'])
            file_handler.setLevel(file_config['level'])
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        elif file_config['kind'] == 'DATE':
            pass
        elif file_config['kind'] == 'APPEND':
            pass
        elif file_config['kind'] == 'OVERWRITE':
            pass

    logging.info('*******')
