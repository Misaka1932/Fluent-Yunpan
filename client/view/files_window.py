import os
import sys
import logging
from PySide6.QtCore import Qt, Signal, QTimer, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, 
    QTableWidgetItem, QLabel, QHeaderView, QFrame, QAbstractItemView,
    QApplication
)
from PySide6.QtGui import QIcon, QColor, QFont
from qfluentwidgets import (
    PushButton, SubtitleLabel, TableWidget, ProgressBar, 
    InfoBar, InfoBarPosition, CardWidget, StrongBodyLabel, 
    TransparentToolButton, MSFluentTitleBar, ToolButton,
    FluentIcon as FIF, setTheme, Theme
)
# from common.network import NetworkThread

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000: # Windows 11
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


logger = logging.getLogger('client_logger')
class FileTableItem(QTableWidgetItem):
    """ 自定义表格项，用于文件名列 """
    def __init__(self, text):
        super().__init__(text)
        self.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

class FileSizeItem(QTableWidgetItem):
    """ 自定义表格项，用于文件大小列，支持按字节大小排序 """
    def __init__(self, size):
        self.size = size
        size_str = self._format_size(size)
        super().__init__(size_str)
        self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    
    def _format_size(self, size):
        """ 将字节大小转换为更友好的显示格式 """
        for unit in ['字节', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}" if unit != '字节' else f"{size} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def __lt__(self, other):
        """ 自定义排序方法，根据实际字节数排序 """
        if isinstance(other, FileSizeItem):
            return self.size < other.size
        return super().__lt__(other)

