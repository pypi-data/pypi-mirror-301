import logging
import sys

def setup_logger(verbose: bool = False, color: bool = False, quiet: bool = False, stdout: bool = False):
    log_format = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO

    formatter = None
    colorlog_missing = False
    
    # Attempt to import colorlog and set up colored logging if requested
    if color:
        try:
            import colorlog
            colored_log_format = "%(cyan)s%(asctime)s %(purple)s%(name)-24s %(log_color)s%(levelname)-8s%(reset)s%(message)s"  # noqa: E501
            formatter = colorlog.ColoredFormatter(colored_log_format, datefmt=date_format)
        except ImportError:
            colorlog_missing = True
            formatter = logging.Formatter(log_format, datefmt=date_format)
    else:
        formatter = logging.Formatter(log_format, datefmt=date_format)

    # Set up the log handler and apply the formatter
    destination = sys.stdout if stdout else sys.stderr
    handler = logging.StreamHandler(destination)
    handler.setFormatter(formatter)

    # Get the root logger and set root configuration
    logger = logging.getLogger("dnsconfigurator")
    logger.setLevel(log_level)
    logger.addHandler(handler)

    # Prevent logging duplication
    if len(logger.handlers) > 1:
        logger.handlers = [handler]

    # Get correct child logger
    logger = logging.getLogger(__name__)
    # Log a warning if colorlog was requested but not available
    if verbose and quiet:
        logger.warning("You can't have both verbose and quiet. Going with verbose")
    if colorlog_missing:
        logger.warning("colorlog module not found, using standard logging format.")
    logger.debug(f"Logging enabled with verbose={verbose} and color={color}")

