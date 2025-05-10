import os
import sys
import logging

LOG_DIR = 'serverinfo/log'

def ensure_dir(directory_path: str):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"目录 '{directory_path}' 已创建。")
        except OSError as e:
            print(f"创建目录 '{directory_path}' 失败: {e}")
            raise

def setup_logger():
    """ 设置日志记录器 """
    ensure_dir(LOG_DIR)
    
    logger = logging.getLogger('server_logger')
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    log_file = os.path.join(LOG_DIR, 'latest.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger