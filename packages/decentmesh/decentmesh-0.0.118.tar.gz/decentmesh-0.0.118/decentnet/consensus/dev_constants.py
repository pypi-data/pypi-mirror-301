"""
Debug Constants
"""
import logging
import os

RUN_IN_DEBUG = bool(os.getenv("DEBUG", False))
LOG_LEVEL = os.getenv("DEBUG_LEVEL", logging.DEBUG)
ENCRYPTION_DEBUG = bool(os.getenv("ENCRYPTION_DEBUG", False))
METRICS = bool(os.getenv("METRICS", False))

BLOCK_SHARE_LOG_LEVEL = os.getenv("BLOCK_SHARE_LOG_LEVEL", logging.ERROR)
SEEDS_AGENT_LOG_LEVEL = os.getenv("SEEDS_AGENT_LOG_LEVEL", logging.INFO)
COMPRESSION_LOG_LEVEL = os.getenv("COMPRESSION_LOG_LEVEL", logging.WARNING)
R2R_LOG_LEVEL = os.getenv("R2R_LOG_LEVEL", logging.INFO)
BLOCK_ERROR_DATA_LOG_LEN = 50