class FilesWindow(Window):
    """ 文件管理窗口 """
    disconnect_requested = Signal()  # 断开连接请求

    def __init__(self, host, port, network_thread):
        super().__init__()
        self.setObjectName("FilesWindow")
        
        # 保存连接信息
        self.host = host
        self.port = port
        self.network_thread = network_thread
        
        # 初始化窗口
        self.initWindow()
        
        # 创建主要布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(30, 30, 30, 30)
        self.mainLayout.setSpacing(15)
        
        # 初始化UI
        self.initUI()
        
        # 初始化信号
        self.initSignals()
        
        # 记录当前任务
        self.current_task = None
        
        # 连接成功后自动刷新文件列表
        QTimer.singleShot(100, self.refresh_files_requested)

    def initWindow(self):
        """初始化窗口属性"""
        # 设置窗口尺寸
        self.resize(800, 600)
        self.setMinimumWidth(600)
        self.setTitleBar(MSFluentTitleBar(self))

        # 设置窗口图标和标题
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setWindowTitle(f"云盘客户端 - 已连接到 {self.host}")
        
        # 设置窗口主题
        setTheme(Theme.AUTO)
        
        # 居中显示
        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def initUI(self):
        # 顶部标题栏
        self.titleCard = CardWidget(self)
        titleLayout = QHBoxLayout(self.titleCard)
        titleLayout.setContentsMargins(15, 10, 15, 10)
        
        self.titleLabel = SubtitleLabel("服务器文件管理", self)
        self.titleLabel.setObjectName("filesTitle")
        
        self.disconnectButton = TransparentToolButton(FIF.CANCEL, self)
        self.disconnectButton.setToolTip("断开连接并返回登录界面")
        
        titleLayout.addWidget(self.titleLabel)
        titleLayout.addStretch(1)
        titleLayout.addWidget(self.disconnectButton)

        # 工具栏
        self.toolCard = CardWidget(self)
        toolLayout = QHBoxLayout(self.toolCard)
        toolLayout.setContentsMargins(20, 15, 20, 15)
        
        self.refreshButton = PushButton("刷新文件列表", self)
        self.refreshButton.setIcon(FIF.SYNC)
        
        self.uploadButton = PushButton("上传文件", self)
        self.uploadButton.setIcon(FIF.ADD)
        
        toolLayout.addWidget(self.refreshButton)
        toolLayout.addWidget(self.uploadButton)
        toolLayout.addStretch(1)

        # 文件表格
        self.tableCard = CardWidget(self)
        tableLayout = QVBoxLayout(self.tableCard)
        tableLayout.setContentsMargins(0, 0, 0, 0)
        
        # 表格标题
        tableHeaderLayout = QHBoxLayout()
        tableHeaderLayout.setContentsMargins(20, 15, 20, 15)
        
        self.tableHeaderLabel = StrongBodyLabel("文件列表", self)
        tableHeaderLayout.addWidget(self.tableHeaderLabel)
        tableHeaderLayout.addStretch(1)
        
        # 文件表格
        self.fileTable = TableWidget(self)
        self.fileTable.setColumnCount(4)  # 文件名、大小、下载、更新
        self.fileTable.setHorizontalHeaderLabels(["文件名", "文件大小", "下载", "更新"])
        self.fileTable.setAlternatingRowColors(True)
        self.fileTable.setWordWrap(False)
        self.fileTable.setShowGrid(False)
        self.fileTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.setRowCount(0)

        # 调整列宽
        header = self.fileTable.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch) # 文件名列自适应
        self.fileTable.setColumnWidth(1, 120)  # 大小
        self.fileTable.setColumnWidth(2, 80)   # 下载
        self.fileTable.setColumnWidth(3, 80)   # 更新
        
        tableLayout.addLayout(tableHeaderLayout)
        tableLayout.addWidget(self.fileTable)

        # 状态/进度区域
        self.statusCard = CardWidget(self)
        self.statusCard.setVisible(False)  # 默认隐藏
        statusLayout = QVBoxLayout(self.statusCard)
        statusLayout.setContentsMargins(20, 15, 20, 15)
        
        self.taskNameLabel = StrongBodyLabel("当前任务: 无", self)
        self.progressBar = ProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        
        statusLayout.addWidget(self.taskNameLabel)
        statusLayout.addWidget(self.progressBar)

        # 空状态提示
        self.emptyStateFrame = QFrame(self)
        emptyLayout = QVBoxLayout(self.emptyStateFrame)
        emptyLayout.setContentsMargins(0, 40, 0, 40)
        emptyLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.emptyIcon = QLabel(self)
        self.emptyIcon.setPixmap(FIF.FOLDER.icon().pixmap(64, 64))
        self.emptyIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.emptyLabel = StrongBodyLabel("服务器上没有文件", self)
        self.emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        emptyLayout.addWidget(self.emptyIcon)
        emptyLayout.addWidget(self.emptyLabel)
        
        self.tableCard.layout().addWidget(self.emptyStateFrame)
        self.emptyStateFrame.setVisible(False)  # 默认隐藏

        # 添加所有组件到主布局
        self.mainLayout.addWidget(self.titleCard)
        self.mainLayout.addWidget(self.toolCard)
        self.mainLayout.addWidget(self.tableCard, 1)  # 表格区域占据剩余空间
        self.mainLayout.addWidget(self.statusCard)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget#FilesWindow {
                background-color: rgb(249, 249, 249);
            }
            
            QLabel#filesTitle {
                font-size: 18px;
                font-weight: bold;
                color: rgb(45, 140, 240);
            }
        """)

    def initSignals(self):
        # 连接UI事件到槽函数
        self.refreshButton.clicked.connect(self.refresh_files_requested)
        self.uploadButton.clicked.connect(self._on_upload_clicked)
        self.disconnectButton.clicked.connect(self._on_disconnect_clicked)
        
        # 连接网络线程的信号
        self.network_thread.file_list_received.connect(self.update_file_list)
        self.network_thread.download_progress.connect(lambda fn, p: self.set_progress(f"下载 '{fn}'", p))
        self.network_thread.download_finished.connect(self._on_download_finished)
        self.network_thread.upload_progress.connect(lambda fn, p: self.set_progress(f"上传 '{fn}'", p))
        self.network_thread.upload_finished.connect(self._on_upload_finished)
        self.network_thread.update_progress.connect(lambda fn, p: self.set_progress(f"更新 '{fn}'", p))
        self.network_thread.update_finished.connect(self._on_update_finished)
        self.network_thread.general_message.connect(self._show_general_message)

    def _on_disconnect_clicked(self):
        """处理断开连接按钮点击"""
        self.disconnect_requested.emit()
        self.close()  # 关闭文件窗口

    def refresh_files_requested(self):
        """请求刷新文件列表"""
        self.network_thread.request_server_file_list()

    def _on_upload_clicked(self):
        """处理上传按钮点击事件"""
        local_path, _ = QFileDialog.getOpenFileName(self, "选择要上传的文件")
        if local_path:
            server_filename = os.path.basename(local_path)
            self.network_thread.upload_client_file(local_path, server_filename)
            logger.info(f"用户请求上传文件: '{server_filename}'")

    def _request_download(self, server_filename):
        """请求下载指定文件"""
        save_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", server_filename, "所有文件(*.*)"
        )
        if save_path:
            self.network_thread.download_server_file(server_filename, save_path)
            logger.info(f"用户请求下载文件: '{server_filename}'")

    def _request_update(self, server_filename):
        """请求更新指定文件"""
        local_path, _ = QFileDialog.getOpenFileName(
            self, "选择要更新的文件", "", "所有文件(*.*)"
        )
        if local_path:
            self.network_thread.update_file(local_path, server_filename)
            logger.info(f"用户请求更新文件: '{server_filename}'")

    def update_file_list(self, files: list):
        """更新文件表格显示"""
        # 清空表格
        self.fileTable.setRowCount(0)
        
        # 显示空状态或更新表格
        if not files:
            self.emptyStateFrame.setVisible(True)
            self.tableHeaderLabel.setText("文件列表 (空)")
        else:
            self.emptyStateFrame.setVisible(False)
            self.tableHeaderLabel.setText(f"文件列表 ({len(files)}个文件)")
            
            # 添加所有文件到表格
            for file_info in files:
                self._add_file_to_table(file_info['name'], file_info['size'])
        
        logger.info(f"已更新服务器文件列表 (共{len(files)}个文件)")

    def _add_file_to_table(self, filename, size):
        """向表格添加一个文件项"""
        row = self.fileTable.rowCount()
        self.fileTable.insertRow(row)
        
        # 文件名列
        self.fileTable.setItem(row, 0, FileTableItem(filename))
        
        # 文件大小列
        self.fileTable.setItem(row, 1, FileSizeItem(size))
        
        # 下载按钮列
        downloadWidget = QWidget()
        downloadLayout = QHBoxLayout(downloadWidget)
        downloadLayout.setContentsMargins(4, 4, 4, 4)
        downloadLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        downloadButton = TransparentToolButton(FIF.DOWNLOAD)
        downloadButton.setToolTip(f"下载 '{filename}'")
        downloadButton.clicked.connect(lambda checked=False, fn=filename: self._request_download(fn))
        
        downloadLayout.addWidget(downloadButton)
        self.fileTable.setCellWidget(row, 2, downloadWidget)
        
        # 更新按钮列
        updateWidget = QWidget()
        updateLayout = QHBoxLayout(updateWidget)
        updateLayout.setContentsMargins(4, 4, 4, 4)
        updateLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        updateButton = TransparentToolButton(FIF.SYNC)
        updateButton.setToolTip(f"更新 '{filename}'")
        updateButton.clicked.connect(lambda checked=False, fn=filename: self._request_update(fn))
        
        updateLayout.addWidget(updateButton)
        self.fileTable.setCellWidget(row, 3, updateWidget)

    def set_progress(self, task_name, percentage):
        """设置任务进度"""
        self.current_task = task_name
        self.taskNameLabel.setText(f"当前任务: {task_name}")
        self.progressBar.setValue(percentage)
        
        # 显示进度区域
        if not self.statusCard.isVisible():
            self.statusCard.setVisible(True)

    def task_finished(self, task_name=None):
        """任务完成，隐藏进度条"""
        # 如果指定了任务名，且不是当前任务，则忽略
        if task_name and task_name != self.current_task:
            return
            
        # 重置并隐藏进度区域
        self.progressBar.setValue(0)
        self.taskNameLabel.setText("当前任务: 无")
        self.statusCard.setVisible(False)
        self.current_task = None

    def _on_download_finished(self, filename, success, message):
        """ 处理下载完成事件 """
        self.task_finished(f"下载 '{filename}'")
        if success:
            logger.info(f"下载完成: {message}")
            self.show_message("success", "下载完成", message)
        else:
            logger.error(f"下载失败: {message}")
            self.show_message("error", "下载失败", message)

    def _on_upload_finished(self, filename, success, message):
        """ 处理上传完成事件 """
        self.task_finished(f"上传 '{filename}'")
        if success:
            logger.info(f"上传完成: {message}")
            self.show_message("success", "上传完成", message)
            self.refresh_files_requested()  # 上传成功后刷新列表
        else:
            logger.error(f"上传失败: {message}")
            self.show_message("error", "上传失败", message)
            
    def _on_update_finished(self, filename, success, message):
        """ 处理更新完成事件 """
        self.task_finished(f"更新 '{filename}'")
        if success:
            logger.info(f"更新完成: {message}")
            self.show_message("success", "更新完成", message)
            self.refresh_files_requested()  # 更新成功后刷新列表
        else:
            logger.error(f"更新失败: {message}")
            self.show_message("error", "更新失败", message)

    def _show_general_message(self, msg_type, content):
        """ 显示一般消息 """
        if msg_type == "error":
            logger.error(content)
            self.show_message("error", "错误", content)
        else:
            logger.info(content)
            self.show_message("info", "提示", content)

    def show_message(self, message_type, title, content):
        """ 显示消息条 """
        if message_type == "success":
            InfoBar.success(
                title=title,
                content=content,
                parent=self,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000
            )
        elif message_type == "error":
            InfoBar.error(
                title=title,
                content=content,
                parent=self,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000
            )
        else:
            InfoBar.info(
                title=title,
                content=content,
                parent=self,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000
            ) 