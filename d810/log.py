import os
import shutil
import logging
import logging.config

LOG_CONFIG_FILENAME = "log.ini"
LOG_FILENAME = "d810.log"
Z3_TEST_FILENAME = "z3_check_instructions_substitution.py"


def clear_logs(log_dir):
    shutil.rmtree(log_dir, ignore_errors=True)


def configure_loggers(log_dir):
    """Configure loggers for D810 - IDA 9.1 compatible version"""
    os.makedirs(log_dir, exist_ok=True)
    log_main_file = os.path.join(log_dir, LOG_FILENAME)
    z3_test_file = os.path.join(log_dir, Z3_TEST_FILENAME)

    # IDA 9.1 compatibility: Use basicConfig instead of fileConfig to avoid path issues
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Create file handler for main log
    file_handler = logging.FileHandler(log_main_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_formatter)

    # Configure D810 logger
    d810_logger = logging.getLogger('D810')
    d810_logger.setLevel(logging.DEBUG)
    d810_logger.handlers.clear()  # Clear existing handlers
    d810_logger.addHandler(console_handler)
    d810_logger.addHandler(file_handler)
    d810_logger.propagate = False

    # Configure sub-loggers
    for logger_name in ['D810.ui', 'D810.optimizer', 'D810.chain', 'D810.branch_fixer',
                        'D810.unflat', 'D810.tracker', 'D810.emulator', 'D810.helper',
                        'D810.pattern_search']:
        sub_logger = logging.getLogger(logger_name)
        sub_logger.setLevel(logging.INFO)
        sub_logger.handlers.clear()
        sub_logger.addHandler(file_handler)
        sub_logger.propagate = False

    # Special configuration for Z3 test logger
    z3_file_handler = logging.FileHandler(z3_test_file, mode='w')
    z3_file_handler.setLevel(logging.DEBUG)
    z3_formatter = logging.Formatter('%(message)s')
    z3_file_handler.setFormatter(z3_formatter)

    z3_file_logger = logging.getLogger('D810.z3_test')
    z3_file_logger.setLevel(logging.INFO)
    z3_file_logger.handlers.clear()
    z3_file_logger.addHandler(z3_file_handler)
    z3_file_logger.propagate = False
    z3_file_logger.info("from z3 import BitVec, BitVecVal, UDiv, URem, LShR, UGT, UGE, ULT, ULE, prove\n\n")
