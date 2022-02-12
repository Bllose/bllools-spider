import logging

def getLevel(level) -> int:
    if level.upper() == 'DEBUG':
        return logging.DEBUG
    elif level.upper() == 'WARN' or level.upper() == 'WARNING':
        return logging.WARNING
    else:
        return logging.INFO