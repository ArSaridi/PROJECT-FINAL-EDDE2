import logging

def logger(process):
    logging.basicConfig(
        format = f"%(asctime)s - [{process}] - [%(levelname)s] - %(message)s",
        level  = logging.INFO)

    return logging
