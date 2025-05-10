import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from common.utils import setup_logger
from view.login_window import LoginWindow
from view.files_window import FilesWindow

# 设置日志
logger = setup_logger()

class Client:
    def __init__(self):
        self.login_window = None
        self.files_window = None
    
    def start(self):
        """ 启动客户端应用程序 """
        logger.info("客户端程序启动")
        
        # 创建登录窗口
        self.login_window = LoginWindow()
        self.login_window.connect_success.connect(self._on_connect_success)
        self.login_window.show()
    
    def _on_connect_success(self, host, port, network_thread):
        """ 连接成功，打开文件窗口 """
        # 创建文件窗口
        self.files_window = FilesWindow(host, port, network_thread)
        self.files_window.disconnect_requested.connect(self._on_disconnect)
        self.files_window.show()
    
    def _on_disconnect(self):
        """ 断开连接，返回登录窗口 """

        # 销毁文件窗口
        if self.files_window:
            self.files_window = None
        
        # 重新显示登录窗口
        if self.login_window:
            self.login_window.show()

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = "1.25"
    
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app.setQuitOnLastWindowClosed(True)
    
    # 创建并启动客户端
    client = Client()
    client.start()
    
    exit_code = app.exec()
    
    logger.info(f"客户端程序退出，状态码: {exit_code}")
    logging.shutdown()
    return exit_code

if __name__ == '__main__':
    sys.exit(main()) 