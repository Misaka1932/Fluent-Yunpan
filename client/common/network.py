import socket
import threading
import json
import os
import logging
from PySide6.QtCore import Qt, Signal, QThread

BUFFER_SIZE = 4096
DEFAULT_SERVER_HOST = '127.0.0.1'
DEFAULT_SERVER_PORT = 65432
LOG_DIR = 'clientinfo/log'

logger = logging.getLogger('client_logger')

class NetworkThread(QThread):
    """ 在单独的线程中处理网络请求，避免GUI冻结 """

    connection_status = Signal(bool, str)       # 连接成功/失败，附加消息
    file_list_received = Signal(list)           # 文件列表数据

    download_progress = Signal(str, int)        # 文件名，进度百分比
    download_finished = Signal(str, bool, str)  # 文件名，是否成功，消息

    upload_progress = Signal(str, int)          # 文件名，进度百分比
    upload_finished = Signal(str, bool, str)    # 文件名，是否成功，消息

    update_progress = Signal(str, int)          # 文件名，进度百分比
    update_finished = Signal(str, bool, str)    # 文件名，是否成功，消息

    general_message = Signal(str, str)          # 消息类型 (info, error), 消息内容

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client_socket = None
        self.is_connected = False
        self.request_queue = []  # (command, data)
        self.mutex = threading.Lock()
        self.running = True

    def connect_to_server(self, host, port):
        """ 连接到服务器 """
        self.request_queue.append(("connect", (host, port)))
        if not self.isRunning():
            self.start()

    def disconnect_from_server(self):
        """ 断开与服务器的连接 """
        self.request_queue.append(("disconnect", None))
        if not self.isRunning():
            self.start()
    
    def request_server_file_list(self):
        """ 请求服务器文件列表 """
        if self.is_connected:
            self.request_queue.append(("list_files", None))
        else:
            self.general_message.emit("error", "未连接到服务器，请先连接。")
            logger.error("未连接到服务器，无法获取文件列表")

    def download_server_file(self, filename, save_path):
        """ 下载服务器上的文件 """
        if self.is_connected:
            self.request_queue.append(("download_file", (filename, save_path)))
        else:
            self.general_message.emit("error", "未连接到服务器，请先连接。")
            logger.error("未连接到服务器，无法下载文件")
    
    def upload_client_file(self, local_path, server_filename):
        """ 上传本地文件到服务器 """
        if self.is_connected:
            self.request_queue.append(("upload_file", (local_path, server_filename)))
        else:
            self.general_message.emit("error", "未连接到服务器，请先连接。")
            logger.error("未连接到服务器，无法上传文件")
    
    def update_file(self, local_path, server_filename):
        """ 更新服务器上的文件 """
        if self.is_connected:
            self.request_queue.append(("update_file", (local_path, server_filename)))
        else:
            self.general_message.emit("error", "未连接到服务器，请先连接。")
            logger.error("未连接到服务器，无法更新文件")

    def _receive_exact(self, size):
        """ 确保接收到指定大小的数据 """
        data = b''
        while len(data) < size:
            chunk = self.client_socket.recv(min(size - len(data), BUFFER_SIZE))
            if not chunk:
                raise socket.error("连接在接收数据时中断")
            data += chunk
        return data

    def _read_header_and_data(self):
        """ 读取由换行符分隔的头部和之后的数据体 """
        buffer = b''
        while True:
            # 这里可以一次多读一点，然后在buffer里找换行符
            char = self.client_socket.recv(1)
            if not char:
                raise socket.error("接收头部时连接中断")
            if char == b'\n':
                break
            buffer += char
        
        header_str = buffer.decode('utf-8')
        status, data_len_str = header_str.split('|',1)
        data_len = int(data_len_str)
        body_data = self._receive_exact(data_len)

        return status, body_data

    def run(self):
        """线程主循环，处理请求队列中的任务。"""
        while self.running:
            if not self.request_queue:
                self.msleep(100)
                continue

            self.mutex.acquire()
            command, data = self.request_queue.pop(0)
            self.mutex.release()

            try:
                if command == "connect":
                    host, port = data
                    if self.client_socket:
                        try: self.client_socket.close() 
                        except: pass
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.settimeout(5)            # 连接超时5秒
                    self.client_socket.connect((host, port))
                    self.is_connected = True
                    self.connection_status.emit(True, f"成功连接到 {host}:{port}")

                elif command == "disconnect":
                    if self.client_socket:
                        self.client_socket.close()
                    self.is_connected = False
                    self.client_socket = None
                    self.connection_status.emit(False, "已断开连接。")
                
                elif command == "list_files":
                    self.client_socket.sendall(b"LIST_FILES")

                    # 服务器会先发头部 (OK_LIST|json_len) 
                    # 再发 \n 
                    # 再发json数据

                    status, body_data = self._read_header_and_data()
                    if status == "OK_LIST":
                        files = json.loads(body_data.decode('utf-8'))
                        self.file_list_received.emit(files)
                    else:
                        self.general_message.emit("error", f"获取文件列表失败: {body_data.decode('utf-8', errors='ignore')}")

                elif command == "download_file":
                    filename, save_path = data
                    request = f"DOWNLOAD_FILE|{filename}".encode('utf-8')
                    self.client_socket.sendall(request)

                    # 服务器: 
                    # OK_DOWNLOAD|filesize\n<filedata> 
                    # ERROR|msg

                    header_buffer = b''
                    while b'\n' not in header_buffer:
                        chunk = self.client_socket.recv(BUFFER_SIZE)
                        if not chunk: raise socket.error("下载时连接中断")
                        header_buffer += chunk
                    
                    header_part, file_data_first_chunk = header_buffer.split(b'\n', 1)
                    header_str = header_part.decode('utf-8')

                    if header_str.startswith("ERROR|"):
                        self.download_finished.emit(filename, False, header_str.split('|',1)[1])
                        continue
                    
                    status, filesize_str = header_str.split('|',1)
                    if status == "OK_DOWNLOAD":
                        filesize = int(filesize_str)
                        received_bytes = len(file_data_first_chunk)
                        
                        with open(save_path, 'wb') as f:
                            f.write(file_data_first_chunk)
                            self.download_progress.emit(filename, int(100 * received_bytes / filesize) if filesize > 0 else 100)
                            while received_bytes < filesize:
                                chunk = self.client_socket.recv(BUFFER_SIZE)
                                if not chunk: 
                                    self.download_finished.emit(filename, False, "下载中途连接中断")
                                    raise socket.error("下载中断") # 跳出循环
                                f.write(chunk)
                                received_bytes += len(chunk)
                                self.download_progress.emit(filename, int(100 * received_bytes / filesize))
                        self.download_finished.emit(filename, True, f"文件 '{filename}' 下载完成。")
                    else:
                        self.download_finished.emit(filename, False, f"下载失败: {header_str}")

                elif command == "upload_file":
                    local_path, server_filename = data
                    if not os.path.exists(local_path):
                        self.upload_finished.emit(server_filename, False, f"本地文件 '{local_path}' 不存在。")
                        logger.error(f"本地文件 '{local_path}' 不存在，上传失败")
                        continue
                    
                    filesize = os.path.getsize(local_path)
                    # 命令: UPLOAD_FILE|filename|filesize
                    request = f"UPLOAD_FILE|{server_filename}|{filesize}".encode('utf-8')
                    self.client_socket.sendall(request)
                    logger.info(f"发送上传文件请求: '{server_filename}' ({filesize}字节)")

                    # 服务器响应: READY_TO_RECEIVE\n
                    response_buffer = b''
                    while b'\n' not in response_buffer:
                        chunk = self.client_socket.recv(BUFFER_SIZE)
                        if not chunk: 
                            logger.error("等待服务器上传许可时连接中断")
                            raise socket.error("等待服务器上传许可时连接中断")
                        response_buffer += chunk
                    
                    server_response = response_buffer.split(b'\n',1)[0].decode('utf-8')

                    if server_response == "READY_TO_RECEIVE":
                        sent_bytes = 0
                        with open(local_path, 'rb') as f:
                            while sent_bytes < filesize:
                                chunk = f.read(BUFFER_SIZE)
                                if not chunk: break # 文件读取完毕
                                self.client_socket.sendall(chunk)
                                sent_bytes += len(chunk)
                                self.upload_progress.emit(server_filename, int(100 * sent_bytes / filesize))
                        
                        # 等待服务器的最终确认: OK|msg 或 ERROR|msg
                        final_response_str = self.client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                        if final_response_str.startswith("OK|"):
                            logger.info(f"文件 '{server_filename}' 上传成功")
                            self.upload_finished.emit(server_filename, True, final_response_str.split('|',1)[1])
                        else:
                            logger.error(f"文件 '{server_filename}' 上传失败: {final_response_str}")
                            self.upload_finished.emit(server_filename, False, final_response_str)
                    else:
                        logger.error(f"服务器未能准备接收: {server_response}")
                        self.upload_finished.emit(server_filename, False, f"服务器未能准备接收: {server_response}")

                elif command == "update_file":
                    local_path, server_filename = data
                    if not os.path.exists(local_path):
                        self.update_finished.emit(server_filename, False, f"本地文件 '{local_path}' 不存在。")
                        logger.error(f"本地文件 '{local_path}' 不存在，更新失败")
                        continue
                    
                    filesize = os.path.getsize(local_path)
                    # 命令: UPDATE_FILE|filename|filesize
                    request = f"UPDATE_FILE|{server_filename}|{filesize}".encode('utf-8')
                    self.client_socket.sendall(request)
                    logger.info(f"发送更新文件请求: '{server_filename}' ({filesize}字节)")

                    # 服务器响应: READY_TO_RECEIVE\n
                    response_buffer = b''
                    while b'\n' not in response_buffer:
                        chunk = self.client_socket.recv(BUFFER_SIZE)
                        if not chunk: 
                            logger.error("等待服务器更新许可时连接中断")
                            raise socket.error("等待服务器更新许可时连接中断")
                        response_buffer += chunk
                    
                    server_response = response_buffer.split(b'\n',1)[0].decode('utf-8')

                    if server_response == "READY_TO_RECEIVE":
                        sent_bytes = 0
                        with open(local_path, 'rb') as f:
                            while sent_bytes < filesize:
                                chunk = f.read(BUFFER_SIZE)
                                if not chunk: break # 文件读取完毕
                                self.client_socket.sendall(chunk)
                                sent_bytes += len(chunk)
                                self.update_progress.emit(server_filename, int(100 * sent_bytes / filesize))
                        
                        # 等待服务器的最终确认: OK|msg 或 ERROR|msg
                        final_response_str = self.client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                        if final_response_str.startswith("OK|"):
                            logger.info(f"文件 '{server_filename}' 更新成功")
                            self.update_finished.emit(server_filename, True, final_response_str.split('|',1)[1])
                        else:
                            logger.error(f"文件 '{server_filename}' 更新失败: {final_response_str}")
                            self.update_finished.emit(server_filename, False, final_response_str)
                    else:
                        logger.error(f"服务器未能准备接收更新: {server_response}")
                        self.update_finished.emit(server_filename, False, f"服务器未能准备接收更新: {server_response}")

            except socket.timeout:
                self.general_message.emit("error", "服务器连接超时。")
                if command == "connect": 
                    self.connection_status.emit(False, "连接超时")

                self.is_connected = False # 记得更新连接状态

            except socket.error as e:
                self.general_message.emit("error", f"网络通信错误: {e}")
                self.is_connected = False # 记得更新连接状态

                if command == "connect": 
                    self.connection_status.emit(False, f"连接错误: {e}")

            except json.JSONDecodeError as e:
                self.general_message.emit("error", f"解析服务器响应失败: {e}")

            except Exception as e:
                self.general_message.emit("error", f"处理请求时发生未知错误: {e}")
                # 对于未知错误，也标记为未连接，以防socket状态不一致
                self.is_connected = False 

                if self.client_socket:
                    try: self.client_socket.close() 
                    except: pass

                self.client_socket = None

    def stop(self):
        self.running = False
        self.request_queue.clear()
        if self.client_socket:
            try: self.client_socket.close() 
            except: pass
        self.quit()
        self.wait() 