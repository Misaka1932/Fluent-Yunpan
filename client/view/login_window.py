import logging
import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QApplication
from PySide6.QtGui import QIcon
from qfluentwidgets import (
    LineEdit, PrimaryPushButton, SubtitleLabel, TitleLabel, 
    CardWidget, MSFluentTitleBar, FluentIcon as FIF,
    StrongBodyLabel, BodyLabel, setTheme, Theme, InfoBar, 
    InfoBarPosition
)
from common.network import NetworkThread, DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000: # Windows 11
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


logger = logging.getLogger('client_logger')
class LoginWindow(Window):
    """ 登录窗口 """
    connect_success = Signal(str, int, NetworkThread)  # 连接成功信号：主机、端口、网络线程

    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setTitleBar(MSFluentTitleBar(self))
        
        # 初始化网络线程
        self.network_thread = NetworkThread(self)
        
        # 设置窗口属性
        self.initWindow()
        
        # 创建主要布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(40, 40, 40, 40)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 设置UI组件
        self.setupUI()
        
        # 初始化信号
        self.initSignals()

    def initWindow(self):
        """初始化窗口属性"""
        # 设置窗口尺寸和图标
        self.resize(800, 600)
        self.setMinimumWidth(600)
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setWindowTitle("云盘客户端 - 登录")
        
        # 设置窗口主题
        setTheme(Theme.AUTO)
        
        # 居中显示
        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
    def setupUI(self):
        # 标题栏
        self.titleLabel = TitleLabel("欢迎使用香草云盘客户端", self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.subtitleLabel = SubtitleLabel("请连接到服务器", self)
        self.subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 卡片容器
        self.cardWidget = CardWidget(self)
        self.cardLayout = QVBoxLayout(self.cardWidget)
        self.cardLayout.setContentsMargins(30, 30, 30, 30)
        self.cardLayout.setSpacing(20)
        
        # 服务器设置
        self.serverSettingsLabel = StrongBodyLabel("服务器设置", self)
        
        hostLayout = QVBoxLayout()
        hostLayout.setSpacing(5)
        hostLabelLayout = QHBoxLayout()
        hostLabelLayout.setContentsMargins(0, 0, 0, 0)
        hostLabelLayout.addWidget(QLabel("主机地址:"))
        hostLabelLayout.addStretch(1)
        self.hostLineEdit = LineEdit(self)
        self.hostLineEdit.setPlaceholderText("服务器地址 (例如: 127.0.0.1)")
        self.hostLineEdit.setText(DEFAULT_SERVER_HOST)
        self.hostLineEdit.setClearButtonEnabled(True)
        hostLayout.addLayout(hostLabelLayout)
        hostLayout.addWidget(self.hostLineEdit)
        
        
        portLayout = QVBoxLayout()
        portLayout.setSpacing(5)
        portLabelLayout = QHBoxLayout()
        portLabelLayout.setContentsMargins(0, 0, 0, 0)
        portLabelLayout.addWidget(QLabel("端口号:"))
        portLabelLayout.addStretch(1)
        self.portLineEdit = LineEdit(self)
        self.portLineEdit.setPlaceholderText("端口号 (例如: 65432)")
        self.portLineEdit.setText(str(DEFAULT_SERVER_PORT))
        self.portLineEdit.setClearButtonEnabled(True)
        portLayout.addLayout(portLabelLayout)
        portLayout.addWidget(self.portLineEdit)
        
        # 连接按钮
        self.connectButton = PrimaryPushButton("连接到服务器", self)
        self.connectButton.setIcon(FIF.LINK)
        
        # 状态标签
        self.statusFrame = QFrame(self)
        self.statusFrame.setObjectName("statusFrame")
        
        statusLayout = QHBoxLayout(self.statusFrame)
        statusLayout.setContentsMargins(15, 10, 15, 10)
        
        self.statusIcon = QLabel(self)
        self.statusIcon.setFixedSize(24, 24)
        
        # 默认显示未连接图标
        disconnected_pixmap = FIF.CANCEL.icon().pixmap(24, 24)
        self.statusIcon.setPixmap(disconnected_pixmap)
        
        self.statusLabel = BodyLabel("尚未连接到服务器", self)
        
        statusLayout.addWidget(self.statusIcon)
        statusLayout.addWidget(self.statusLabel, 1)
        
        # 添加组件到卡片布局
        self.cardLayout.addWidget(self.serverSettingsLabel)
        self.cardLayout.addLayout(hostLayout)
        self.cardLayout.addLayout(portLayout)
        self.cardLayout.addWidget(self.connectButton)
        self.cardLayout.addWidget(self.statusFrame)
        
        # 添加组件到主布局
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.subtitleLabel)
        self.mainLayout.addWidget(self.cardWidget)
        self.mainLayout.addStretch(1)

    def initSignals(self):
        self.connectButton.clicked.connect(self._on_connect_clicked)
        self.hostLineEdit.returnPressed.connect(self._on_connect_clicked)
        self.portLineEdit.returnPressed.connect(self._on_connect_clicked)
        self.network_thread.connection_status.connect(self._on_connection_status_changed)

    def _on_connect_clicked(self):
        host = self.hostLineEdit.text().strip()
        port_str = self.portLineEdit.text().strip()
        
        if not host:
            self.show_error_info("请输入服务器地址")
            return
            
        if not port_str:
            self.show_error_info("请输入端口号")
            return
        
        try:
            port = int(port_str)
            if not (0 < port < 65536):
                raise ValueError("端口号必须在 1 ~ 65535 之间")
                
            self.set_status("正在连接...", "connecting")
            self.network_thread.connect_to_server(host, port)
            
        except ValueError as e:
            self.set_status(f"端口号无效: {e}", "error")
            self.show_error_info(f"端口号无效: {e}")
    
    def _on_connection_status_changed(self, is_connected, message):
        """处理连接状态变化"""
        if is_connected:
            # 连接成功
            self.set_status(message, "success")
            logger.info(f"连接成功: {message}")
            
            # 触发连接成功信号，传递主机、端口和网络线程
            host = self.hostLineEdit.text().strip()
            port = int(self.portLineEdit.text().strip())
            self.connect_success.emit(host, port, self.network_thread)
            
            # 在文件窗口打开后隐藏登录窗口
            self.hide()
        else:
            # 连接失败
            self.set_status(message, "error")
            logger.error(f"连接错误: {message}")
    
    def set_status(self, message, status_type="default"):
        """ 设置连接状态显示 """
        self.statusLabel.setText(message)
        
        if status_type == "success":
            self.statusFrame.setStyleSheet("#statusFrame { background-color: #E3F2FD; border: 1px solid #2196F3; border-radius: 5px; }")
            self.statusIcon.setPixmap(FIF.COMPLETED.icon().pixmap(24, 24))
            self.statusLabel.setStyleSheet("color: #0D47A1;")
            
        elif status_type == "error":
            self.statusFrame.setStyleSheet("#statusFrame { background-color: #FFEBEE; border: 1px solid #FF5252; border-radius: 5px; }")
            self.statusIcon.setPixmap(FIF.CANCEL.icon().pixmap(24, 24))
            self.statusLabel.setStyleSheet("color: #C62828;")
            
        elif status_type == "connecting":
            self.statusFrame.setStyleSheet("#statusFrame { background-color: #FFF8E1; border: 1px solid #FFC107; border-radius: 5px; }")
            self.statusIcon.setPixmap(FIF.SYNC.icon().pixmap(24, 24))
            self.statusLabel.setStyleSheet("color: #FF8F00;")
            
        else:  # default
            self.statusFrame.setStyleSheet("#statusFrame { border: 1px solid #E0E0E0; border-radius: 5px; }")
            self.statusIcon.setPixmap(FIF.INFO.icon().pixmap(24, 24))
            self.statusLabel.setStyleSheet("color: #616161;")

    def show_error_info(self, message):
        """显示错误提示"""
        InfoBar.error(
            title="连接错误",
            content=message,
            parent=self,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        
    def closeEvent(self, event):
        """ 关闭窗口前，确保网络线程停止 """
        if self.isVisible():  # 只有在窗口被关闭而不是隐藏时才停止应用
            logger.info("正在关闭客户端...")
            if hasattr(self, 'network_thread'):
                self.network_thread.stop()
        super().closeEvent(event) 